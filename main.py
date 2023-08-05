import openai
import speech_recognition
import pyttsx3
import re
import wave
import time
import struct
import pvporcupine


# Possibly add a sleep function so that the program is only listening for the word wake up or something
# Try to optimize performance if im gonna have it running all the time
# Try to implement a way to have the prorgam keep listening as you keep speaking.
#Its annoying to have to try and time your input and having it break if you mess it up
# what time is it abbott

#Initializing pvporcupine wake word stuff
ACCESS_KEY = open("paccess_key", "r").read()
KEYWORD_FILE_PATH = open("wake_words", "r").read()

porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=KEYWORD_FILE_PATH)
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)

# Chat GPT Integration
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

# Abbott initiation with pyttsx3
abbott = pyttsx3.init()
voices = abbott.getProperty('voices')

abbott.setProperty('rate', 175)
abbott.setProperty('voice', voices[2].id)


def listening_for_wake():
    porcupine = None
    pa = None
    audio_stream = None


def quit(inp):
    if inp == 'shut down':
        abbott.say("Powering down, have a nice day")
        abbott.runAndWait()
        return True

def abbott_description():
    abbott.say("Good question! Im a fairly simple AI assistant created for the purpose of satisfying curiosity. "
               "I am connected to chat g p t and that is where I get most of my answers. Right now I do not have much "
               "functionality besides text based responses, but I hope to one day be developed further as an "
               "original deep learning algorithm capable of producing physical results, as well as playing music, "
               "creating art and learning independently.")

    abbott.runAndWait()

# Function to check for wake word and end up calling speaking()
def check_for_wake(string):

    wake_word_list = ["hey abbott"]
    for word in wake_word_list:

        regex = re.search(word, string)

        if regex != None:
            return True
    return False

# check if there is a func from this module that does this more efficiently
def tell_time():
    current_time = time.strftime("%H %M %p")
    current_time = current_time.split(' ')
    current_hour = current_time[0]
    current_hour = int(current_hour)

    if current_hour > 12:
        current_hour -= 12


    current_hour = str(current_hour)
    current_time[0] = current_hour
    current_time = ' '.join(current_time)
    abbott.say(current_time)
    abbott.runAndWait()


# Function for chat gpt responses and assistant like behavior
def speaking():

    abbott.say("Hello, what can I do for you today")
    abbott.runAndWait()

#Figure out how to wait a long time to capture input, but as soon as input is captured and there is no more
#speaking then stop the recording and answer the prompt

    while True:

        try:

            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio, key=None, language='en-IN')
            text = text.lower()
            print(f"User: {text}")

            sleep_words = ["goodbye abbott", "goodbye", "bye", "bye abbott", "talk to you later"]
            for word in sleep_words:
                abbott_regex = re.search(word, text)
                if abbott_regex != None:
                    abbott.say("Goodbye sir, have a nice day")
                    abbott.runAndWait()
                    return

            chat_log.append({"role": "user", "content": text})
            print("chatbot started")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=chat_log
            )

            abbott_response = response['choices'][0]['message']['content']
            abbott_response = abbott_response.strip("\n").strip()

            print("Abbott:", abbott_response)
            abbott.say(abbott_response)
            abbott.runAndWait()


            chat_log.append({"role": "assistant", "content": abbott_response.strip("\n").strip()})

        except Exception as e:

            # abbott.say("I'm sorry, I didn't catch that. Can you please repeat?")
            pass


# Speech Recognition
text = ''
recognizer = speech_recognition.Recognizer()
# Function Definitions:

# Quit function to stop program when prompted


chat_log = []
print("Listening...")


# Main program loop
while True:
    print(pvporcupine.KEYWORDS)
    # try:
    print("entering try")
    with speech_recognition.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
        # audio = recognizer.record(mic, duration=5)
        print("listening")
        #Abbotts main issue rn is with this line of code, sometimes the program just does not stop listening
        audio = recognizer.listen(mic)
        recognizer.pause_threshold = 3

        print("done listening")
        text = recognizer.recognize_google(audio, key=None, language='en-IN')
        text = text.lower()
        print(text)

        if check_for_wake(text):
            speaking()

        if quit(text):
            break

        if re.search('abbott what are you', text) != None:
            abbott_description()

        if re.search('abbott what time is it', text) != None:
            tell_time()

    # except Exception as e:
    #     print("entering except")
    #     recognizer = speech_recognition.Recognizer()
    #     continue
