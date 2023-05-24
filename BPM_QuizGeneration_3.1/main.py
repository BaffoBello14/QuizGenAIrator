from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 5pag.pdf')
#pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 10pag.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT.pdf')
# pdf_reader = PDFReader('pdf/file7.pdf')
pdf_reader.process_pdf()

quiz_generator = QuizGenerator()
quiz_generator.generate()

quiz = Quiz()
# quiz.print_quiz()
# quiz.print_correct_answers()

quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text())
# quiz_analyzer.extract_questions_keywords()
# quiz_analyzer.analyze_starting_text()
# quiz_analyzer.compare_text_quiz()
