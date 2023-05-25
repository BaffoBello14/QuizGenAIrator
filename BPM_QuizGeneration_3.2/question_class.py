
class Question:
    def __init__(self, question, answers, correct_answer):
        super().__init__()

        self.text = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.level = 0  # tbd

    def get_text(self):
        return self.text

    def get_answers(self):
        return self.answers

    def get_correct_answer(self):
        return self.correct_answer

    def get_num_answers(self):
        return len(self.answers)

    def get_answer(self, index):
        if 0 <= index < len(self.answers):
            return self.answers[index]
        else:
            return None

    def get_correct_answer_text(self):
        index = ord(self.get_correct_answer().upper()) - ord('A')
        if 0 <= index < len(self.answers):
            return self.answers[index]
        else:
            return None
