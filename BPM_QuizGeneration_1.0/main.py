from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

pdf_reader = PDFReader('pdf/file7.pdf')
pdf_reader.process_pdf()

quiz_generator = QuizGenerator()
quiz_generator.generate()

#for i in range(5):
    #quiz_generator = QuizGenerator()
    #quiz_generator.generate(i)
