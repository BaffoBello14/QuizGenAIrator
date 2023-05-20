from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

pdf_reader = PDFReader('D:/ProgettoBPM/BPM/BPM_QuizGeneration_1.0/pdf/file8.pdf')
pdf_reader.process_pdf()

#quiz_generator = QuizGenerator()
#quiz_generator.generate()

for i in range(1):
    quiz_generator = QuizGenerator()
    quiz_generator.generate(i)
