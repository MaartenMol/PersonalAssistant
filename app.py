#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

import re
import webbrowser
import requests
import xmltodict

import win32com.client as wincl
speak = wincl.Dispatch("SAPI.SpVoice")

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
        result = r.recognize_google(audio, language = "nl-NL")
        print("Google Speech Recognition thinks you said: " + result)
        lookForAgent(result)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def lookForAgent(result):
    if "hey NS".lower() in result.lower():
        agent_NS(result)

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

#Define main APP
if __name__ == '__main__':
    listenMic()