import sounddevice as sd
import numpy as np
import speech_recognition as sr
from scipy.io.wavfile import write
import tempfile

def take_voice_command(duration=5, fs=44100):
    print("Listening...")

    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    # Convert to int16 (VERY IMPORTANT)
    recording = (recording * 32767).astype('int16')

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_file.name, fs, recording)

    r = sr.Recognizer()
    with sr.AudioFile(temp_file.name) as source:
        audio = r.record(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        print("Could not understand")
        return ""