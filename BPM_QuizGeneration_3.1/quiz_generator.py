import math
import time
import openai
import tiktoken

openai.api_key = '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'

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        # print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


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

        file_path = 'input/refactor_query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.refactor_query = file_contents

        self.model_id = 'gpt-3.5-turbo'

    def get_starting_text(self):
        return self.text

    def generate(self):

        file_path = 'results/quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("")

        limit_len = 10000
        overlap_value = math.floor(limit_len/2)
        lower_index = 0
        upper_index = limit_len
        text_partitions = []
        num_partitions = math.floor(len(self.text)/overlap_value)

        for i in range(num_partitions):
            text_partitions.append(self.text[lower_index:upper_index])
            lower_index = lower_index + overlap_value
            upper_index = upper_index + overlap_value
        if len(self.text[lower_index:]) > 0:
            text_partitions.append(self.text[lower_index:])
            num_partitions = num_partitions + 1

        # the overlap is now represented by half partition
        print("Text divided in", num_partitions, " overlapped partitions")

        for partition in text_partitions:

            conversation = []
            prompt = partition + " " + self.query
            conversation.append({'role': 'user', 'content': prompt})
            print("TOKENS BEFORE RESPONSE", num_tokens_from_messages(conversation, self.model_id))

            response = openai.ChatCompletion.create(
                model=self.model_id,
                messages=conversation
            )
            conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

            print("\tTOKENS WITH RESPONSE", num_tokens_from_messages(conversation, self.model_id))

            file_path = 'results/quiz.txt'
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(conversation[-1]['content'].strip())
                file.write("\n\n")

            time.sleep(20)

        self.refactor()

    def refactor(self):

        file_path = 'results/quiz.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        raw_quiz = file_contents

        conversation = []
        prompt = raw_quiz + " " + self.refactor_query
        conversation.append({'role': 'user', 'content': prompt})
        print("(Refactoring) TOKENS BEFORE RESPONSE", num_tokens_from_messages(conversation, self.model_id))

        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation
        )
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        print("\tTOKENS WITH RESPONSE", num_tokens_from_messages(conversation, self.model_id))

        file_path = 'results/quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(conversation[-1]['content'].strip())

# partizionamento sovrapposto?

# estrarre x domande da ogni partizione
# eventualmente implementare una classe TextCleaner per rimuovere sommario o altre robe
# usare gpt per fare la append di domande mantentento la numerazione
# usare gpt per rimuovere dal quiz globale eventuali risposte simili
# e formattare nuovamente il testo delle domande (rimuovere eventuali righe vuote ecc...)
