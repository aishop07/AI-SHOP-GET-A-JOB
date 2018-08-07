from django.shortcuts import render,redirect
from chatterbot import ChatBot
import speech_recognition as sr
import time
import os
from gtts import gTTS
# from . import image_capture as ic
from django.http import HttpResponse
# from . import chtatterbotchinese as cb
# Create your views here.
def index(request):
    return render(request,'home/index.html',locals()) 
def virtualas(request):
    next_page={'url':"/index"}   
    chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer'
    )
    chatbot.train([
                "登入",
                "開始掃描登入 請看著相機",
                "結帳",
                "現在開始結帳",  
                "註冊",
                "正在前往註冊頁面",
                "不要",
                "你說甚麼我聽不懂",
                "好棒",
                "你說甚麼我聽不懂",
    ]
    )
    def speak(audioString):
        print(audioString)
        tts = gTTS(text=audioString, lang='zh-tw')
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
            data=r.recognize_google(audio,language="zh-TW")
            print("You said: " + data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            recordAudio()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return data

    def botinout(data):
        bot_input = chatbot.get_response(data)
        print(bot_input.serialize(),str(bot_input))  
        if len(str(bot_input))==0:
            bot_input='請再說一次'
        print('11111',bot_input)
        speak(str(bot_input))
        return str(bot_input)
        # return
    def friday(sentence):
        print(sentence)
        if "登入" in sentence:
            # return_object=HttpResponse("<script>location.href='photo/login'</script>")
            next_page['url']="/photo/login"
            print(1)
        elif "結帳" in sentence:
            # return_object=HttpResponse("<script>location.href='member/create'</script>") 
            next_page['url']="/member/create"           
            print(2)
        elif "註冊" in sentence:
            # return_object=HttpResponse("<script>location.href='member/create'</script>")  
            next_page['url']="/member/create"
            print(3)
        else:
            print(4)
            friday(botinout(recordAudio()))          
    speak('您好!請問我可以為您做甚麼?')
    friday(botinout(recordAudio()))
    return redirect(next_page['url'])
