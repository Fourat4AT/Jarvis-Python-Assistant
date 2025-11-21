
import datetime
import os
import sys
import time
import webbrowser
import pyautogui
import pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
import json
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import numpy as np
import psutil 
import subprocess
# from elevenlabs import generate, play
# from elevenlabs import set_api_key
# from api_key import api_key_data
# set_api_key(api_key_data)

# def engine_talk(query):
#     audio = generate(
#         text=query, 
#         voice='Grace',
#         model="eleven_monolingual_v1"
#     )
#     play(audio)

with open("intents.json") as file:
    data = json.load(file)

model = load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer=pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder=pickle.load(encoder_file)

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening.......", end="", flush=True)
        r.pause_threshold=1.0
        r.phrase_threshold=0.3
        r.sample_rate = 48000
        r.dynamic_energy_threshold=True
        r.operation_timeout=5
        r.non_speaking_duration=0.5
        r.dynamic_energy_adjustment=2
        r.energy_threshold=4000
        r.phrase_time_limit = 10
        # print(sr.Microphone.list_microphone_names())
        audio = r.listen(source)
    try:
        print("\r" ,end="", flush=True)
        print("Recognizing......", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print("\r" ,end="", flush=True)
        print(f"User said : {query}\n")
    except Exception as e:
        print("Say that again please")
        return "None"
    return query

def cal_day():
    day = datetime.datetime.today().weekday() + 1
    day_dict={
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
    return day_of_week

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = time.strftime("%I:%M:%p")
    day = cal_day()

    if(hour>=0) and (hour<=12) and ('AM' in t):
        speak(f"Good morning Mishu, it's {day} and the time is {t}")
    elif(hour>=12)  and (hour<=16) and ('PM' in t):
        speak(f"Good afternoon Mishu, it's {day} and the time is {t}")
    else:
        speak(f"Good evening Mishu, it's {day} and the time is {t}")

def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'discord' in command:
        speak("opening your discord server")
        webbrowser.open("https://discord.com/")
    elif 'instagram' in command:
        speak("opening your instagram")
        webbrowser.open("https://www.instagram.com/")
    else:
        speak("No result found")

def schedule():
    day = cal_day().lower()
    speak("Boss today's schedule is ")
    week={
    "monday": "Boss, today you have a productive start. From 9:00 to 10:30 you’ll review Enetcom network configurations, from 10:30 to 11:00 you have a short break, from 11:00 to 12:30 you’ll practice Python automation tasks, from 12:30 to 1:30 you have lunch, and from 1:30 to 3:00 you’ll work on configuring Cisco switches.",
    "tuesday": "Boss, today you’ll focus on security. From 9:00 to 10:30 you have a workshop on firewall setups, from 10:30 to 11:00 you have a break, from 11:00 to 12:30 you’ll work on your Kali Linux penetration testing lab, from 12:30 to 1:30 you have lunch, and from 1:30 to 3:00 you’ll review Wireshark traffic analysis.",
    "wednesday": "Boss, today is hands-on networking day. From 9:00 to 11:00 you’ll configure VLANs and test inter-VLAN routing on your lab, from 11:00 to 11:30 you have a coffee break, from 11:30 to 1:00 you’ll practice VPN setups, and from 1:00 to 3:00 you’ll continue working on your Enetcom lab exercises.",
    "thursday": "Boss, today is coding-focused. From 9:00 to 10:30 you’ll work on your backend Python scripts, from 10:30 to 11:00 you have a break, from 11:00 to 12:30 you’ll debug your automation projects, from 12:30 to 1:30 you have lunch, and from 1:30 to 3:00 you’ll integrate APIs into your projects.",
    "friday": "Boss, today is review and documentation day. From 9:00 to 10:30 you’ll write lab reports for your networking projects, from 10:30 to 11:00 you have a break, from 11:00 to 12:30 you’ll update your project logs and notes, from 12:30 to 1:30 you have lunch, and from 1:30 to 3:00 you’ll plan next week’s tasks.",
    "saturday": "Boss, today is learning and personal projects. From 9:00 to 11:00 you’ll watch tutorials on advanced network security, from 11:00 to 11:30 you have a break, from 11:30 to 1:00 you’ll practice lab exercises on Enetcom, and from 1:00 to 3:00 you’ll explore Python mini-projects.",
    "sunday": "Boss, today is a rest day, but you can spend 1-2 hours reviewing notes or checking upcoming tasks for the week."
}

    if day in week.keys():
        speak(week[day])


def openApp(command):
    if "calculator" in command:
        speak("Opening Calculator")
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif "notepad" in command:
        speak("Opening Notepad")
        os.startfile('C:\\Windows\\System32\\notepad.exe')
    elif "paint" in command:
        speak("Opening Paint")
        os.startfile('C:\\Windows\\System32\\mspaint.exe')
    elif "elden ring" in command.lower():
        speak("Opening Elden Ring")
        os.startfile(r'D:\Games\ELDEN RING\Game\eldenring.exe')
        

def closeApp(command):
    if "calculator" in command:
        speak("closing calculator")
        os.system("taskkill /f /im calc.exe")
    elif "notepad" in command:
        speak("closing notepad")
        os.system('taskkill /f /im notepad.exe')
    elif "paint" in command:
        speak("closing paint")
        os.system('taskkill /f /im mspaint.exe')

def browsing(query):
    if 'google' in query:
        speak("Boss, what should i search on google..")
        s = command().lower()
        webbrowser.open(f"{s}")
    # elif 'edge' in query:
    #     speak("opening your microsoft edge")
    #     os.startfile()

def condition():
    usage = str(psutil.cpu_percent())
    speak(f"CPU is at {usage} percentage")
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak(f"Boss our system have {percentage} percentage battery")

    if percentage>=80:
        speak("Boss we could have enough charging to continue our recording")
    elif percentage>=40 and percentage<=75:
        speak("Boss we should connect our system to charging point to charge our battery")
    else:
        speak("Boss we have very low power, please connect to charging otherwise recording should be off...")

if __name__ == "__main__":
    wishMe()
    speak("Allow me to introduce myself I am Jarvis, the virtual artificial intelligence and I'm here to assist you with a variety of tasks as best I can, 24 hours a day seven days a week.")
    while True:
        query = command().lower()
        # query  = input("Enter your command-> ")
        if ('facebook' in query) or ('discord' in query) or ('whatsapp' in query) or ('instagram' in query):
            social_media(query)
        elif ("university time table" in query) or ("schedule" in query):
            schedule()
        elif ("volume up" in query) or ("increase volume" in query):
            pyautogui.press("volumeup")
            speak("Volume increased")
        elif ("volume down" in query) or ("decrease volume" in query):
            pyautogui.press("volumedown")
            speak("Volume decrease")
        elif ("volume mute" in query) or ("mute the sound" in query):
            pyautogui.press("volumemute")
            speak("Volume muted")
        elif ("open calculator" in query) or ("open notepad" in query) or ("open paint" in query):
            openApp(query)
        elif ("close calculator" in query) or ("close notepad" in query) or ("close paint" in query):
            closeApp(query)
        elif ("what" in query) or ("who" in query) or ("how" in query) or ("hi" in query) or ("thanks" in query) or ("hello" in query):
                padded_sequences = pad_sequences(tokenizer.texts_to_sequences([query]), maxlen=20, truncating='post')
                result = model.predict(padded_sequences)
                tag = label_encoder.inverse_transform([np.argmax(result)])

                for i in data['intents']:
                    if i['tag'] == tag:
                        speak(np.random.choice(i['responses']))
        elif ("open google" in query) or ("open edge" in query):
            browsing(query)
        elif ("system condition" in query) or ("condition of the system" in query):
            speak("checking the system condition")
            condition()
        elif "exit" in query:
            sys.exit()
# speak("Hello, I'm JARVIS")