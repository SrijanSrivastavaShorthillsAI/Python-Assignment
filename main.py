import os
from datetime import datetime
import pytz
from loader.pdf_loader import PDFLoader
from loader.docx_loader import DOCXLoader
from loader.ppt_loader import PPTLoader
from data_extractor.extractor import DataExtractor
from storage.file_storage import FileStorage

def generate_filename(file_path):
    # Extract the base name of the file (without the directory)
    base_name = os.path.basename(file_path)
    
    # Remove the file extension (e.g., ".pdf")
    name_without_extension = os.path.splitext(base_name)[0]
    
    # Append "output" and current time in IST
    ist = pytz.timezone('Asia/Kolkata')  # Define the IST timezone
    current_time = datetime.now(ist).strftime('%Y-%m-%d_%H-%M-%S')  # Format the current time
    
    # Create the new filename by joining with hyphens
    new_filename = f"{name_without_extension}-output-{current_time}.txt"
    
    return new_filename

def main():
    file_path = 'example.pdf'
    
    # Select appropriate loader based on file extension
    if file_path.endswith('.pdf'):
        loader = PDFLoader()
    elif file_path.endswith('.docx'):
        loader = DOCXLoader()
    elif file_path.endswith('.pptx'):
        loader = PPTLoader()
    else:
        raise ValueError("Unsupported file format")

    # Load and extract data
    extractor = DataExtractor(loader)
    extractor.load(file_path)
    text_data = extractor.extract_text()

    # Generate dynamic output file name
    dynamic_filename = generate_filename(file_path)

    # Store the extracted data with the dynamic file name
    file_storage = FileStorage(extractor)
    file_storage.store_data(text_data, dynamic_filename)

if __name__ == "__main__":
    main()
