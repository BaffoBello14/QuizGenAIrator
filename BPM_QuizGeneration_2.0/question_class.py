
class Question:
    def __init__(self, question, answers, correct_answer):
        super().__init__()

        self.text = question
        self.answers = answers
        self.correct_answer = correct_answer

    def get_text(self):
        return self.text

    def get_answers(self):
        return self.answers

    def get_correct_answer(self):
        return self.correct_answer
