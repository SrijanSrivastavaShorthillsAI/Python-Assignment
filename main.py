import os
import sys
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
from dotenv import load_dotenv
from loader.pdf_loader import PDFLoader
from loader.docx_loader import DOCXLoader
from loader.ppt_loader import PPTLoader
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage
from data_extractor.pdfExtractor import PdfExtractor
from data_extractor.docxExtractor import DocxExtractor
from data_extractor.pptExtractor import PPTExtractor

load_dotenv()

class FileValidationError(Exception):
    """Custom Exception for File Validation Errors."""
    pass

def main():

    file_path = input("Enter the file path: ")
    iterator = {".pdf" : PDFLoader(), ".docx" : DOCXLoader(), ".pptx" : PPTLoader()}
    validator = {".pdf" : PdfReader, ".docx" : Document, ".pptx" : Presentation}
    extractor = {".pdf" : PdfExtractor, ".docx" : DocxExtractor, ".pptx" : PPTExtractor}
    
    
    # Select appropriate loader and validate file based on extension
    for ext in iterator:
        if file_path.endswith(ext):
            try:
                with open(file_path, 'rb') as file:
                    validator[ext](file)  # This will raise an error if the file is corrupted
                    loader = iterator[ext]
                    fileExtractor = extractor[ext]
            except Exception:
                raise FileValidationError("Error : Corrupted file found.")
            break
    else:
        raise FileValidationError("Error : Unsupported file format.")

    # Load and extract data if validation is successful
    print("------------------")
    extractor = fileExtractor(loader)
    extractor.load(file_path)

    output_image = "output_images"
    output_text = "output_text"
    output_tables = "output_tables"

    if not os.path.exists(output_image):
        os.makedirs(output_image)
    if not os.path.exists(output_text):
        os.makedirs(output_text)
    if not os.path.exists(output_tables):
        os.makedirs(output_tables)

    text_data = extractor.extract_text()
    hyperlinks = extractor.extract_links()
    images = extractor.extract_images(output_image)
    tables = extractor.extract_tables(output_tables)

    base_name = os.path.basename(file_path)
    name_without_extension = os.path.splitext(base_name)[0]

    # Define the full paths for the output files
    new_filename_text = os.path.join(output_text, f"{name_without_extension}-output-text_data.txt")
    new_filename_links = os.path.join(output_text, f"{name_without_extension}-output-hyperlinks.txt")

    # Store the extracted data with the dynamic file name
    file_storage = FileStorage(extractor)
    file_storage.store_data(text_data, new_filename_text)
    file_storage.store_data(hyperlinks, new_filename_links)

    # Store the extracted data into SQL database
    sql_storage = SQLStorage(os.getenv("DATABASE_HOST"), os.getenv("DATABASE_USER"), os.getenv("DATABASE_PASSWORD"))

    sql_storage.create_database("python")
    sql_storage.use_database("python")

    sql_storage.create_table_if_not_exists()
    for data in text_data:
        sql_storage.insert_data(
            file_name=os.path.basename(file_path),
            page_number=data.get('page_number'),
            text=data.get('text'),
            headings=data.get('headings'),
            font_styles=data.get('font_styles')
        )

    # Store extracted hyperlinks and images into the database
    for link in hyperlinks:
        sql_storage.insert_link(
            file_name=os.path.basename(file_path),
            page_number=link.get('page_number'),
            linked_text=link.get('linked_text'),
            url=link.get('url')
        )
    
    for image_path, page_number in images:
        sql_storage.insert_image(
            file_name=os.path.basename(file_path),
            image_path=image_path,
            page_number=page_number
        )

    print("Data extraction and storage complete.")

if __name__ == "__main__":
    try:
        main()
    except FileValidationError as e:
        print(e)  # This will print the custom error message without showing a traceback.
        sys.exit(1)  # Exit the program with status code 1 indicating an error.
