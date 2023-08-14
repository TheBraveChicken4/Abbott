import openai
import pyaudio
import speech_recognition
import pyttsx3
import re
import wave
import time
import struct
import pvporcupine
import pvcheetah
from pvrecorder import PvRecorder



# Possibly add a sleep function so that the program is only listening for the word wake up or something
# Try to optimize performance if im gonna have it running all the time
#figure out how to import local files and clean up this code so that it runs smoother



#Initializing pvporcupine wake word stuff
ACCESS_KEY = open("paccess_key", "r").read()
KEYWORD_FILE_PATH = r"C:\Users\josh\PycharmProjects\abbott\wake_word\hey-abbott_en_windows_v2_2_0.ppn"


# Chat GPT Integration
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

# Abbott initiation with pyttsx3
abbott = pyttsx3.init()
voices = abbott.getProperty('voices')

abbott.setProperty('rate', 175)
abbott.setProperty('voice', voices[2].id)


def general_speech_to_text():
    full_text = ''
    try:
        cheetah = pvcheetah.create(access_key=ACCESS_KEY, endpoint_duration_sec=2.5)
        recorder = PvRecorder(device_index=-1, frame_length=cheetah.frame_length)
        recorder.start()
        print("listening... recorder in process")
        try:

            while True:

                partial_transcript, is_endpoint = cheetah.process(recorder.read())
                full_text += partial_transcript
                if is_endpoint:
                    final_transcript = cheetah.flush()
                    full_text += final_transcript
                    break

        finally:
            print('done listening')
            recorder.stop()

    finally:
        print(full_text)
        cheetah.delete()
        return str(full_text)



# Function to check for wake word and end up calling speaking()
def listening_for_wake():
    porcupine = None
    pa = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_FILE_PATH])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected .. ")

                #Main speaking functionality here
                return True
                time.sleep(1)
    finally:
        if porcupine is not None:
            porcupine.delete()

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

    abbott.say("What can I do for you today?")
    abbott.runAndWait()

    while True:

        try:
            print("entering speech try")

            text = general_speech_to_text()
            text = text.lower()
            print(text)
            if quit(text):
                break

            if re.search('what are you', text) != None:
                abbott_description()
                pass

            if re.search('what time is it', text) != None:
                tell_time()
                pass
            else:
                print(f"User: {text}")

                sleep_words = ["goodbye abbott", "goodbye", "bye", "bye abbott", "talk to you later","thank you"]
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
            print("entering speech except")
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
    # try:
    print("entering main try")
    if listening_for_wake():
        # time.sleep(0.5)
        speaking()


    # except Exception as e:
    #     print("entering except")
    #     recognizer = speech_recognition.Recognizer()
    #     continue


