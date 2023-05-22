import spacy

class QuizAnalyzer:
    def __init__(self, quiz, text):
        super().__init__()
        self.nlp = spacy.load("en_core_web_lg")  # Utilizzo di un modello più specifico
        self.quiz = quiz
        self.text = text

    def extract_questions_keywords(self):
        for i in range(self.quiz.get_num_questions()):
            question_text = self.quiz.get_question(i).get_text()
            # Process the question text with spaCy
            doc = self.nlp(question_text)

            question_entities = doc.ents

            # Extract the keywords
            keywords = []
            for chunk in doc.noun_chunks:
                if chunk.root.pos_ == "NOUN":
                    keywords.append(chunk.text)

            # Print the question, keywords, and entities
            print(question_text)
            print("Keywords:", keywords)
            print("Entities:", question_entities)
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

    def compare_text_quiz(self):
        # Implementa una logica di confronto testo-quiz
        text_doc = self.nlp(self.text)

        for i in range(self.quiz.get_num_questions()):
            question_text = self.quiz.get_question(i).get_text()
            question_doc = self.nlp(question_text)

            similarity_score = text_doc.similarity(question_doc)  # Calcola la similarità del coseno
            print("Question:", question_text)
            print("Similarity Score:", similarity_score)
            print()

