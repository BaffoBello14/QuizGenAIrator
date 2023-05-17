import openai
import re

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY_HERE"

# Define the prompt
prompt = "Given the following text, generate 5 multiple-choice questions and answers: The Mona Lisa is a half-length portrait painting by Italian artist Leonardo da Vinci. It is considered an archetypal masterpiece of the Italian Renaissance, and has been described as the best known, the most visited, the most written about, the most sung about, and the most parodied work of art in the world."

# Define the completion parameters
model = ""
temperature = 0.5
max_tokens = 2048
stop_sequence = "\n\n"
n_questions = 5

# Generate the questions and answers
response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    max_tokens=max_tokens,
    temperature=temperature,
    n=n_questions,
    stop=stop_sequence
)

# Extract the questions and answers from the response
questions = []
answers = []
for choice in response.choices:
    text = choice.text
    match = re.match(r"Q: (.*)\nA: (.*)\nB: (.*)\nC: (.*)\nD: (.*)", text)
    if match:
        q, a, b, c, d = match.groups()
        questions.append(q)
        answers.append([a, b, c, d])

# Print the questions and answers
for i, q in enumerate(questions):
    print(f"Question {i+1}: {q}")
    print(f"A. {answers[i][0]}")
    print(f"B. {answers[i][1]}")
    print(f"C. {answers[i][2]}")
    print(f"D. {answers[i][3]}\n")
