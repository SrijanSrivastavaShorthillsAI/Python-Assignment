from typing import List, Dict, Any
import tabula
from loader.file_loader import FileLoader
from data_extractor.extractor import DataExtractor
import fitz
import os

class PdfExtractor(DataExtractor):
    def __init__(self, loader: FileLoader):
        super().__init__(loader)

    # * for text
    def extract_text(self) -> List[Dict[str, Any]]:
        """Extract text, headings, and font styles from a PDF file."""
        extracted_data = []
        for page_num, page in enumerate(self.file.pages, start=1):
            text = page.extract_text()
            headings = self.extract_headings(text)
            font_styles = self.extract_font_styles()
            extracted_data.append({
                "page_number": page_num,
                "text": text,
                "headings": headings,
                "font_styles": font_styles
            })
        return extracted_data

    # * for heading
    def extract_headings(self, text: str) -> List[str]:
        """Extract headings from text using simple heuristics."""
        headings = [line.strip() for line in text.splitlines() if line.isupper() or len(line) > 30]
        return headings

    # * for font styles
    def extract_font_styles(self) -> Dict[str, int]:
        """Extract font styles from a PDF by analyzing the text for style indicators."""
        styles = {'bold': 0, 'italic': 0}
        for page in self.file.pages:
            for font in page.get("fonts", []):  # Simplified example, can use more detailed parsing
                if "Bold" in font["name"]:
                    styles['bold'] += 1
                if "Italic" in font["name"]:
                    styles['italic'] += 1
        return styles

    # * for images
    def extract_images(self, output_folder: str) -> List[str]:
        # Open the PDF file
        pdf_document = fitz.open(self.file_path)
        image_paths = []

        # Loop through each page
        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            image_list = page.get_images(full=True)  # Get images from the page
            
            for img_index, img in enumerate(image_list):
                # Extract the image index and the XREF number
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                
                # Get the image bytes
                image_bytes = base_image["image"]
                image_extension = base_image["ext"]  # Get the image extension
                image_path = os.path.join(output_folder, f'image_page_{page_number + 1}_{img_index + 1}.{image_extension}')

                # Save the image
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                image_paths.append([image_path, page_number + 1])

        return image_paths

    # * for links
    def extract_links(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a PDF file."""
        extracted_links = []
        for page_num, page in enumerate(self.file.pages, start=1):
            # Extract annotations from the page
            if '/Annots' in page:
                annotations = page['/Annots']
                for annot in annotations:
                    annot_obj = annot.get_object()  # Get the annotation object
                    # Check if the annotation object has the expected structure
                    if '/A' in annot_obj and '/URI' in annot_obj['/A']:
                        link = annot_obj['/A']['/URI']
                        extracted_links.append({
                            "linked_text": link,  # You can also extract the text if needed
                            "url": link,
                            "page_number": page_num
                        })
        return extracted_links

    # * for tables
    def extract_tables(self, output_folder: str) -> List[str]:
        # Extract tables from PDF
        tables = tabula.read_pdf(self.file_path, pages='all', multiple_tables=True)

        extracted_tables = []

        # Save each table as a CSV file
        for i, table in enumerate(tables):
            csv_file_path = os.path.join(output_folder, f'table_pdf_{i + 1}.csv')
            table.to_csv(csv_file_path, index=False)  # Save to CSV without index
            extracted_tables.append(csv_file_path)

        return extracted_tables