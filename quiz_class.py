from question_class import Question


class Quiz:
    def __init__(self):
        super().__init__()

        self.questions = []

        file_path = 'results/quiz.txt'
        with open(file_path, encoding='utf-8') as file:
            content = file.read()

        # Split the content into individual questions
        question_texts = content.split('\n\n')

        # Process each question text
        for question_text in question_texts:
            question_lines = question_text.strip().split('\n')

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

    def get_question(self, index):
        if 0 <= index < len(self.questions):
            return self.questions[index]
        else:
            return None

    def print_quiz(self):
        for i, question in enumerate(self.questions, start=1):
            print(f"Question {i}:", question.get_text())
            options = question.get_answers()
            for j, option in enumerate(options, start=1):
                print(f"{chr(64 + j)}. {option}")
            print(f"Bloom taxonomy level:", question.get_level())  # to remove
            print(f"Score:", question.get_score())  # to remove
            print()

    def print_correct_answers(self):
        for i, question in enumerate(self.questions, start=1):
            print(f"Correct answer for question {i}:", question.get_correct_answer())
        print()

    def get_num_questions(self):
        return len(self.questions)


