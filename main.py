from quiz_analyzer import QuizAnalyzer
from quiz_class import Quiz
from quiz_generator import QuizGenerator
from pdf_reader import PDFReader
from tkinter import filedialog

# declaration of the Revised Bloom's Taxonomy levels
bloom_levels = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]

print("Considering the Revised Bloom's Taxonomy levels", bloom_levels, "for questions.")
print("Specify how many questions you want for each level in the multi choice quiz.")

# input of the number of questions desired for each Bloom's level
num_questions_level = []
for i in range(len(bloom_levels)):
    num_question = -1
    while num_question < 0:
        message = str(bloom_levels[i]) + " questions: "
        num_question = int(input(message))
        if num_question >= 0:
            num_questions_level.append(num_question)
print()

# PDFReader object declaration passing to it the pdf from which extract the text
file_path = filedialog.askopenfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
if not file_path:
    exit()

pdf_reader = PDFReader(file_path)
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
print("Number of available questions for each Revised Bloom's Taxonomy level, before the selection.")
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.select_questions(num_questions_level, bloom_levels)
print("Number of questions for each Revised Bloom's Taxonomy level for the final quiz.")
quiz.print_num_questions_for_each_level(bloom_levels)
quiz.generate_files()
