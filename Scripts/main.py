import openai
import speech_recognition
import pyttsx3
import re



# Possibly add a sleep function so that the program is only listening for the word wake up or something
# Try to optimize performance if im gonna have it running all the time




#global variables
quit_bool = False

# Chat GPT Integration
API_KEY = open("API_KEY", "r").read()
openai.api_key = API_KEY

# Abbott initiation with pyttsx3
abbott = pyttsx3.init()
voices = abbott.getProperty('voices')

abbott.setProperty('rate', 175)
abbott.setProperty('voice', voices[2].id)


# Speech Recognition
text = ''
recognizer = speech_recognition.Recognizer()
# Function Definitions:

# Quit function to stop program when prompted
def quit(inp):
    if inp == 'shut down':
        abbott.say("Powering down, have a nice day")
        abbott.runAndWait()
        return True



# Function to check for wake word and end up calling speaking()
def check_for_wake(string):

    wake_word_list = ["hey abbott", "abbott"]
    for word in wake_word_list:

        regex = re.search(word, string)

        if regex != None:
            return True
    return False


# Function for chat gpt responses and assistant like behavior
def speaking():

    abbott.say("Hello, what can I do for you today")
    abbott.runAndWait()
#Figure out how to wait a long time to capture input, but as soon as input is captured and there is no more
#speaking then stop the recording and answer the prompt

    while True:

        try:
            audio = recognizer.record(mic, duration=5)
            text = recognizer.recognize_google(audio, language='en-IN')
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



chat_log = []
# Main program loop
while True:

    try:

        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.record(mic, duration=3)

            text = recognizer.recognize_google(audio, language='en-IN')
            text = text.lower()

            if check_for_wake(text):
                speaking()

            if quit(text):
                break


    except Exception as e:
        recognizer = speech_recognition.Recognizer()
        continue
