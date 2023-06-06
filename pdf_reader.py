import PyPDF2
import re

class PDFReader:
    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path

    def process_pdf(self):
        # Open the PDF file in binary mode
        with open(self.file_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # Initialize an empty string to store the extracted text
            text = ''

            # Iterate over each page in the PDF
            for page in pdf_reader.pages:
                # Extract the text from the page and append it to the 'text' variable
                text += page.extract_text()

            # Remove consecutive multiple spaces
            text = re.sub(r'\s+', ' ', text)

            # Remove leading and trailing spaces
            text = text.strip()

            # Remove line breaks
            text = text.replace('\n', '')

            # Remove empty lines
            lines = text.split('\n')
            lines = [line for line in lines if line.strip() != '']
            text = '\n'.join(lines)

            # Remove non-printable characters
            text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)

            # Define the path to save the extracted plain text
            file_path = 'input/extracted_plain_text.txt'

            # Write the extracted text to a file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
