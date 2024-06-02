import pyttsx3
import os
import datetime
import wikipedia
import webbrowser
import speech_recognition as sr
import random

count = 0
new_rate = 150
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', new_rate)

def speak(audio):
    # this function is for computer speaking
    engine.say(audio)
    engine.runAndWait()

def greetings():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Hello, Good Morning")
    elif 12 <= hour < 17:
        speak("Hello, Good Afternoon")
    elif 17 <= hour < 22:
        speak("Hello, Good Evening")
    else:
        speak("Hello, Good Night")
    speak("I am Sera. How can I help you.")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-uk')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "none"
    return query.lower()

if __name__ == '__main__':
    greetings()
    while True:
        if count > 0:
            speak("Anything else?")

        main_query = take_command()
        print(main_query)

        if 'wikipedia' in main_query:
            speak("Searching in Wikipedia...")
            main_query = main_query.replace("wikipedia", "")
            results = wikipedia.summary(main_query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            count += 1

        elif 'facebook' in main_query:
            webbrowser.open('https://www.facebook.com')
            count += 1

        elif 'code' in main_query:
            code_path = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
            count += 1

        elif 'time' in main_query:
            str_time = datetime.datetime.now().strftime('%H:%M:%S')
            speak(str_time)
            count += 1

        elif 'cafeteria' in main_query or 'canteen' in main_query or 'food court' in main_query:
            speak("It is on the fourth floor.")
            count += 1

        elif 'sana safinaz' in main_query:
            speak("It is on the third floor, shop number 3.")
            count += 1

        elif 'gul ahmed' in main_query:
            speak("It is on the third floor, shop number 1.")
            count += 1

        elif 'al karam' in main_query:
            speak("It is on the second floor, shop number 3.")
            count += 1

        elif 'jay dot' in main_query:
            speak("It is on the first floor, shop number 3.")
            count += 1

        elif 'washroom' in main_query or 'bathroom' in main_query:
            speak("Please turn left, then go straight.")
            count += 1

        elif 'emergency exit' in main_query:
            speak("Please turn right, then go straight, take left and there are stairs which lead you towards the emergency exit gate.")
            count += 1

        elif 'exit' in main_query:
            speak("Please turn left, then go straight, take right and there is the main exit gate.")
            count += 1

        elif 'fire' in main_query:
            speak("Please turn right, then go straight, take left and there are stairs which lead you towards the emergency exit gate.")
            count += 1

        elif 'none' in main_query:
            speak("Say that again please")
            count += 1

        elif 'thank you' in main_query or 'thankyou' in main_query:
            speak("It's my pleasure.")
            exit()

        elif 'thanks' in main_query or 'thank' in main_query:
            speak("It's my pleasure.")
            exit()
            
        elif 'none' in main_query or 'no' in main_query:
            speak("It's my pleasure.")
            exit()

        