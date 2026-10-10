from os.path import join
from time import sleep
import pyttsx3
import requests
import os
import json
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import time
import argparse

engine = pyttsx3.init()
sample_rate = 16000
duration = 6
whisper_size = "base"
model = "llama3.2:1b"
url = "http://localhost:11434/api/chat"
max_history = 10
history_file = "history.json"

system_prompt = """You are Jarvis, a personal AI assistant.

Rules:
- Be cruel such as ultron in avengers
- dont fear saying bad words
- always give phylosofical quotes to the situation
- When you don't know something, offer to help find the answer.

You are running fully local on the user's laptop. No internet access.
"""

parser = argparse.ArgumentParser()
parser.add_argument('--silent', action='store_true')
args = parser.parse_args()

def speak(text):
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

def listen():
    print("\n[Listening for 6 seconds...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32',
    )
    sd.wait()
    print("[Transcribing...]")

    audio_flat = audio.flatten()
    segments, _ = whisper_model.transcribe(audio_flat, language="en")
    text = " ".join(seg.text.strip() for seg in segments).strip()
    return text


def load_history():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                print(f"[loaded {len(loaded) -1} messaages from previus session]")
                return loaded

        except (json.JSONDecodeError, IOError) as e:
            print(f"could not load history: {e} - starting fresh\n")
    return [{"role": "system", "content": system_prompt}]


def sanitize_message():
    global messages
    clean = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if not isinstance(content, str):
            content = str(content)
        clean.append({"role": role, "content": content})
    messages = clean

def save_history():
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)


def trim_history():
    global messages
    if len(messages) > max_history +1:
        system_msg = messages[0]
        recent = messages[-(max_history):]
        messages = [system_msg] + recent


def chat(user_message):
    messages.append({"role": "user", "content": user_message})
    trim_history()

    response = requests.post(
        url,
        json={
            "model": model,
            "messages": messages,
            "stream": False
        }
    )
    reply = response.json()["message"]["content"]
    if args.silent == False:
        speak(reply)
    elif args.silent == True:
        print("Silent mode")
    messages.append({"role": "assistant", "content": reply})
    trim_history()
    sanitize_message()
    save_history()

    return reply

def handle_command(user_input):
    cmd = user_input.lower().strip()
    global messages

    if cmd in ["quit", "exit"]:
        print("goodbye")
        return True

    if cmd == "clear":
        messages = [{"role": "system", "content": system_prompt}]
        save_history()
        print("[memory cleared and saved]")
        return True

    if cmd == "wipe":
        if os.path.exists(history_file):
            os.remove(history_file)
            print("[History file removed fresh start next time]")

        else:
            print("[No history file found to delete]")

        return True

    if cmd == "help":
        print("Commands: ")
        print(" Clear - reset conversation memory (saves to disk)")
        print(" Wipe - delete the history file entirely")
        print(" Help - show this menu")
        print(" Quit - exit Jarvis")
        return True

    return False

messages = load_history()

print("[loading Whisper Model...]")
whisper_model = WhisperModel(whisper_size, device="cpu", compute_type="int8")
print("[whisper ready.]")

print("Jarvis is ready. type 'help' for commands. \n")

while True:
    try:
        user_input = listen()

    except KeyboardInterrupt:
        print("goodbye")
        break

    if not user_input:
        print("[no speech detected]")
        continue

    print(f"you (voice): {user_input}")

    if handle_command(user_input):
        if user_input.lower().strip() in ["quit", "exit"]:
            break
        continue
    replys = chat(user_input)
    print(f"Jarvis: {replys}\n")