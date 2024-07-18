#Imports
import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from dotenv import load_dotenv

# Load env.
load_dotenv()

# Load vosk model and use KaldiRecognizer tool
model = Model("vosk-model-small-en-us-0.15")
recognizer= KaldiRecognizer(model, 16000) 

# Use pyaudio
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

# print listening
print("listening...")
 
# Loop to listen to the microphone
try:
    while True:
        data = stream.read(8192)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(result.get('text', ''))
        else:
            result = json.loads(recognizer.PartialResult())
            print(result.get('partial', ''))
except KeyboardInterrupt:
    print("Stopping...")

finally:
    stream.stop_stream()
    stream.close()
    mic.terminate()