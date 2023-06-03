from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader

# declaration of the Revised Bloom's Taxonomy levels
bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]

# input of the number of questions desired for each Bloom's level
num_questions_level = []
for i in range(len(bloom_levels)):
    message = str(bloom_levels[i]) + " questions: "
    num_questions_level.append(int(input(message)))

# PDFReader object declaration passing to it the pdf from which extract the text
pdf_reader = PDFReader('pdf/file0.pdf')
pdf_reader.process_pdf()

# QuizGenerator object declaration passing to it the number of questions for each level and the Bloom's levels
quiz_generator = QuizGenerator(num_questions_level, bloom_levels)
quiz_generator.generate()

# Quiz object declaration passing to it the language in which the quiz is written
quiz = Quiz(quiz_generator.get_language())

# QuizAnalyzer declaration passing to it the generated quiz and the starting text
quiz_analyzer = QuizAnalyzer(quiz, quiz_generator.get_starting_text())
quiz_analyzer.calculate_weighted_standing()

# selection of desired number of questions for each level from the quiz (selecting the best ones)
quiz.select_questions(num_questions_level, bloom_levels)
quiz.generate_files()
