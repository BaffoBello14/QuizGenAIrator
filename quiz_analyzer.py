import spacy
import enchant


class QuizAnalyzer:
    def __init__(self, quiz, text):
        super().__init__()

        self.quiz = quiz
        language = quiz.get_language()
        # if (language) cambiare libreria
        self.nlp = spacy.load("it_core_news_lg")

        self.text = text

        # Define weights for similarity, coherence, and clarity
        self.similarity_weight = 0.6
        self.coherence_weight = 0.3
        self.clarity_weight = 0.1

    def compare_text_quiz(self):
        # Implementa una logica di confronto testo-quiz
        text_doc = self.nlp(self.text)

        for i in range(self.quiz.get_num_questions()):

            question_text = self.quiz.get_question(i).get_text()
            question_doc = self.nlp(question_text)
            similarity_score = text_doc.similarity(question_doc)  # Calcola la similarità del coseno
            # print("Question:", question_text)
            # print("Similarity Score:", similarity_score)

            self.quiz.get_question(i).set_score(similarity_score)

            for j in range(self.quiz.get_question(i).get_num_answers()):
                answer_text = self.quiz.get_question(i).get_answer(j)
                answer_doc = self.nlp(answer_text)

                similarity_score = text_doc.similarity(answer_doc)  # Calcola la similarità del coseno
                # print("\tAnswer:", answer_text)
                # print("\tSimilarity Score:", similarity_score)

            # print(self.quiz.get_question(i).get_correct_answer(), self.quiz.get_question(i).get_correct_answer_text())
            # print()

    def calculate_weighted_standing(self):

        for question in self.quiz.get_questions():

            # TEXT <-> QUESTION + ANSWERS
            # Combine the question and options into a single string
            question_text = question.get_text() + ' '.join(question.get_answers())
            # Process the combined text using NLP
            doc_combined = self.nlp(question_text)
            # Calculate the similarity between the combined text and the text
            similarity_score = doc_combined.similarity(self.nlp(self.text))

            # ANSWERS <-> QUESTION
            # Combine the question and options into a single string
            answers_text = ' '.join(question.get_answers())
            # Process the combined text using NLP
            doc_combined = self.nlp(answers_text)
            # Calculate the similarity between the combined text and the text
            coherence_score = doc_combined.similarity(self.nlp(question.get_text()))

            # Process the question using NLP
            doc_question = self.nlp(question.get_text())

            # Calculate the average token vector similarity within the question
            token_similarities = []
            for token in doc_question:
                token_similarity = token.similarity(doc_question)
                token_similarities.append(token_similarity)

            clarity_score = sum(token_similarities) / len(token_similarities)

            # Calculate the weighted standing
            weighted_standing = self.similarity_weight * similarity_score + self.coherence_weight * coherence_score \
                                + self.clarity_weight * clarity_score

            question.set_score(weighted_standing)

            print(question.get_text())
            print("\tsimilarity_score: ", similarity_score)
            print("\tcoherence_score: ", coherence_score)
            print("\tclarity_score", clarity_score)
