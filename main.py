from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

num_questions_level = []
bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]
for i in range(len(bloom_levels)):
    message = str(bloom_levels[i]) + " questions: "
    num_questions_level.append(int(input(message)))

print("num x level global", num_questions_level)

# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 5pag ita.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT 10pag.pdf')
# pdf_reader = PDFReader('pdf/Modulo 2.1 - IoT.pdf')
pdf_reader = PDFReader('pdf/file2.pdf')
pdf_reader.process_pdf()

quiz_generator = QuizGenerator(num_questions_level, bloom_levels)
quiz_generator.generate()

quiz = Quiz(quiz_generator.get_language())

quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text())
quiz_analyzer.calculate_weighted_standing()

# quiz.print_quiz()
# quiz.print_correct_answers()
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.select_questions(num_questions_level, bloom_levels)
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.print_complete_quiz()
