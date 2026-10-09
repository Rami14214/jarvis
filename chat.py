import requests

url = "http://localhost:11434/api/chat"
model = "llama3.2:1b"


messages = [
    {"role": "system", "content": "You are jarvis, a personal assistant. Keep replies short and clear."}
]


def chat(message):
    messages.append({"role": "user", "content": message})

    response = requests.post(
        url,
        json={
            "model": model,
            "messages": messages,
            "stream": False
        }
    )
    reply = response.json()["message"]["content"]

    messages.append({"role": "assistant", "content": reply})
    return reply
print("jarvis is ready. Type 'quit' to exit.\n")

while True:
    user_input = input("you: ")
    if user_input.lower() in ["quit", "exit"]:
        print("have a good day!")
        break

    reply = chat(user_input)
    print(f"Jarvis: {reply}\n")


