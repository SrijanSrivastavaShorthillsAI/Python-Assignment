# Data Extractor

## Overview

Data Extractor is a Python application designed to extract text, hyperlinks, headings, and font styles from various document formats, including PDF, DOCX, and PPTX.

## Features

- **Extract Text**: Retrieve text content from PDF, DOCX, and PPTX files.
- **Extract Headings**: Identify and extract headings based on simple heuristics.
- **Extract Hyperlinks**: Gather all hyperlinks present in the documents.
- **Extract Font Styles**: Identify basic font styles such as bold and italic (currently implemented for PDF).
- **Support for Multiple Formats**: Handle PDF, DOCX, and PPTX files seamlessly.

## Requirements

- Python 3.x
- Required libraries:
  - `PyPDF2`
  - `python-docx`
  - `python-pptx`
  - `pdf2image`
  - `Pillow`

You can install the required libraries using pip:

```bash
pip install PyPDF2 python-docx python-pptx pdf2image Pillow reportlab
