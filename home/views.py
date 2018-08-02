from django.shortcuts import render
import datetime
from chatterbot import ChatBot
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
import cv2
from. import image_capture as ic
from django.http import HttpResponse

# Create your views here.
def index(request):
    now = datetime.datetime.now()
    return render(request,'home/index.html',locals())
def virtualas(request):
     jirvis()
def jirvis(): 
    chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
    )
    chatbot.train([
                "login",
                "please look the camera for login process",
                "check",
                "now checking the pice for you" ,  
                "close computer",
                "goodbye chris",
                "take the photo ",
                "for taking the photo correctly, please look the camera, If you are ready press the space buttom "     
        ]
        )
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
        data ='' 
        try:
            # Uses the default API key
            # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`      
            data=r.recognize_google(audio)
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return data

    def botinout(data):
        bot_input = chatbot.get_response(data)
        speak(str(bot_input))
        return str(bot_input)
    def friday(sentence):
        if "ok" in sentence:
            pass
        if "check" in sentence:
            pass
        if "goodby" in sentence:
            exit()
        if "for taking" in sentence:
            # ic.photogetter()
            speak('photo have been taked ')
            exit()    
    speak('Hi!Chris!What can I do for you?')
    while 1:
            friday(botinout(recordAudio()))
            
        
