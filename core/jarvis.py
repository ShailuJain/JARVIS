from wit import Wit
from speech_recognition import *
import pyttsx3
from pynput import keyboard
from math import ceil
from db import speech_table
from db.intent_table import get_intent_name
from helpers.date_time import DateTimeFunctions
from core.tasks import Tasks


class SpeechListener:

    def __init__(self):
        self.recognizer = Recognizer()
        self.mic = Microphone()
        self.WIT_API_KEY = "HKK55NQXIRC7ZFVL2FPCE2JZQNVMCIDR"
        self.wit = Wit(self.WIT_API_KEY)
        self.isMicUsed = False
        self.func_to_stop_listen = None

    def listen_and_get_speech(self, cb):
        if not self.isMicUsed:
            self.isMicUsed = True
            self.func_to_stop_listen = self.recognizer.listen_in_background(self.mic, cb)

    def get_response_from_wit(self, speech_text):
        assert isinstance(speech_text, str)
        return str(self.wit.message(speech_text))

    def __del__(self):
        self.func_to_stop_listen(True)


class Jarvis:

    class JarvisVoice:

        engine = None
        rate = None

        def __init__(self, rate=150):
            self.rate = rate

        # def say(self, lock, text_):
        #     lock.acquire()
        #     print("inside say")
        #     self.engine.setProperty('rate', self.rate)
        #     self.engine.say(text_)
        #     self.engine.runAndWait()
        #     print("after run and wait")
        #     lock.release()
        #     print("lock released")

        def say(self, text_):
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', self.rate)
            self.engine.say(text_)
            self.engine.runAndWait()
            del self.engine

        def set_rate(self, rate):
            self.rate = rate

    def __init__(self):
        self.tasks = Tasks()
        self.activate_code = "1"
        self.deactivate_code = "0"
        self.speech_recognition_factor = 0.6
        self.greeted = False
        self.isStarted = False
        self.speech_listener = None
        self.jarvis_voice = None

    def set_activate_code(self, key):
        self.activate_code = key[0]

    def set_deactivate_code(self, key):
        self.deactivate_code = key[0]

    def speak(self, text):
        self.jarvis_voice.say(text)

    def start(self):
        def on_key_release(key):
            key = str(key).replace("'", "")
            if (self.activate_code == key) and (not self.isStarted):
                self.isStarted = True
                self.start_jarvis()
            elif (self.deactivate_code == key) and self.isStarted:
                self.isStarted = False
                self.stop_jarvis()
        with keyboard.Listener(on_release=on_key_release) as listener:
            listener.join()

    def listen(self):
        self.speech_listener.listen_and_get_speech(self.process_speech_callback)

    def process_speech_callback(self, recognizer, audio_data):
            try:
                speech = recognizer.recognize_wit(audio_data, self.speech_listener.WIT_API_KEY)
                self.interpret_and_execute(speech)
            except RequestError:
                self.speak("Please check your internet connection, Shailesh!")
            except UnknownValueError:
                self.speak("Sorry sir, i cannot understand")

    def greet(self):
        self.speak(DateTimeFunctions.get_current_time_greet() + " Shailesh, How can i help")

    def repeat(self, command):
        self.speak(command)

    def stop_jarvis(self):
        self.speak("Good bye sir!")
        del(self.jarvis_voice, self.speech_listener)

    def start_jarvis(self):
        self.speech_listener = SpeechListener()
        self.jarvis_voice = self.JarvisVoice()
        if not self.greeted:
            self.greet()
            self.greeted = True
        self.listen()

    def get_intent_and_entity(self, speech):
        count = 0
        result = speech_table.select()
        intent_id = -1
        entity = ""
        for i in range(len(result)):
            row = result[i]
            speech_keywords = str(row['speech_keywords']).split(",")
            for keyword in speech_keywords:
                if speech.__contains__(keyword):
                    count += 1
            if count >= ceil(len(speech_keywords) * self.speech_recognition_factor):
                intent_id = row['intent_id']
                break
        intent_name = get_intent_name(intent_id)
        entity = str(speech).replace(intent_name, "")
        return intent_name, entity

    def interpret_and_execute(self, speech):
        intent, entity = self.get_intent_and_entity(speech)
        try:
            self.tasks.execute(intent, entity)
        except KeyError as e:
            self.speak("Sorry, ")
