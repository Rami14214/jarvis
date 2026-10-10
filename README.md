Jarvis, AI Assistant

Jarvis is an AI assistant that 100% local
and 100% built in python

to build jarvis -i used:
- fast whisperer as a speech to text
- llama3.2:1b from ollama as an LLM
- pyttsx3 for the voice output
- sounddevice to capture the audio
- http to make requests to and from the LLM

Requirements:
- Python 3.11+ 
- Ollama installed
- around 2GB of free storage
- mic and speaker if not integrated in the laptop/pc

How to setup:
1- pull the ollama model:
    ollama pull llama3.2:1b

2- Clone the github repository:
- git clone https://github.com/rami14214/jarvis

3- Create a virtual enviroment:
- python -m venv venv
- venv\scripts\activate

4- install packages:
- pip install -r requirements.txt 


5- Run:
- python chat.py        #for voice mode
- python chat.py --silent     #for silent mode


type help to check all the commands


Enjoy version 1 of Jarvis, more to come!