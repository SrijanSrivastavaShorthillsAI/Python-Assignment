import os
from PIL import Image
import mysql.connector
import json

class SQLStorage:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def create_table_if_not_exists(self):
        # Creating a table for text data, hyperlinks, and images
        create_text_table_query = """
        CREATE TABLE IF NOT EXISTS extracted_text (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name TEXT NOT NULL,
            page_number INT,
            text TEXT,
            headings TEXT,
            font_styles TEXT
        );
        """
        create_links_table_query = """
        CREATE TABLE IF NOT EXISTS extracted_links (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name TEXT NOT NULL,
            page_number INT,
            linked_text TEXT,
            url TEXT
        );
        """
        create_images_table_query = """
        CREATE TABLE IF NOT EXISTS extracted_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            file_name TEXT NOT NULL,
            image_path TEXT NOT NULL,
            image_resolution VARCHAR(20),  
            image_size BIGINT
        );
        """
        # Execute the table creation queries
        self.cursor.execute(create_text_table_query)
        self.cursor.execute(create_links_table_query)
        self.cursor.execute(create_images_table_query)
        self.connection.commit()

    def insert_data(self, file_name, page_number, text, headings, font_styles):
            # Ensure that lists or dictionaries are converted to JSON strings before insertion
            if isinstance(text, (list, dict)):
                text = json.dumps(text)  # Convert list or dict to JSON string
            if isinstance(headings, (list, dict)):
                headings = json.dumps(headings)  # Convert list or dict to JSON string
            if isinstance(font_styles, (list, dict)):
                font_styles = json.dumps(font_styles)  # Convert list or dict to JSON string

            query = """
            INSERT INTO extracted_text (file_name, page_number, text, headings, font_styles)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (file_name, page_number, text, headings, font_styles))
            self.connection.commit()

    def insert_link(self, file_name, page_number, linked_text, url):
        query = """
        INSERT INTO extracted_links (file_name, page_number, linked_text, url)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (file_name, page_number, linked_text, url))
        self.connection.commit()

    def insert_image(self, file_name, image_path):
            # Open the image and get its resolution
            with Image.open(image_path) as img:
                width, height = img.size  # Get image width and height
                resolution = f"{width} x {height}"  # Format resolution as 'a x b'

            # Get the file size in bytes
            image_size = os.path.getsize(image_path)

            # Insert the image data along with resolution and size into the database
            query = """
            INSERT INTO extracted_images (file_name, image_path, image_resolution, image_size)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (file_name, image_path, resolution, image_size))
            self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()
