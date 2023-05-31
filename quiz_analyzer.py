import spacy

class QuizAnalyzer:
    def __init__(self, quiz, text, language):
        super().__init__()

        self.nlp = self.load_spacy_model(language)
        self.quiz = quiz
        self.text = text
        self.dictionary = self.load_enchant_dictionary(language)

    def load_spacy_model(self, language):
        if language == "english":
            return spacy.load("en_core_web_trf")
        elif language == "italian":
            return spacy.load("it_core_news_lg")
        elif language == "french":
            return spacy.load("fr_dep_news_trf")

    def extract_questions_keywords(self):
        for i in range(self.quiz.get_num_questions()):
            doc = self.nlp(self.quiz.get_question(i).get_text())
            text_entities = doc.ents

            keywords = []
            for chunk in doc.noun_chunks:
                if chunk.root.pos_ == "NOUN":
                    keywords.append(chunk.text)

            print(self.quiz.get_question(i).get_text())
            print(keywords)
            print(text_entities)
        print()

    def analyze_starting_text(self):
        text_doc = self.nlp(self.text)

        text_entities = text_doc.ents
        print("Text Named Entities")
        print(text_entities)

        text_keywords = [token.text for token in text_doc if not token.is_stop and token.is_alpha]
        print("Text Keywords")
        print(text_keywords)

        text_keywords = [token.text for token in text_doc if not token.is_stop and token.is_alpha and self.dictionary.check(token.text)]
        print("Filtered Text Keywords")
        print(text_keywords)

    def compare_text_quiz(self):
        text_doc = self.nlp(self.text)

        for i in range(self.quiz.get_num_questions()):
            question_text = self.quiz.get_question(i).get_text()
            question_doc = self.nlp(question_text)
            similarity_score = text_doc.similarity(question_doc)
            # print("Question:", question_text)
            # print("Similarity Score:", similarity_score)

            self.quiz.get_question(i).set_score(similarity_score)

            for j in range(self.quiz.get_question(i).get_num_answers()):
                answer_text = self.quiz.get_question(i).get_answer(j)
                answer_doc = self.nlp(answer_text)

                similarity_score = text_doc.similarity(answer_doc)
                # print("\tAnswer:", answer_text)
                # print("\tSimilarity Score:", similarity_score)

            # print(self.quiz.get_question(i).get_correct_answer(), self.quiz.get_question(i).get_correct_answer_text())
            # print()
