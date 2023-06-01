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
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
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
    def __init__(self, num_questions_level, bloom_levels):
        super().__init__()

        file_path = 'input/extracted_plain_text.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.text = file_contents

        file_path = 'input/main_query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.query = file_contents

        file_path = 'input/level_query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.level_query = file_contents

        file_path = 'input/language_query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.language_query = file_contents

        file_path = 'input/refactor_query.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        self.refactor_query = file_contents

        self.num_questions_level = num_questions_level
        self.bloom_levels = bloom_levels
        self.model_id = 'gpt-3.5-turbo'
        self.language = ""
        self.find_language()

    def get_language(self):
        return self.language

    def get_starting_text(self):
        return self.text

    def find_language(self):
        conversation = []  # List to store the conversation messages

        prompt = self.text[:500] + " " + self.language_query + " "  # Create the prompt for language identification
        conversation.append({'role': 'user', 'content': prompt})  # Add the user message with the prompt

        # Call the Chat API to get the AI response
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation
        )

        # Append the AI response to the conversation
        conversation.append(
            {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

        # Extract the identified language from the conversation and update self.language
        self.language = conversation[-1]['content'].strip()

        # Check if the identified language is supported
        if self.language not in ["english", "french", "italian", "spanish", "german"]:
            print(self.language + " is not supported!!!")
            exit()

    def generate(self):
        file_path = 'output/raw_quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("")

        limit_len = 11000
        overlap_value = math.floor(limit_len / 2)
        lower_index = 0
        upper_index = limit_len
        text_partitions = []
        num_partitions = math.floor(len(self.text) / overlap_value)

        # Divide the text into overlapping partitions
        for i in range(num_partitions):
            text_partitions.append(self.text[lower_index:upper_index])
            lower_index = lower_index + overlap_value
            upper_index = upper_index + overlap_value
        if len(self.text[lower_index:]) > 0:
            text_partitions.append(self.text[lower_index:])
            num_partitions = num_partitions + 1

        # Print the number of partitions created
        print("Text divided into", num_partitions, "overlapped partitions")

        num_questions_level_partition = []
        tot_questions = 0

        # Calculate the total number of questions needed for the given number of partitions
        for i in range(len(self.num_questions_level)):
            tot_questions += math.ceil(self.num_questions_level[i] / num_partitions)

        temp_query = "Generate " + str(tot_questions) + " questions classified by the Revised Bloom's Taxonomy:"

        # Determine the number of questions for each level in each partition and update the temp_query
        for i in range(len(self.num_questions_level)):
            num_questions_level_partition.append(math.ceil(self.num_questions_level[i] / num_partitions))
            temp_query = temp_query + " " + str(num_questions_level_partition[i]) \
                         + " questions must be of level " + self.bloom_levels[i]
            if i == (len(self.num_questions_level) - 1):
                temp_query = temp_query + ". The language of the quiz must be: " + self.language
                break
            temp_query = temp_query + ","

        # Generate questions for each partition
        for partition in text_partitions:
            response_is_ok = False
            content = ""

            while not response_is_ok:
                conversation = []

                prompt = temp_query + " " + self.query + " " + partition
                conversation.append({'role': 'user', 'content': prompt})
                print("TOKENS BEFORE RESPONSE", num_tokens_from_messages(conversation, self.model_id))

                # Call the Chat API to get the AI response
                response = openai.ChatCompletion.create(
                    model=self.model_id,
                    messages=conversation
                )

                conversation.append(
                    {'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
                print("\tTOKENS WITH RESPONSE", num_tokens_from_messages(conversation, self.model_id))

                for j in range(len(self.num_questions_level)):
                    content = conversation[-1]['content'].strip()
                    num_occurrences = content.count(self.bloom_levels[j])
                    if num_occurrences != num_questions_level_partition[j]:
                        response_is_ok = False
                        break
                    else:
                        response_is_ok = True

                if not response_is_ok:
                    print("\t\tWrong number of questions for levels!!!")
                    time.sleep(20)

            time.sleep(20)

            # Write the generated content to the output file
            file_path = 'output/raw_quiz.txt'
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(content)
                file.write("\n\n")

        self.refactor(num_partitions, num_questions_level_partition)

    def refactor(self, num_partitions, num_questions_level_partition):
        # Read the contents of the raw_quiz.txt file
        file_path = 'output/raw_quiz.txt'
        with open(file_path, encoding='utf-8') as file:
            file_contents = file.read()
        raw_quiz = file_contents

        # Calculate the total number of questions needed for refactoring
        tot_questions = 0
        for value in num_questions_level_partition:
            tot_questions += value
        tot_questions *= num_partitions

        print("tot_questions", tot_questions)

        # Create a prompt for the refactoring step
        conversation = []
        prompt = raw_quiz + " " + self.refactor_query + " " + str(tot_questions) + "."
        conversation.append({'role': 'user', 'content': prompt})
        print("(Refactoring) TOKENS BEFORE RESPONSE", num_tokens_from_messages(conversation, self.model_id))

        # Query the AI model for refactoring the quiz
        response = openai.ChatCompletion.create(
            model=self.model_id,
            messages=conversation
        )
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
        print("\tTOKENS WITH RESPONSE", num_tokens_from_messages(conversation, self.model_id))

        # Write the refactored quiz content to the refactored_quiz.txt file
        file_path = 'output/refactored_quiz.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(conversation[-1]['content'].strip())

