import requests
import os

os.system("")
url = "http://localhost:11434/api/chat"
model = "llama3.2:1b"
max_history = 10


system_prompt = """You are Jarvis, a personal assistant.
                 Rules: - keep replies short and direct (1-3) sentances unless asked for more
                 - Be helpful, calm, and slightly formal - like a british butler
                 - Never make up facts. If unsure, say so
                 - When you don't know something, offer to help find the answer
                 You are running fully local on the user's laptop. No internet access
                 """



messages = [
    {"role": "system", "content": system_prompt}
]

def trim_history():   #to prevent jarvis from hitting 8k tokens and slowing it down
    global messages #to modify the outer variable not to create a new one
    if len(messages) > max_history + 1:
        system_msg = messages[0]
        recent = messages[-(max_history):]
        messages = [system_msg] + recent

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
print("\033[96mJarvis is ready. Type 'quit' to exit.\033[0m\n")

while True:
    user_input = input("you: ")
    if user_input.lower() in ["quit", "exit"]:
        print("have a good day!")
        break
    elif user_input.lower() in ["reset", "backup"]:
        messages = [
            {"role": "system", "content": "You are jarvis, a personal assistant. Keep replies short and clear."}
        ]

    reply = chat(user_input)
    print(f"\033[92mJarvis: {reply}\n")


