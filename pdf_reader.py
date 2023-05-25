import PyPDF2
import re


class PDFReader:
    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path

    def process_pdf(self):
        with open(self.file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Rimuovi spazi multipli consecutivi
            text = re.sub(r'\s+', ' ', text)
            # Rimuovi spazi iniziali e finali
            text = text.strip()
            # Rimuovi i ritorni a capo
            text = text.replace('\n', '')
            # Rimuovi le righe vuote
            lines = text.split('\n')
            lines = [line for line in lines if line.strip() != '']
            text = '\n'.join(lines)
            # Rimuovi i caratteri non stampabili
            text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F-\x9F]', '', text)

            file_path = 'input/text.txt'
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
