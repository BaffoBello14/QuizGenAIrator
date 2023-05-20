
class Question:
    def __init__(self, question_text):
        super().__init__()

        self.text = question_text
        self.op



    def generate(self,i):
    #def generate(self):
        conversation = []

        prompt = self.text + " " + self.query
        conversation.append({'role': 'user', 'content': prompt})

        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation
        )
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        file_path = 'D:/ProgettoBPM/BPM/BPM_QuizGeneration_1.0/results/quiz'+str(i)+'.txt'
        #file_path = 'results/quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(conversation[-1]['content'].strip())
