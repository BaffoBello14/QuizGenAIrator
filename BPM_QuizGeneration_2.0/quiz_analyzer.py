import spacy


class QuizAnalyzer:
    def __init__(self, quiz):
        super().__init__()

        self.nlp = spacy.load("en_core_web_sm")
        self.quiz = quiz

    def extract_questions_keywords(self):

        for i in range(self.quiz.get_num_questions()):
            # Process the text with spaCy
            doc = self.nlp(self.quiz.get_question(i).get_text())

            # Extract the keywords
            keywords = []
            for chunk in doc.noun_chunks:
                if chunk.root.pos_ == "NOUN":
                    keywords.append(chunk.text)

            # Print the keywords
            print(self.quiz.get_question(i).get_text())
            print(keywords)
