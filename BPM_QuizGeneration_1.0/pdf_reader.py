import PyPDF2


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

            if len(text) > 4096:
                text = text[:4096]  # Taglia il testo se supera il limite consentito

            file_path = 'D:/ProgettoBPM/BPM/BPM_QuizGeneration_1.0/input/text.txt'
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text)
