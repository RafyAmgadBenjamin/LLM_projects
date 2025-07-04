# imports
import ollama
from openai import OpenAI
from dotenv import load_dotenv
import os

# constants

MODEL_GPT = 'gpt-4o-mini'
MODEL_LLAMA = 'llama3.2'

# set up environment
# Initialize and constants

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if api_key and api_key.startswith('sk-proj-') and len(api_key)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")
    
MODEL = 'gpt-4o-mini'
openai = OpenAI()

# here is the question; type over this to ask something new

question = """
Please explain what this code does and why:
yield from {book.get("author") for book in books if book.get("author")}
"""

# Get gpt-4o-mini to answer, with streaming
def find_answer_chat_gpt(question):
    stream = openai.chat.completions.create(
        model= MODEL_GPT, 
        messages = [
            {"role": "system", "content": "You are generic chatpot that can help me to answer any question including the coding one"},
            {"role": "user", "content": question}
        ],
        stream = True
    )
    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ''
        response += content
        print(content, end='', flush=True)  # Print only the new chunk, not the full response
    print()
    return response


# Get Llama 3.2 to answer

def find_answer_llama(question):
    stream = ollama.chat(
            model= MODEL_LLAMA, 
            messages = [
            {"role": "system", "content": "You are generic chatpot that can help me to answer any question including the coding one"},
            {"role": "user", "content": question}
        ],
            stream = True
        )
    response = ""
    for chunk in stream:
        content = chunk['message']['content']
        response += content
        print(content, end='', flush=True)
    print()
    return response

def __main__():
    print("Answer from GPT-4o-mini:")
    find_answer_chat_gpt(question)
    
    print("\nAnswer from Llama 3.2:")
    find_answer_llama(question)