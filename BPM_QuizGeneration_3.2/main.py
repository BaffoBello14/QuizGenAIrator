from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

# 5 livelli possibili (len(num_questions_leve) è 5)
num_questions_level = [3, 2, 0, 4, 1]

pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 5pag.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 10pag.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT.pdf')
# pdf_reader = PDFReader('pdf/file7.pdf')
pdf_reader.process_pdf()

quiz_generator = QuizGenerator(num_questions_level)
quiz_generator.generate()

quiz = Quiz()
# quiz.print_quiz()
# quiz.print_correct_answers()

quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text())
# quiz_analyzer.extract_questions_keywords()
# quiz_analyzer.analyze_starting_text()
# quiz_analyzer.compare_text_quiz()
