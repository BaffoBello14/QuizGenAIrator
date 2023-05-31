from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

# 5 livelli possibili (len(num_questions_leve) è 5)
language = "italiano"
'''while True:
    language = input('Choose the language: ')
    if language == "italiano" or language == "english" or language == "francoise":
        break'''

num_questions_level = [3, 2, 1, 4, 1]
bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]

print("num x level global", num_questions_level)

pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 5pag ita.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 10pag.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT.pdf')
# pdf_reader = PDFReader('pdf/file7.pdf')
pdf_reader.process_pdf()

quiz_generator = QuizGenerator(num_questions_level, bloom_levels, language)
quiz_generator.find_language()
# quiz_generator.generate()
# quiz_generator.refactor()

quiz = Quiz()
# quiz.print_correct_answers()

quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text())
# quiz_analyzer.extract_questions_keywords()
# quiz_analyzer.analyze_starting_text()
quiz_analyzer.compare_text_quiz()

# quiz.print_quiz()
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.select_questions(num_questions_level, bloom_levels)
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.print_quiz()
