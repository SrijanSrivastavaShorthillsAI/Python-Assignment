from typing import List, Dict, Any
import tabula
from loader.file_loader import FileLoader
from data_extractor.extractor import DataExtractor
from PIL import Image
import io
import os
import pandas as pd

class DocxExtractor(DataExtractor):
    def __init__(self, loader: FileLoader):
        super().__init__(loader)

    # * for text
    def extract_text(self) -> List[Dict[str, Any]]:
        """Extract text and headings from a DOCX file."""
        extracted_data = []
        page_num = 0
        for para in (self.file.paragraphs):
            text = para.text
            if(text):
                page_num += 1;
                headings = self.extract_headings(text)
                font_styles = {}  # You may add logic to extract font styles from DOCX if needed
                extracted_data.append({
                    "page_number":page_num,
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
        """Extract font styles (bold, italic) from a DOCX file."""
        styles = {'bold': 0, 'italic': 0}
        for para in self.file.paragraphs:
            for run in para.runs:
                if run.bold:
                    styles['bold'] += 1
                if run.italic:
                    styles['italic'] += 1
        return styles

    # * for images
    def extract_images(self, output_folder: str) -> List[str]:
        """Extract images from a DOCX file."""
        image_paths = []
        for page_num, rel in enumerate(self.file.part.rels.values(), start=1):
            if "image" in rel.target_ref:
                image_data = rel.target_part.blob
                image = Image.open(io.BytesIO(image_data))
                image_path = os.path.join(output_folder, f'docx_image_{page_num}.png')
                image.save(image_path)
                image_paths.append([image_path, page_num])
        return image_paths

    # * for links
    def extract_links(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a DOCX file."""
        extracted_links = []

        # Access the document's relationships to find hyperlinks
        for page_num, rel in enumerate(self.file.part.rels.values(), start=1):
            if "hyperlink" in rel.reltype:
                hyperlink = rel.target_ref  # Extract the hyperlink URL
                extracted_links.append({
                    "url": hyperlink,
                    "page_number":page_num
                })
        return extracted_links

    # * for tables
    def extract_tables(self, output_folder: str) -> List[str]:
        """Extract tables from a DOCX file and save as CSV."""
        extracted_tables = []
        for i, table in enumerate(self.file.tables):
            # Convert the table to a DataFrame
            data = [[cell.text for cell in row.cells] for row in table.rows]
            df = pd.DataFrame(data)
            csv_file_path = os.path.join(output_folder, f'table_docx_{i + 1}.csv')
            df.to_csv(csv_file_path, index=False, header=False)
            extracted_tables.append(csv_file_path)
        return extracted_tables
