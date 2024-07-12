# app/services/file_service.py

from app.utils.s3_utils import S3Utils
class FileService:
    def __init__(self, upload_dir="uploads"):
        self.s3_utils = S3Utils()

    def upload_file_to_s3(self, file_path, bucket_name, s3_key=None):
        upload_result = self.s3_utils.upload_file_to_s3(file_path, bucket_name, s3_key)
        return upload_result

    def upload_extracted_content_to_s3(self, text, tables, bucket_name, text_key, tables_key):
        text_upload_result = self.s3_utils.upload_content_to_s3(text, bucket_name, text_key)
        tables_upload_result = self.s3_utils.upload_content_to_s3("\n".join(tables), bucket_name, tables_key)
        return text_upload_result, tables_upload_result

    def upload_parsed_content(self, file_path, text_key, tables_key, bucket_name):
        return self.s3_utils.upload_parsed_content(file_path, text_key, tables_key, bucket_name)