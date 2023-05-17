import openai

def generate_questions(text):
    prompt = f"Generate multiple-choice questions based on the following text:\n\n{text}\n\n---\n\nQuestion:"

    # Generate questions using the OpenAI Codex model
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=64,
        n=5,  # Number of questions to generate
        stop=None,
        temperature=0.6,  # Controls the randomness of the generated questions
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Process the generated questions
    questions = []
    for choice in response.choices:
        question = choice.text.strip().replace("Question:", "").strip()
        questions.append(question)

    return questions


def generate_answers(questions):
    answers = []

    # Generate answers for each question
    for question in questions:
        prompt = f"Question: {question}\nAnswer:"

        # Generate an answer using the OpenAI Playground API
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose the appropriate engine
            prompt=prompt,
            max_tokens=16,
            n=1,
            stop=None,
            temperature=0.3,  # Controls the randomness of the generated answers
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        answer = response.choices[0].text.strip().replace("Answer:", "").strip()
        answers.append(answer)

    return answers


# Main program
text = "Your plain text goes here."  # Provide your plain text here

questions = generate_questions(text)
answers = generate_answers(questions)

# Print the generated questions and answers
for i in range(len(questions)):
    print(f"Question {i + 1}: {questions[i]}")
    print(f"Answer {i + 1}: {answers[i]}")
    print()
