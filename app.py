#!/usr/bin/env python3

# Required for MIC: PyAudio

speechLang = "nl-NL"
import speech_recognition as sr
import re, webbrowser, requests, xmltodict, datetime
from googlesearch import search
from pyowm import OWM

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

# from phue import Bridge
# bridge = Bridge('192.168.0.33')

def listenMic():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        #r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("Recorded")

    # recognize speech using Google Speech Recognition
    print("Sending to Google...")
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio, language = speechLang)
        print("Google Speech Recognition thinks you said: " + result)
        lookForAgent(result)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def lookForAgent(result):
    if "NS".lower() in result.lower():
        agent_NS(result)
    # if "hey Philips".lower() in result.lower():
    #     agent_Philips(result)
    if "Jarvis".lower() in result.lower():
        agent_Jarvis(result)

def agent_NS(result):
    if "welke treinen vertrekken" in result.lower():
        reg_ex = re.search('welke treinen vertrekken er vanaf (.*)', result.lower())
        if reg_ex:
            Station = reg_ex.group(1)

        #API Authentication
        auth_details = ('joshuajessy47@gmail.com', 'vlgUm9-dkCiFX8swDoQ4uNdO1kiNtZhBs1CAIkbJl6gX3946BJ8uEQ')

        #API Query
        api_url = 'http://webservices.ns.nl/ns-api-avt?station='+ Station
        response = requests.get(api_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)

        #Result
        print('Dit zijn de vertrekkende treinen:')
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16] # 18:36
            trein = vertrek['TreinSoort']
            spoor = str(vertrek['VertrekSpoor'])
            spoor1 = spoor.replace("OrderedDict([('@wijziging', 'false'), ('#text', '", "")
            spoor2 = spoor1.replace("')])", "")
            spoor3 = spoor2.replace("OrderedDict([('@wijziging', 'true'), ('#text', '", "")
            try:
                vertraging = ' met ' + vertrek['VertrekVertragingTekst'] + ' vertraging '
            except KeyError:
                vertraging = ""

            vertragingInfo = vertraging.replace("+", "")

            print('Om '+vertrektijd+' vertrekt er een ' + trein + ' richting '+ eindbestemming + ' vanaf spoor ' + spoor3 + vertragingInfo)

    if "geef informatie over" in result.lower():
        reg_ex = re.search('geef informatie over station (.*)', result.lower())
        ns_url = 'https://www.ns.nl'
        if reg_ex:
            Station = reg_ex.group(1)

        print("Ik ga info geven over " + Station)

        URL = "https://www.ns.nl/rio-reisinfo-api/service/stations?q=" + Station

        r = requests.get(url = URL)

        data = r.json() 

        station_id = data[0]['id'] 
        station_naam = data[0]['naam'] 

        goUrl = ns_url + '/stationsinformatie/' + station_id + "/" + station_naam
        webbrowser.open(goUrl)

# def agent_Philips(result):
#     if "verbind mijn lichten" in result.lower():
#         bridge.connect()
    
#     if "zet de lichten aan in de" in result.lower():
#         reg_ex = re.search('zet de lichten aan in de (.*)', result.lower())
#         if reg_ex:
#             room = reg_ex.group(1)
        
#         bridge.set_light(room,'on', True)
#         print("De lichten in de " + room + " staan nu aan!")

def agent_Jarvis(result):
    if "open reddit" in result.lower():
        reg_ex = re.search('open reddit (.*)', result.lower())
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1).lower()
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        # speak.Speak("Opening Reddit for you!")

    if "zoek op" in result.lower():
        reg_ex = re.search('zoek op (.*)', result)
        url = 'https://www.google.com'
        if reg_ex:
            search = reg_ex.group(1)
            url = url + '/search?q=' + search
        webbrowser.open(url)
        # speak.Speak("Opening Google for you!")

    if "hoe is het weer" in result.lower():
        reg_ex = re.search('hoe is het weer in (.*)', result.lower())
        if reg_ex:
            city = reg_ex.group(1)
        owm = OWM(API_key='ab0d5e80e8dafb2cb81fa9e82431c1fa')
        obs = owm.weather_at_place(city)
        w = obs.get_weather()
        k = w.get_status()
        x = w.get_temperature(unit='celsius')
        result = 'Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min'])
        print(result)
        speak.Speak(result)

    if "hoe laat" in result.lower():
        now = datetime.datetime.now()
        time = 'Current time is %d hours %d minutes' % (now.hour, now.minute)
        print(time)
        speak.Speak(time)

#Define main APP
if __name__ == '__main__':
    while True:
        listenMic()