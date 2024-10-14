from typing import List, Dict, Any

import tabula
from loader.file_loader import FileLoader
from loader.pdf_loader import PDFLoader
from loader.docx_loader import DOCXLoader
from loader.ppt_loader import PPTLoader
from typing import List, Dict, Any
from loader.file_loader import FileLoader
from loader.pdf_loader import PDFLoader
from loader.docx_loader import DOCXLoader
from loader.ppt_loader import PPTLoader
from pdf2image import convert_from_path
from PIL import Image
import fitz
import os
import io
import pandas as pd

class DataExtractor:
    def __init__(self, loader: FileLoader):
        self.loader = loader
        self.file = None
        self.file_path = None

    def load(self, file_path: str):
        """Load the file using the appropriate loader based on file type."""
        self.file = self.loader.load_file(file_path)
        self.file_path = file_path 

    # * for text
    def extract_text(self) -> List[Dict[str, Any]]:
        """
        Extract text from the loaded file. The method handles PDFs, DOCX, and PPTX files.
        """
        extracted_data = []
        if isinstance(self.loader, PDFLoader):
            extracted_data = self._extract_from_pdf()
        elif isinstance(self.loader, DOCXLoader):
            extracted_data = self._extract_from_docx()
        elif isinstance(self.loader, PPTLoader):
            extracted_data = self._extract_from_pptx()
        return extracted_data

    def _extract_from_pdf(self) -> List[Dict[str, Any]]:
        """Extract text, headings, and font styles from a PDF file."""
        extracted_data = []
        for page_num, page in enumerate(self.file.pages, start=1):
            text = page.extract_text()
            headings = self._extract_headings(text)
            font_styles = self._extract_font_styles(text)
            extracted_data.append({
                "page_number": page_num,
                "text": text,
                "headings": headings,
                "font_styles": font_styles
            })
        return extracted_data

    def _extract_from_docx(self) -> List[Dict[str, Any]]:
        """Extract text and headings from a DOCX file."""
        extracted_data = []
        for para in self.file.paragraphs:
            text = para.text
            headings = self._extract_headings(text)
            font_styles = {}  # You may add logic to extract font styles from DOCX if needed
            extracted_data.append({
                "text": text,
                "headings": headings,
                "font_styles": font_styles
            })
        return extracted_data

    def _extract_from_pptx(self) -> List[Dict[str, Any]]:
        """Extract text and headings from a PPTX file."""
        extracted_data = []
        for slide_num, slide in enumerate(self.file.slides, start=1):
            text = "\n".join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
            headings = self._extract_headings(text)
            font_styles = self._extract_font_styles(text)
            extracted_data.append({
                "slide_number": slide_num,
                "text": text,
                "headings": headings,
                "font_styles": font_styles
            })
        return extracted_data

    
    # * for heading
    def _extract_headings(self, text: str) -> List[str]:
        """Extract headings from text using simple heuristics."""
        headings = [line.strip() for line in text.splitlines() if line.isupper() or len(line) > 30]
        return headings

    # * for font styles
    def _extract_font_styles(self, text: str) -> Dict[str, int]:
        if isinstance(self.loader, PDFLoader):
            return self._extract_font_styles_from_pdf()
        elif isinstance(self.loader, DOCXLoader):
            return self._extract_font_styles_from_docx()
        elif isinstance(self.loader, PPTLoader):
            return self._extract_font_styles_from_pptx()
        
    def _extract_font_styles_from_pdf(self) -> Dict[str, int]:
        """Extract font styles from a PDF by analyzing the text for style indicators."""
        styles = {'bold': 0, 'italic': 0}
        for page in self.file.pages:
            for font in page.get("fonts", []):  # Simplified example, can use more detailed parsing
                if "Bold" in font["name"]:
                    styles['bold'] += 1
                if "Italic" in font["name"]:
                    styles['italic'] += 1
        return styles

    def _extract_font_styles_from_docx(self) -> Dict[str, int]:
        """Extract font styles (bold, italic) from a DOCX file."""
        styles = {'bold': 0, 'italic': 0}
        for para in self.file.paragraphs:
            for run in para.runs:
                if run.bold:
                    styles['bold'] += 1
                if run.italic:
                    styles['italic'] += 1
        return styles

    def _extract_font_styles_from_pptx(self) -> Dict[str, int]:
        """Extract font styles (bold, italic) from a PPTX file."""
        styles = {'bold': 0, 'italic': 0}
        for slide in self.file.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text_frame"):
                    for para in shape.text_frame.paragraphs:
                        for run in para.runs:
                            if run.font.bold:
                                styles['bold'] += 1
                            if run.font.italic:
                                styles['italic'] += 1
        return styles
        

    # * for images
    def extract_images(self, output_folder="output_images") -> List[str]:
        """Extract images from the loaded file (PDF, DOCX, PPTX)."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if isinstance(self.loader, PDFLoader):
            return self._extract_images_from_pdf(output_folder)
        elif isinstance(self.loader, DOCXLoader):
            return self._extract_images_from_docx(output_folder)
        elif isinstance(self.loader, PPTLoader):
            return self._extract_images_from_pptx(output_folder)

    def _extract_images_from_pdf(self, output_folder: str) -> List[str]:
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

                image_paths.append(image_path)

        return image_paths

    def _extract_images_from_docx(self, output_folder: str) -> List[str]:
        """Extract images from a DOCX file."""
        image_paths = []
        for i, rel in enumerate(self.file.part.rels.values()):
            if "image" in rel.target_ref:
                image_data = rel.target_part.blob
                image = Image.open(io.BytesIO(image_data))
                image_path = os.path.join(output_folder, f'docx_image_{i + 1}.png')
                image.save(image_path)
                image_paths.append(image_path)
        return image_paths

    def _extract_images_from_pptx(self, output_folder: str) -> List[str]:
        """Extract images from a PPTX file."""
        image_paths = []
        for i, slide in enumerate(self.file.slides):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # 13 corresponds to 'PICTURE'
                    image = shape.image
                    image_bytes = image.blob
                    image_file_name = f'pptx_image_{i + 1}.png'
                    image_path = os.path.join(output_folder, image_file_name)
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    image_paths.append(image_path)
        return image_paths

    # * for links
    def extract_links(self) -> List[Dict[str, Any]]:
        """
        Extract hyperlinks from the file. Handles PDFs, PPTX, and DOCX files.
        """
        extracted_links = []
        if isinstance(self.loader, PDFLoader):
            extracted_links = self._extract_links_from_pdf()
        elif isinstance(self.loader, DOCXLoader):
            extracted_links = self._extract_links_from_docx()
        elif isinstance(self.loader, PPTLoader):
            extracted_links = self._extract_links_from_pptx()
        return extracted_links

    def _extract_links_from_pdf(self) -> List[Dict[str, Any]]:
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

    def _extract_links_from_pptx(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a PPTX file."""
        extracted_links = []
        for slide_num, slide in enumerate(self.file.slides, start=1):
            for shape in slide.shapes:
                if hasattr(shape, "hyperlink") and shape.hyperlink.address:
                    extracted_links.append({
                        "linked_text": shape.text,
                        "url": shape.hyperlink.address,
                        "slide_number": slide_num
                    })
        return extracted_links

    def _extract_links_from_docx(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a DOCX file."""
        extracted_links = []
        # Access the document's relationships to find hyperlinks
        for rel in self.file.part.rels.values():
            if "hyperlink" in rel.reltype:
                # Extract the hyperlink target
                hyperlink = rel.target_ref
                
                # Find the paragraph that contains this hyperlink
                for para in self.file.paragraphs:
                    for run in para.runs:
                        if hyperlink in run._element.xml:
                            linked_text = run.text
                            extracted_links.append({
                                "linked_text": linked_text,
                                "url": hyperlink,
                                "page_number": None  # DOCX does not have a concept of pages
                            })
        return extracted_links

    # * for tables
    def extract_tables(self, output_folder="output_tables") -> List[str]:
        """Extract tables from the loaded file (PDF, DOCX, PPTX) and save them as CSV files."""
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if isinstance(self.loader, PDFLoader):
            return self._extract_tables_from_pdf(output_folder)
        elif isinstance(self.loader, DOCXLoader):
            return self._extract_tables_from_docx(output_folder)
        elif isinstance(self.loader, PPTLoader):
            return self._extract_tables_from_pptx(output_folder)

    def _extract_tables_from_pdf(self, output_folder: str) -> List[str]:
        # Extract tables from PDF
        tables = tabula.read_pdf(self.file_path, pages='all', multiple_tables=True)

        extracted_tables = []

        # Save each table as a CSV file
        for i, table in enumerate(tables):
            csv_file_path = os.path.join(output_folder, f'table_pdf_{i + 1}.csv')
            table.to_csv(csv_file_path, index=False)  # Save to CSV without index
            extracted_tables.append(csv_file_path)

        return extracted_tables

    def _extract_tables_from_docx(self, output_folder: str) -> List[str]:
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

    def _extract_tables_from_pptx(self, output_folder: str) -> List[str]:
        """Extract tables from a PPTX file and save as CSV."""
        extracted_tables = []
        for slide_num, slide in enumerate(self.file.slides, start=1):
            for shape in slide.shapes:
                if shape.has_table:
                    table = shape.table
                    data = [[cell.text for cell in row.cells] for row in table.rows]
                    df = pd.DataFrame(data)
                    csv_file_path = os.path.join(output_folder, f'table_pptx_slide_{slide_num}.csv')
                    df.to_csv(csv_file_path, index=False, header=False)
                    extracted_tables.append(csv_file_path)

        print(extracted_tables)
        return extracted_tables
