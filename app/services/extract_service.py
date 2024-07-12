# app/services/extract_service.py


from app.utils.pdf_parser import pdf_parser
from app.utils.ocr import OCR




class ExtractService:
    def __init__(self):

        self.parser = pdf_parser()
        self.ocr = OCR()

    def extract_from_pdf(self, file_path):
        # try:
            with open(file_path, "rb") as f:
                text, tables = self.parser(file_path)
            return "\n".join(text), tables
        # except Exception as e:
        #     return f"Error extracting from PDF: {str(e)}", []

    def extract_from_image(self, file_path):
        try:
            with open(file_path, "rb") as f:
                text, tables = self.parser(file_path)
            return "\n".join(text), tables
        except Exception as e:
            return f"Error extracting from PDF: {str(e)}", []

from app.services.extract_service import ExtractService

def main():
    extract_service = ExtractService()

    # 设置文件路径
    pdf_file_path = r"G:\python_script\pdf_convertor\tests\data\test.pdf"
    image_file_path = r"G:\python_script\pdf_convertor\tests\data\test.png"

    # 测试从 PDF 提取
    pdf_text, pdf_tables = extract_service.extract_from_pdf(pdf_file_path)
    print("PDF Extraction Result:")
    print("Text:", pdf_text)
    print("Tables:", pdf_tables)
    print()

    # 测试从图像提取
    image_text, image_tables = extract_service.extract_from_image(image_file_path)
    print("Image Extraction Result:")
    print("Text:", image_text)
    print("Tables:", image_tables)

if __name__ == "__main__":
    main()