from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.services.extract_service import ExtractService
from app.utils.db_utils import DBUtils
import os
import zipfile
import boto3
from botocore.exceptions import NoCredentialsError
from tempfile import TemporaryDirectory

router = APIRouter()
extract_service = ExtractService()
db_utils = DBUtils()

# Initialize S3 client
s3_client = boto3.client('s3', region_name='your-region-name')

@router.post("/")
async def upload_file(file: UploadFile = File(...), bucket_name: str = "your-bucket-name"):
    try:
        # Save uploaded file
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(file.file.read())

        if zipfile.is_zipfile(file_location):
            results = process_zip(file_location)
        else:
            results = process_single_file(file_location)

        # Save task status to SQLite
        task_id = db_utils.save_task_status(file.filename, "completed")

        # Upload parsed files to S3
        upload_to_s3(file.filename, bucket_name)

        # Clean up temp files
        os.remove(file_location)

        return {"message": "File processed and uploaded", "results": results, "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/download/{task_id}")
async def download_file(task_id: int, bucket_name: str = "your-bucket-name"):
    task = db_utils.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    file_name = task["file_name"]
    parsed_text_path = f"temp/{file_name}_parsed.txt"
    parsed_table_path = f"temp/{file_name}_parsed_table.txt"

    with TemporaryDirectory() as temp_dir:
        txt_file_path = os.path.join(temp_dir, f"{file_name}_parsed.txt")
        table_file_path = os.path.join(temp_dir, f"{file_name}_parsed_table.txt")

        try:
            s3_client.download_file(bucket_name, f"{file_name}_parsed.txt", txt_file_path)
            s3_client.download_file(bucket_name, f"{file_name}_parsed_table.txt", table_file_path)
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS credentials not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error downloading from S3: {str(e)}")

        return FileResponse(txt_file_path, filename=f"{file_name}_parsed.txt")

def process_zip(file_path):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall("extracted_files")

    results = []
    for root, dirs, files in os.walk("extracted_files"):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith(".pdf"):
                result = extract_service.extract_from_pdf(file_path)
            elif file_name.endswith((".png", ".jpg", ".jpeg")):
                result = extract_service.extract_from_image(file_path)
            else:
                result = f"Unsupported file type: {file_name}"
            results.append(result)

            # Save parsed content to files
            parsed_text_path = f"temp/{file_name}_parsed.txt"
            parsed_table_path = f"temp/{file_name}_parsed_table.txt"
            with open(parsed_text_path, "w") as f:
                f.write(result[0])
            with open(parsed_table_path, "w") as f:
                f.write("\n".join(result[1]))

    # Clean up extracted files
    for root, dirs, files in os.walk("extracted_files"):
        for file_name in files:
            os.remove(os.path.join(root, file_name))

    return results

def process_single_file(file_path):
    if file_path.endswith(".pdf"):
        result = extract_service.extract_from_pdf(file_path)
    elif file_path.endswith((".png", ".jpg", ".jpeg")):
        result = extract_service.extract_from_image(file_path)
    else:
        return "Unsupported file type"

    # Save parsed content to files
    parsed_text_path = f"temp/{os.path.basename(file_path)}_parsed.txt"
    parsed_table_path = f"temp/{os.path.basename(file_path)}_parsed_table.txt"
    with open(parsed_text_path, "w") as f:
        f.write(result[0])
    with open(parsed_table_path, "w") as f:
        f.write("\n".join(result[1]))

    return result

def upload_to_s3(file_name, bucket_name):
    parsed_text_path = f"temp/{file_name}_parsed.txt"
    parsed_table_path = f"temp/{file_name}_parsed_table.txt"

    try:
        s3_client.upload_file(parsed_text_path, bucket_name, f"{file_name}_parsed.txt")
        s3_client.upload_file(parsed_table_path, bucket_name, f"{file_name}_parsed_table.txt")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {str(e)}")