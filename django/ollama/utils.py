import speech_recognition as sr

def voice_input():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, phrase_time_limit=5)

    # recognize speech using Sphinx
    try:
        transcribed_audio = r.recognize_sphinx(audio)
        print("Sphinx thinks you said " + transcribed_audio)
        return transcribed_audio
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
        return "Error: Audio not understood"