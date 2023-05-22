import spacy


class QuizAnalyzer:
    def __init__(self, quiz, text):
        super().__init__()

        self.nlp = spacy.load("en_core_web_sm")
        self.quiz = quiz
        self.text = text

    def extract_questions_keywords(self):

        for i in range(self.quiz.get_num_questions()):
            # Process the text with spaCy
            doc = self.nlp(self.quiz.get_question(i).get_text())

            text_entities = doc.ents

            # Extract the keywords
            keywords = []
            for chunk in doc.noun_chunks:
                if chunk.root.pos_ == "NOUN":
                    keywords.append(chunk.text)

            # Print the keywords
            print(self.quiz.get_question(i).get_text())
            print(keywords)
            print(text_entities)
        print()

    def analyze_starting_text(self):

        text_doc = self.nlp(self.text)

        # Named Entities: Extract named entities (people, organizations, locations, etc.)
        text_entities = text_doc.ents
        print("Text Named Entities")
        print(text_entities)

        # Keywords: Identify keywords or important terms
        text_keywords = [token.text for token in text_doc if not token.is_stop and token.is_alpha]
        print("Text Keywords")
        print(text_keywords)
        print()
