# consultant.html - Finance Consultant UI
# <button>Record</button>

# https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py
import speech_recognition as sr
import requests

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    transcribed_audio = r.recognize_sphinx(audio)
    print("Sphinx thinks you said " + transcribed_audio)
except sr.UnknownValueError:
    print("Sphinx could not understand audio")

# Send transcribed_audio to api
response = requests.post("http://127.0.0.1:11434", json=transcribed_audio)
# Type the output in consultant.html
print(response.text)
