import spacy

class QuizAnalyzer:
    def __init__(self, quiz, text, output_function):
        super().__init__()

        self.quiz = quiz
        self.output_function = output_function

        language = quiz.get_language()
        if language == "english":
            if not spacy.util.is_package("en_core_web_lg"):
                self.output_function("English package is not installed!")
                self.output_function("Downloading English language package in progress...")
                spacy.cli.download("en_core_web_lg")
                self.output_function("Package installed")
            self.nlp = spacy.load("en_core_web_lg")
        elif language == "italian":
            if not spacy.util.is_package("it_core_news_lg"):
                self.output_function("Italian package is not installed!")
                self.output_function("Downloading Italian language package in progress...")
                spacy.cli.download("it_core_news_lg")
                self.output_function("Package installed")
            self.nlp = spacy.load("it_core_news_lg")
        elif language == "french":
            if not spacy.util.is_package("fr_core_news_lg"):
                self.output_function("French package is not installed!")
                self.output_function("Downloading French language package in progress...")
                spacy.cli.download("fr_core_news_lg")
                self.output_function("Package installed")
            self.nlp = spacy.load("fr_core_news_lg")
        elif language == "spanish":
            if not spacy.util.is_package("es_core_news_lg"):
                self.output_function("Spanish package is not installed!")
                self.output_function("Downloading Spanish language package in progress...")
                spacy.cli.download("es_core_news_lg")
                self.output_function("Package installed")
            self.nlp = spacy.load("es_core_news_lg")
        elif language == "german":
            if not spacy.util.is_package("de_core_news_lg"):
                self.output_function("German package is not installed!")
                self.output_function("Downloading German language package in progress...")
                spacy.cli.download("de_core_news_lg")
                self.output_function("Package installed")
            self.nlp = spacy.load("de_core_news_lg")

        self.text = text

        # Define weights for similarity, coherence, and clarity
        self.similarity_weight = 0.6    # for the comparison: TEXT <-> QUESTION + ANSWERS
        self.coherence_weight = 0.3     # for the comparison: ANSWERS <-> QUESTION
        self.clarity_weight = 0.1       # for the comparison based on tokens

    def calculate_weighted_standing(self):
        counter = 1
        for question in self.quiz.get_questions():
            self.output_function("Evaluating question " + str(counter) + " of " + str(len(self.quiz.get_questions())))
            counter += 1
            # comparison: TEXT <-> QUESTION + ANSWERS
            # Combine the question and options into a single string
            question_text = question.get_text() + ' '.join(question.get_answers())
            # Process the combined text using NLP
            doc_combined = self.nlp(question_text)
            # Calculate the similarity between the combined text and the text
            similarity_score = doc_combined.similarity(self.nlp(self.text))
            # comparison: ANSWERS <-> QUESTION
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
            weighted_standing = self.similarity_weight * similarity_score \
                                + self.coherence_weight * coherence_score \
                                + self.clarity_weight * clarity_score

            # setting the score on the question
            question.set_score(weighted_standing)
