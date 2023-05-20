import openai

openai.api_key = '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'
model_id = 'gpt-3.5-turbo'

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation

def format_response(role, content):
    return f'{role}: {content}\n'

conversation = [{'role': 'system', 'content': 'How may I help you?'}]

while True:
    conversation = ChatGPT_conversation(conversation)
    last_message = conversation[-1]
    formatted_response = format_response(last_message['role'].strip(), last_message['content'].strip())
    print(formatted_response)

    prompt = input('User:')
    conversation.append({'role': 'user', 'content': prompt})
