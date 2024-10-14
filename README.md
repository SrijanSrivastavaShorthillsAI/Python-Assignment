# Data Extractor

## Overview

Data Extractor is a Python application designed to extract text, hyperlinks, headings, and font styles from various document formats, including PDF, DOCX, and PPTX. It provides a modular and extensible framework for efficiently handling and processing document data.

## Features

- **Extract Text**: Retrieve text content from PDF, DOCX, and PPTX files.
- **Extract Headings**: Identify and extract headings based on simple heuristics.
- **Extract Hyperlinks**: Gather all hyperlinks present in the documents.
- **Extract Font Styles**: Identify basic font styles such as bold and italic (currently implemented for PDF).
- **Support for Multiple Formats**: Handle PDF, DOCX, and PPTX files seamlessly.
- **Table Extraction**: Extract tables from PDF, DOCX, and PPTX files.
- **Image Extraction**: Extract images embedded in PDF, DOCX, and PPTX files.
- **Database Storage**: Save extracted data (text, hyperlinks, and images) into a MySQL database for persistent storage.
- **Dynamic File Naming**: Automatically generate output filenames based on the input file's name and format.
- **Environment Configuration**: Utilize a `.env` file for easy configuration of environment variables, including database connection settings.

## Requirements

- Python 3.x
- Required libraries:
  - `PyPDF2`
  - `python-docx`
  - `python-pptx`
  - `pdf2image`
  - `Pillow`
  - `pytz`
  - `python-dotenv`
  - `mysql-connector-python`

You can install the required libraries using pip:

```bash
pip install PyPDF2 python-docx python-pptx pdf2image Pillow python-dotenv mysql-connector-python
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/data-extractor.git
    cd data-extractor
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory with the following structure:

    ```plaintext
    DATABASE_HOST=your_database_host
    DATABASE_USER=your_database_user
    DATABASE_PASSWORD=your_database_password
    DATABASE_NAME=your_database_name
    ```

## Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Provide the filepath in the terminal(3 testing files are present in the directory with name sample.pdf, sample.pptx, sample.docx)

3. The extracted data will be stored in the specified output folder and the configured database.
