from pynput.keyboard import Controller, Key
import re
special_char_mappings = {
    'comma': ',',
    'full stop': '.',
    'dot': '.',
    'colon': ':',
    'semicolon': ';',
    'semi colon': ';',
    'exclamation': '!',
    'at the rate': '@',
    'hash': '#',
    'percent': '%',
    'dollar': '$',
    'ampersand': '&',
    'multiply': '*',
    'plus': '+',
    'minus': '-',
    'left round bracket': '(',
    'right round bracket': ')',
    'left square bracket': '[',
    'right square bracket': ']',
    'left curly bracket': '{',
    'right curly bracket': '}',
    'left angle bracket': '<',
    'right angle bracket': '>',
    'double quote': '"',
    'single quote': "'",
    'back slash': r'\\',
    'forward slash': '/',
    'question mark': '?',
    'space': ' ',
    'underscore': '_',
}
shortcut_keys_mapping = {
    'control': Key.ctrl,
    'left control': Key.ctrl_l,
    'right control': Key.ctrl_r,
    'shift': Key.shift,
    'left shift': Key.shift_l,
    'right shift': Key.shift_r,
    'alt': Key.alt,
    'left alt': Key.alt_l,
    'right alt': Key.alt_r,
    'up': Key.up,
    'down': Key.down,
    'left': Key.left,
    'right': Key.right,
    'enter': Key.enter,
    'backspace': Key.backspace,
    'delete': Key.delete
}


class Tasks:

    def __init__(self, jarvis):
        self.jarvis = jarvis
        self.keyboard = Controller()
        self.intents_entities = {}
        self.intent_action_mapping = {
            "open": self.open,
            "type": self.type,
            "press": self.press,
            "turn_on": self.turn_on,
        }

    def execute(self, intents_entities):
        for intent in intents_entities:
            try:
                self.intent_action_mapping[intent](intents_entities[intent])
            except KeyError as e:
                raise e
            except Exception as e:
                raise e

    def open(self, entity):
        pass

    def turn_on(self, entity):
        modes = self.__get_jarvis_modes(entity)

    def type(self, entity):
        entity = self.__change_entity_speech(entity)
        self.keyboard.type(entity)

    def press(self, entity):
        lst = entity.split(" ")
        try:
            for key in lst:
                self.keyboard.press(shortcut_keys_mapping[key])
        except KeyError as e:
            raise e

    def __change_entity_speech(self, entity):
        if entity:
            entity = str(entity).replace("raw ", "raw")
            for symbol in special_char_mappings:
                temp = re.sub(r"\b%s\b" % symbol, special_char_mappings[symbol], entity)
                if temp:
                    entity = temp
            temp = re.sub(r"\braw (.*?)\b", r"\1", entity)
        return temp

    def __get_jarvis_modes(self, entity):
        all_available_modes = self.jarvis.modes
        for mode in all_available_modes:
            pass
        return all_available_modes

