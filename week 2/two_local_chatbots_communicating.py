## imports
import requests
import ollama


llama_model = "llama3.2"
deepseek_model = "deepseek-r1"

llama_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

deepseek_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

llama_messages = ["Hi there"]
deep_messages = ["Hi"]


def call_llama():
    messages = [{"role": "system", "content": llama_system}]
    for llama, deep in zip(llama_messages, deep_messages):
        messages.append({"role": "user", "content": llama})
        messages.append({"role": "assistant", "content": deep})
    response = ollama.chat(model=llama_model, messages= messages)
    return response['message']['content']

def call_deepseek():
    messages = [{"role": "system", "content": deepseek_system}]
    for llama, deep in zip(llama_messages, deep_messages):
        messages.append({"role": "user", "content": deep})
        messages.append({"role": "assistant", "content": llama})
    response = ollama.chat(model=deepseek_model, messages= messages)
    return response['message']['content']
               
def __main__():
    print("llama : ", llama_messages)
    print("deep_seek :", deep_messages)
    for i in range(5):
        llama_next = call_llama()
        print("llama : ", llama_messages)
        llama_messages.append(llama_next)
        print()
        deep_next = call_deepseek()
        print("deep_seek :", deep_messages)
        deep_messages.append(deep_next)
        print()