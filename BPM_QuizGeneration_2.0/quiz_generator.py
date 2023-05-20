import openai

openai.api_key = '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'


class QuizGenerator:
    def __init__(self):
        super().__init__()

        file_path = 'input/text.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.text = file_contents

        file_path = 'input/query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.query = file_contents

        self.model_id = 'gpt-3.5-turbo'

    #def generate(self,i):
    def generate(self):
        conversation = []

        prompt = self.text + " " + self.query
        conversation.append({'role': 'user', 'content': prompt})

        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation
        )
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        #file_path = 'results/quiz'+str(i)+'.txt'
        file_path = 'results/quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(conversation[-1]['content'].strip())
