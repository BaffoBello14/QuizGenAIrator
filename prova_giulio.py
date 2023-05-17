import openai

# Imposta la tua chiave API di OpenAI
openai.api_key = 'LA_TUA_CHIAVE_API'

def create_quiz(text):
    # Chiamata all'API di OpenAI per generare domande sul testo di input
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=100,
        n=5,
        stop=None,
        temperature=0.6,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Estrai le domande dalla risposta dell'API
    questions = [choice['text'].strip() for choice in response.choices]

    # Crea il formato del quiz a risposta multipla
    quiz = []
    for i, question in enumerate(questions):
        options = [
            {'text': 'Risposta corretta', 'correct': True},
            {'text': 'Risposta errata 1', 'correct': False},
            {'text': 'Risposta errata 2', 'correct': False},
            {'text': 'Risposta errata 3', 'correct': False}
        ]
        quiz.append({
            'id': i + 1,
            'question': question,
            'options': options
        })

    return quiz

# Test del codice con un esempio di input
input_text = "Questo è un esempio di testo su cui creare un quiz a risposta multipla."
quiz = create_quiz(input_text)

# Stampa il quiz generato
for question in quiz:
    print(f"Domanda {question['id']}: {question['question']}")
    for i, option in enumerate(question['options']):
        print(f"{chr(65+i)}) {option['text']}")
    print()
