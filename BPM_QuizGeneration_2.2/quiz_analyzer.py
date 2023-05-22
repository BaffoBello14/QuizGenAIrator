import spacy
import enchant

class QuizAnalyzer:
    def __init__(self, quiz, text):
        super().__init__()

        self.nlp = spacy.load("en_core_web_lg")
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

        # Load the dictionary
        dictionary = enchant.Dict("en_US")  # Replace "en_US" with the appropriate language code for your dictionary
        # Keywords: Identify keywords or important terms
        text_keywords = [token.text for token in text_doc if
                         not token.is_stop and token.is_alpha and dictionary.check(token.text)]
        print("Filtered Text Keywords")
        print(text_keywords)

    def compare_text_quiz(self):
        # Implementa una logica di confronto testo-quiz
        text_doc = self.nlp(self.text)

        for i in range(self.quiz.get_num_questions()):

            question_text = self.quiz.get_question(i).get_text()
            question_doc = self.nlp(question_text)

            if len(question_doc) > 0 and len(text_doc) > 0:
                similarity_score = text_doc.similarity(question_doc)
            else:
                similarity_score = 0.0  # Assegna uno score di similarità basso o nullo in caso di documenti vuoti o senza parole valide

            print("Question:", question_text)
            print("Similarity Score:", similarity_score)

            for j in range(self.quiz.get_question(i).get_num_answers()):

                answer_text = self.quiz.get_question(i).get_answer(j)
                answer_doc = self.nlp(answer_text)

                if len(answer_doc) > 0 and len(text_doc) > 0:
                    similarity_score = text_doc.similarity(answer_doc)
                else:
                    similarity_score = 0.0  # Assegna uno score di similarità basso o nullo in caso di documenti vuoti o senza parole valide

                print("\tAnswer:", answer_text)
                print("\tSimilarity Score:", similarity_score)

            print(self.quiz.get_question(i).get_correct_answer(), self.quiz.get_question(i).get_correct_answer_text())
            print()
