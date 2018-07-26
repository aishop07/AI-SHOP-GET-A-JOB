#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("audio.mp3")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("What can I do for you?")
        audio = r.listen(source)
        print(audio)
 
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def Friday(data):
    if "Friday open computer" in data:
        speak("hi chris! the system is ready ")
    if "check computer" in data:
        speak("the system status is working well")
    if "what's your name" in data:
        speak("My name is friday")
    if "what time is it" in data:
        speak(ctime())
    if "close computer" in data:
        speak('got it')
        speak('goodbye chris')
        exit()
    
 
    
 
# initialization
time.sleep(2)
speak("Hi chris!What can I do for you!")
while True:
    data = recordAudio()
    Friday(data)
    