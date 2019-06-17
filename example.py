import speech_recognition as sr

speechLang = "nl-NL"

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
    if "Jarvis".lower() in result.lower():
        agent_Jarvis(result)

def agent_Jarvis(result):
    if "hoe gaat het" in result.lower():
        print("Met mij gaat het goed meneer!")

#Define main APP
if __name__ == '__main__':
    while True:
        listenMic()

import rquests

API_ENDPOINT = "http://test-api.nl/api/getStatus"

r = requests.get(url = API_ENDPOINT) 
response = json.loads(r.text)