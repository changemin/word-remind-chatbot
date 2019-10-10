import pyttsx3
import json

with open('config.json', 'r', encoding='UTF-8') as config: # read config file
    data = config.read()
    configData = json.loads(data)
    voiceID_KO = configData['TTS']['voiceID_KO']
    voiceID_EN = configData['TTS']['voiceID_EN']

engine = pyttsx3.init()

# Voice IDs pulled from engine.getProperty('voices')
# These will be system specific

# Use female English voice
engine.setProperty('voice', voiceID_EN)
engine.say('Hello with my new voice')

# Use female Russian voice
engine.setProperty('voice', voiceID_KO)
engine.say('이건 한국어야')

engine.runAndWait()