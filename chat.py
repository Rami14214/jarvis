import requests

def ask_ollama(prompt):
    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "llama3.2:1b",
                                 "prompt": prompt,
                                 "stream": False
                             })
    return response.json()["response"]

print("jarvis is ready. Type 'quit' to exit.\n")

while True:
    user_input = input("you: ")
    if user_input.lower() in ["quit", "exit"]:
        print("have a good day!")
        break

    reply = ask_ollama(user_input)
    print(f"Jarvis: {reply}\n")


