import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Say something...")
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en-US")
    print("You said:", text)
except Exception as e:
    print("Could not understand. Error:", e)
