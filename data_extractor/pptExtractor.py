from typing import List, Dict, Any
from loader.file_loader import FileLoader
import os
from data_extractor.extractor import DataExtractor
import pandas as pd

class PPTExtractor(DataExtractor):
    def __init__(self, loader: FileLoader):
        super().__init__(loader)

    # * for text
    def extract_text(self) -> List[Dict[str, Any]]:
        """Extract text and headings from a PPTX file."""
        extracted_data = []
        for slide_num, slide in enumerate(self.file.slides, start=1):
            text = "\n".join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
            headings = self.extract_headings(text)
            font_styles = self.extract_font_styles()
            extracted_data.append({
                "page_number": slide_num,
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
    def extract_images(self, output_folder: str) -> List[str]:
        """Extract images from a PPTX file."""
        image_paths = []
        for slide_num, slide in enumerate(self.file.slides, start=1):
            for shape in slide.shapes:
                if shape.shape_type == 13:  # 13 corresponds to 'PICTURE'
                    image = shape.image
                    image_bytes = image.blob
                    image_file_name = f'pptx_image_{slide_num}.png'
                    image_path = os.path.join(output_folder, image_file_name)
                    with open(image_path, 'wb') as f:
                        f.write(image_bytes)
                    image_paths.append([image_path, slide_num])
        return image_paths

    # * for links
    def extract_links(self) -> List[Dict[str, Any]]:
        """Extract hyperlinks from a PPTX file."""
        extracted_links = []
        # Loop through each slide in the presentation
        for slide_num, slide in enumerate(self.file.slides, start=1):
            # Loop through each shape in the slide
            for shape in slide.shapes:
                # Check if the shape has a text frame and it is not None
                if hasattr(shape, "text_frame") and shape.text_frame is not None:
                    # Loop through each paragraph in the text frame
                    for paragraph in shape.text_frame.paragraphs:
                        # Loop through each run in the paragraph
                        for run in paragraph.runs:
                            # Check if the run has a hyperlink and get the link address
                            if run.hyperlink and run.hyperlink.address:
                                extracted_links.append({
                                    "linked_text": run.text,  # Get the text of the hyperlink
                                    "url": run.hyperlink.address,  # Get the hyperlink address
                                    "page_number": slide_num  # Get the slide number
                                })
        return extracted_links

    # * for tables
    def extract_tables(self, output_folder: str) -> List[str]:
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

        return extracted_tables