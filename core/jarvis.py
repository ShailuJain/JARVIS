from speech_recognition import *
import pyttsx3
from pynput import keyboard
from math import ceil
from db.tables import *
from helpers.date_time import DateTimeFunctions
from helpers.tasks import Tasks


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

    class JarvisEar:

        def __init__(self):
            self.recognizer = Recognizer()
            self.mic = Microphone()
            self.CLIENT_ID = "MlhdPdxE9BfyE__TnrjIgw=="
            self.CLIENT_KEY = "mpIolTcUrVBtofW_qTP-JgIogzVWUPxB4hGg5Dy_SkrzK4PeliSoaJ0M-q3NumOUyZ9MdqKSbiiHvy2jQLYqsw=="
            self.API_KEY = "HKK55NQXIRC7ZFVL2FPCE2JZQNVMCIDR"
            self.isMicUsed = False
            self.func_to_stop_listen = None

        def listen_and_get_speech(self, cb):
            if not self.isMicUsed:
                print("Listening")
                self.isMicUsed = True
                self.func_to_stop_listen = self.recognizer.listen_in_background(self.mic, cb)

        # def get_response_from_wit(self, speech_text):
        #     assert isinstance(speech_text, str)
        #     return str(self.wit.message(speech_text))

        def __del__(self):
            self.func_to_stop_listen(True)

    def __init__(self):
        self.tasks = Tasks(self)
        self.activate_code = "1"
        self.deactivate_code = "0"
        self.speech_recognition_factor = 0.6
        self.greeted = False
        self.isStarted = False
        self.jarvis_ear = None
        self.jarvis_voice = None
        self.isTypingModeOn = False
        self.intents_entities = {}
        self.modes = ("typing_mode", "reading_mode")

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
        self.jarvis_ear.listen_and_get_speech(self.process_speech_callback)

    def process_speech_callback(self, recognizer, audio_data):
            try:
                # speech = recognizer.recognize_houndify(audio_data,
                #                                        client_id=self.speech_listener.CLIENT_ID,
                #                                        client_key=self.speech_listener.CLIENT_KEY
                #                                        )
                speech = recognizer.recognize_wit(audio_data, self.jarvis_ear.API_KEY)
                # speech = recognizer.recognize_google(audio_data)
                speech = str(speech).lower()
                self.interpret_and_execute(speech)
            except RequestError as e:
                self.speak(e)
            except UnknownValueError as e:
                # self.speak(RepliesTable.get_random_reply("error"))
                print(e)

    def greet(self):
        self.speak(DateTimeFunctions.get_current_time_greet() + " Shailesh, How can i help")

    def repeat(self, command):
        self.speak(command)

    def stop_jarvis(self):
        self.speak("Good bye sir!")
        del(self.jarvis_voice, self.jarvis_ear)

    def start_jarvis(self):
        self.jarvis_ear = self.JarvisEar()
        self.jarvis_voice = self.JarvisVoice()
        if not self.greeted:
            # self.greet()
            self.greeted = True
        self.listen()

    def get_intents_and_entities(self, speech):
        result = SpeechTable.select(what="intent_id, speech_keywords")
        print("res:", result, "speech:", speech)
        intent_names = []
        intent_entity = {}
        for i in range(len(result)):
            row = result[i]
            speech_keywords = str(row['speech_keywords']).split(",")
            if self.intent_matches_speech(speech_keywords, speech):
                intent_id = row['intent_id']
                intent_names.append(IntentTable.get_intent_name(intent_id))
        print(intent_names)
        for i in range(len(intent_names)):
            intent_name = intent_names[i]
            index_curr_intent = str(speech).find(intent_name) + len(intent_name)
            if i == len(intent_names)-1:
                index_next_intent = None
            else:
                next_intent_name = intent_names[i+1]
                index_next_intent = str(speech).find(next_intent_name)
            intent_entity[intent_name.strip()] = speech[index_curr_intent:index_next_intent].strip()
        return intent_entity

    def interpret_and_execute(self, speech):
        if self.isTypingModeOn:
            self.intents_entities.clear()
            self.intents_entities['type'] = speech
        else:
            self.intents_entities = self.get_intents_and_entities(speech)
            print(self.intents_entities)
        try:
            self.tasks.execute(self.intents_entities)
        except KeyError as e:
            self.speak(RepliesTable.get_random_reply("error"))

    def intent_matches_speech(self, speech_keywords, speech):
        count = 0
        for keyword in speech_keywords:
            if speech.__contains__(keyword):
                count += 1
        if count >= ceil(len(speech_keywords) * self.speech_recognition_factor):
            return True
        return False

