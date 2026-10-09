import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

sample_rate = 16000
duration = 5

print("Loading whisper model (first run downloads it)...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("model loaded.\n")

input("Press Enter to start recording 5 seconds...")
print("recording...")

audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
sd.wait()

print("recording completed.\n")

audio_flat = audio.flatten()

segments, info = model.transcribe(audio_flat, language="en")

text = " ".join(seg.text.strip() for seg in segments)
print(f"you said: {text}")

