import pyttsx3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--silent', action='store_true')
args = parser.parse_args()



def speak(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[0].id)
    engine.say(text)
    engine.runAndWait()


if args.silent == False:
    speak("Say something!")
print("say something!")
