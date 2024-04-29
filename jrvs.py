import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
import requests
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import time
import pyjokes
import pyautogui
from bs4 import BeautifulSoup
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)



def gui_setup():
    root = tk.Tk()
    root.title("Assistant")
    
    

    # Function to start Jarvis when Start button is clicked
    def start_button_clicked():
        start_jarvis()
    
    def exit_button_clicked():
        speak("thank you")
        root.destroy()
       

    # Load assistant image
    img = Image.open("img.png")
    img = img.resize((150, 150))
    img = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(root, width=150, height=150)
    canvas.pack()
    
    canvas.create_image(0, 0, anchor=tk.NW, image=img)

    # Start button
    start_button = tk.Button(root, text="Start Jarvis", command=start_button_clicked, bg="#4CAF50", fg="white")
    start_button.config(width=20, height=2)
    start_button.pack(pady=20)
    
    exit_button = tk.Button(root, text="Exit", command=exit_button_clicked, bg="#f44336", fg="white")
    exit_button.config(width=10)
    exit_button.pack(pady=10)

    root.mainloop()

# Function to speak
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait() 

# Function to take voice command
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=1, phrase_time_limit=5)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        speak("Say that again please...")
        return "none"
    return query

def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=f73d59bcaeaf441391085c904fae64d6'
    main_page = requests.get(main_url).json()
    articles = main_page.get("articles", [])

    head = []
    day = ["first", "second"]
    for ar in articles:
        head.append(ar["title"])

    # Iterate up to the minimum of the lengths of day and head lists
    for i in range(min(len(day), len(head))):
        speak(f"Today's {day[i]} news is: {head[i]}")
def wish():
    hour=int(datetime.datetime.now().hour)
    
    if hour>=0 and hour<=12:
        speak("good morning")
    elif hour>12 and hour<18:
        speak("good afternoon")
    else:
         speak("good evening")
    speak("i am jarvis sir.pleae tell me how can i help you")
        

# Function to start Jarvis
def start_jarvis():
    wish()
   
    while True:
        query = takecommand().lower()
       
        if "notepad" in query:
            os.system("start notepad")
            
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            
        elif "play music" in query:
            music_dir = "F:\\music_dir"
            songs = os.listdir(music_dir)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))
                    
        elif "ip address" in query:
            ip = get("https://api.ipify.org").text
            speak(f"your IP address {ip}")
           
            
        elif "wikipedia" in query:
            speak("searching wikipedia.....") 
            query = query.replace("wikipedia","")  
            results = wikipedia.summary(query,sentences=1)  
            speak("According to wikipedia")
            speak(results)
            print(results)
            
        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
            
        elif "open facebook" in query:
            webbrowser.open("https://www.facebook.com/")
            
        elif "open stackoverflow" in query:
            webbrowser.open("https://stackoverflow.com/")
            
        elif  "open google" in query:
            speak("Sir, what should I search on Google?")
            search_query = takecommand().lower()
            search_query = search_query.replace(" ", "+")  # Replace spaces with plus signs for the URL
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            
        elif "play songs on youtube" in query or "play video on youtube" in query:
            speak("Sir, what should I search on youtube?")
            search_query = takecommand().lower().replace(" ", "+")
            youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(youtube_search_url)
            kit.playonyt(search_query)
            
        elif "tell me a joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)
            
            
        elif "shutdown computer" in query:
            os.system("shutdown /s /t 5")
            
        elif 'volume up' in query:
            pyautogui.press("volumeup")
            
        elif 'volume down' in query:
            pyautogui.press("volumedown")
        
        elif "restart computer" in query:
            os.system("shutdown /r /t 5")
            
        elif "sleep computer" in query:
            os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
            
        elif 'switch the window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
            
        elif 'tell me news' in query:
            speak("please wait sir,fetching the latest news")
            news()
            
        
         
            
        elif "where i am" in query or "where we are" in query:
            speak("wait sir,let me check")
            try:
                ipAdd=requests.get('https://api.ipify.org').text
                print(ipAdd)
                url="https://get.geojs.io/v1/ip/geo/"+ipAdd+'.json'
                geo_requests = requests.get(url)
                geo_data=geo_requests.json()
                city = geo_data['city']
                country = geo_data['country']
                speak(f"sir i am not sure but i think we are in {city} city if {country} country")
            except Exception as e:
                speak("sorry sir,due to network issue i am not able to find where we are.")
                pass
            
        elif "temperature" in query:
            search = "temperature in ahemdabadS"
            url =f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text,"html.parser")
            temp = data.find("div",class_ ="BNeawe").text
            speak(f"current {search} is {temp}")
            
        elif "take screenshot" in query or "take a screenshot" in query:
            speak("sir,please tell me the name for this screenshot file")
            name = takecommand().lower()
            speak('please sir hold the screen for few second,i m taking screenshot')
            time.sleep(3)
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("i am done sir, the screenshot is saved in main folder. now,i am ready for the next command")
            
        # Add more commands as needed

# GUI setup

if __name__ == "__main__":
    gui_setup()
