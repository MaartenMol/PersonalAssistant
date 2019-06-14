import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import urllib
import json
from bs4 import BeautifulSoup as soup
import wikipedia
import random
from time import strftime
from playsound import playsound

import pyttsx3
engine = pyttsx3.init()

from gtts import gTTS
import os

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")


def sofiaResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        
        os.system("say " + audio)
def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command
def assistant(command):
    "if statements for executing commands"
#open subreddit Reddit
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        
        engine.say("The Reddit content has been opened for you Sir.")
        engine.runAndWait()

        tts = gTTS(text='The Reddit content has been opened for you Sir.', lang='en')
        tts.save("good.mp3")

        playsound('good.mp3')

        #speak.Speak("The Reddit content has been opened for you Sir.")

        #sofiaResponse('The Reddit content has been opened for you Sir.')

while True:
    assistant(myCommand())