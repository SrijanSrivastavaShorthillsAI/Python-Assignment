import os
import json
from loader.pdf_loader import PDFLoader
from loader.docx_loader import DOCXLoader
from loader.ppt_loader import PPTLoader
from data_extractor.extractor import DataExtractor
from storage.file_storage import FileStorage
from storage.sql_storage import SQLStorage
from dotenv import load_dotenv

load_dotenv()

def main():

    file_path = input("Enter the file path : ")
    iterator = {".pdf" : PDFLoader(), ".docx" : DOCXLoader(), ".pptx" : PPTLoader()}
    
    # Select appropriate loader based on file extension
    for it in iterator:
        if file_path.endswith(it):
            loader = iterator[it]
            break;
    else:
        raise ValueError("Unsupported file format")
    
    # Load and extract data
    extractor = DataExtractor(loader)
    extractor.load(file_path)

    text_data = extractor.extract_text()
    hyperlinks = extractor.extract_links()
    images = extractor.extract_images()
    tables = extractor.extract_tables()

    base_name = os.path.basename(file_path)
    name_without_extension = os.path.splitext(base_name)[0]
    
    output_folder = 'output'  # Directory to save output files

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the full paths for the output files
    new_filename_text = os.path.join(output_folder, f"{name_without_extension}-output-text_data.txt")
    new_filename_links = os.path.join(output_folder, f"{name_without_extension}-output-hyperlinks.txt")

    # Store the extracted data with the dynamic file name
    file_storage = FileStorage(extractor)
    file_storage.store_data(text_data, new_filename_text)
    file_storage.store_data(hyperlinks, new_filename_links)

    # Store the extracted data into SQL database
    sql_storage = SQLStorage(os.getenv("DATABASE_HOST"), os.getenv("DATABASE_USER"), os.getenv("DATABASE_PASSWORD"), os.getenv('DATABASE_NAME'))
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
    main()
