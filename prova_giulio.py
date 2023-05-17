import PyPDF2
import random
import openai

openai.api_key = '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'

def generate_question_answer(text):
    # Controlla la lunghezza del testo
    if len(text) > 4096:
        text = text[:4096]  # Taglia il testo se supera il limite consentito
    
    # Genera una domanda
    question = "Qual è la seguente affermazione vera?\n" + text
    
    # Genera una risposta corretta
    answer_correct = text
    
    # Genera 4 risposte errate
    answers_wrong = []
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=100,
        n=4,
        stop=None,
        temperature=0.6,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    if response.choices:
        answers_wrong = [choice['text'] for choice in response.choices]
    
    # Randomizza l'ordine delle risposte
    answers = [answer_correct] + answers_wrong
    random.shuffle(answers)
    
    return question, answers

def process_pdf(file_path):
    # Apre il file PDF
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Estrae il testo da tutte le pagine
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Dividi il testo in domande
        questions = text.split('?')
        
        # Genera domande e risposte per ogni domanda
        quiz = []
        for question_text in questions:
            if question_text.strip() != '':
                question, answers = generate_question_answer(question_text)
                quiz.append({
                    'question': question,
                    'answers': answers
                })
        
        return quiz

# Esempio di utilizzo
quiz = process_pdf('C:/Users/giuli/OneDrive/Desktop/Cloud Computing/2023_02_09_lecture_notes_21_22_Cloud_Computing_Giacomo_Pacini.pdf')

# Stampa le domande e le risposte generate
for i, qna in enumerate(quiz):
    print(f"Domanda {i+1}: {qna['question']}")
    for j, answer in enumerate(qna['answers']):
        print(f"{chr(65 + j)}) {answer}")
