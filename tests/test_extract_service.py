import pytest
from app.services.extract_service import ExtractService
import os

@pytest.fixture
def extract_service():
    service = ExtractService()
    return service

def test_extract_from_pdf_success(extract_service):
    pdf_path = os.path.join(os.path.dirname(__file__), 'data', 'test.pdf')
    text, tables = extract_service.extract_from_pdf(pdf_path)
    print("Text:", text)
    print("Tables:", tables)
    assert isinstance(text, str)
    assert isinstance(tables, list)

def test_extract_from_pdf_error(extract_service):
    nonexistent_path = os.path.join(os.path.dirname(__file__), 'data', 'nonexistent_file.pdf')
    text, tables = extract_service.extract_from_pdf(nonexistent_path)
    assert "Error extracting from PDF" in text
    assert tables == []

def test_extract_from_image_success(extract_service):
    image_path = os.path.join(os.path.dirname(__file__), 'data', 'test.png')
    text, tables = extract_service.extract_from_image(image_path)
    print(text, tables)
    assert isinstance(text, str)
    assert isinstance(tables, list)

def test_extract_from_image_error(extract_service):
    nonexistent_path = os.path.join(os.path.dirname(__file__), 'data', 'nonexistent_image.jpg')
    text, tables = extract_service.extract_from_image(nonexistent_path)
    assert "Error extracting from PDF" in text
    assert tables == []

if __name__ == "__main__":
    pytest.main()