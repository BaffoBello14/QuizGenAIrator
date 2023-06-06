from fpdf import FPDF
from question_class import Question
import tkinter as tk
from tkinter import filedialog
import os
import re
from langdetect import detect

def translate_bloom_levels(text):
    terms_en = ["Remembering", "Understanding", "Applying", "Analyzing", "Evaluating"]
    terms_it = ["Ricordare", "Comprendere", "Applicare", "Analizzare", "Valutare"]
    terms_es = ["Recordar", "Comprender", "Aplicar", "Analizar", "Evaluar"]
    terms_fr = ["Mémoriser", "Comprendre", "Appliquer", "Analyser", "Évaluer"]
    terms_de = ["Wissen", "Verstehen", "Anwenden", "Analysieren", "Evaluieren"]

    for term in text.split():

        term_language = detect(term)

        if term_language != 'en':
            index = -1
            if term in terms_it:
                index = terms_it.index(term)
            elif term in terms_es:
                index = terms_it.index(term)
            elif term in terms_fr:
                index = terms_it.index(term)
            elif term in terms_de:
                index = terms_it.index(term)
            if not index == -1:
                text = text.replace(term, terms_en[index])

    return text

def preprocess_question_lines(question_lines):
    pattern = r'^\d+\.'
    # if the complete question has less than 7 lines it is not actually a question
    if len(question_lines) < 7:
        return None
    # if the complete question has more than 7 lines
    # is necessary to remove any lines that precedes the question
    if len(question_lines) > 7:
        lines_to_remove = []
        for single_line in question_lines:
            if not re.match(pattern, single_line):
                lines_to_remove.append(single_line)
            else:
                break
        for line in lines_to_remove:
            question_lines.remove(line)
    # if the complete question still has more than 7 lines
    # is necessary to remove any lines that follow the question
    if len(question_lines) > 7:
        question_lines = question_lines[0:6]
    # to translate terms in Bloom line
    question_lines[6] = translate_bloom_levels(question_lines[6])

    return question_lines

class Quiz:
    def __init__(self, language, output_function):
        super().__init__()

        self.questions = []
        self.language = language
        self.output_function = output_function

        file_path = 'output/raw_quiz.txt'
        with open(file_path, encoding='utf-8') as file:
            content = file.read()

        # Split the content into individual questions
        question_texts = content.split('\n\n')

        # Process each question text
        for question_text in question_texts:
            question_lines = question_text.strip().split('\n')

            question_lines = preprocess_question_lines(question_lines)
            if question_lines is None:
                continue

            # Extract the question and answers
            question = question_lines[0][question_lines[0].index('. ') + 2:]
            answers = [line[2:] for line in question_lines[1:-2]]
            correct_answer = question_lines[-2][-1]
            level = question_lines[-1].split(": ")[-1].strip()

            # Add the question to the quiz object
            self.add_question(question, answers, correct_answer, level)

    def add_question(self, question, answers, correct_answer, level):
        new_question = Question(question, answers, correct_answer, level)
        self.questions.append(new_question)

    def get_language(self):
        return self.language

    def get_questions(self):
        return self.questions

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        else:
            return None

    def get_num_questions(self):
        return len(self.questions)

    def get_quiz_as_string(self):
        quiz_text = ""
        for i, question in enumerate(self.questions, start=1):
            quiz_text += f"Question {i}: {question.get_text()}\n"
            options = question.get_answers()
            for j, option in enumerate(options, start=1):
                quiz_text += f"{chr(64 + j)}. {option}\n"
            quiz_text += "\n"
        quiz_text = quiz_text.replace("’", "'")
        return quiz_text

    def get_complete_quiz_as_string(self):
        quiz_text = ""
        for i, question in enumerate(self.questions, start=1):
            quiz_text += f"Question {i}: {question.get_text()}\n"
            options = question.get_answers()
            for j, option in enumerate(options, start=1):
                quiz_text += f"{chr(64 + j)}. {option}\n"
            quiz_text += f"Correct answer: {question.get_correct_answer()}\n"
            quiz_text += f"Bloom taxonomy level: {question.get_level()}\n"
            quiz_text += f"Score: {question.get_score()}\n\n"
        quiz_text = quiz_text.replace("’", "'")
        return quiz_text

    def get_correct_answers_as_string(self):
        answers_text = ""
        for i, question in enumerate(self.questions, start=1):
            answers_text += f"Correct answer for question {i}: {question.get_correct_answer()}\n"
        return answers_text

    def print_num_questions_for_each_level(self, bloom_levels):
        count_questions_by_level = {}

        for level in bloom_levels:
            count = 0
            for question in self.questions:
                if question.get_level() == level:
                    count += 1
            count_questions_by_level[level] = count

        for level in bloom_levels:
            count = count_questions_by_level[level]
            self.output_function(f"Questions for level {level}: {count}")
        self.output_function()

    def select_questions(self, num_questions_level, bloom_levels):
        selected_questions_by_level = {}  # Dictionary to store selected questions for each level

        sorted_questions_by_level = {}  # Dictionary to store questions sorted by level

        # Sort questions by level
        for question in self.questions:
            level = question.get_level()
            if level not in sorted_questions_by_level:
                sorted_questions_by_level[level] = []
            sorted_questions_by_level[level].append(question)

        # Sort questions within each level by score in descending order
        for level, level_questions in sorted_questions_by_level.items():
            sorted_questions_by_level[level] = sorted(level_questions, key=lambda q: q.get_score(), reverse=True)

        unique_scores = []
        for level, level_questions in sorted_questions_by_level.items():
            indexes_to_remove = []
            index = 0
            for question in level_questions:
                if question.get_score() not in unique_scores:
                    unique_scores.append(question.get_score())
                else:
                    indexes_to_remove.append(index)
                index += 1
            for index_to_remove in indexes_to_remove:
                level_questions.pop(index_to_remove)

        # Select the specified number of questions for each level
        for level, level_questions in sorted_questions_by_level.items():
            num_questions = num_questions_level[bloom_levels.index(level)]  # Get the number of questions for the level
            selected_questions = level_questions[:num_questions]  # Select the top questions
            selected_questions_by_level[level] = selected_questions

        self.questions = []  # Clear the existing questions list

        # Populate self.questions with the selected questions
        for level, level_questions in selected_questions_by_level.items():
            for question in level_questions:
                self.questions.append(question)

    def generate_files(self):
        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        file_path = 'output/final_quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.get_complete_quiz_as_string())

        file_path = 'results/questions.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.get_quiz_as_string())

        file_path = 'results/answers.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.get_correct_answers_as_string())

        root = tk.Tk()
        root.withdraw()  # Hide the main window

        path = filedialog.askdirectory()
        if not path:
            path = "results"

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Set the font and size for the PDF
        pdf.set_font("Arial", size=12)

        # Write the content to the PDF
        pdf.multi_cell(0, 10, self.get_quiz_as_string(), 'UTF-8')

        # Save the PDF file
        pdf.output(path + '/questions.pdf', 'F')

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()

        # Set the font and size for the PDF
        pdf.set_font("Arial", size=12)

        # Write the content to the PDF
        pdf.multi_cell(0, 10, self.get_correct_answers_as_string(), 'UTF-8')

        # Save the PDF file
        pdf.output(path + '/answers.pdf', 'F')

        self.output_function("The multi-choice quiz has been successfully generated.")
