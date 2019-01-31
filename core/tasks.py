from pynput.keyboard import Controller


class Tasks:

    def __init__(self):
        self.keyboard = Controller()
        self.intent = ""
        self.entity = ""
        self.intent_action_mapping = {
            "open": self.open,
            "type": self.type
        }

    def execute(self, intent, entity):
        self.intent = intent
        self.entity = entity
        try:
            self.intent_action_mapping[self.intent]
        except KeyError as e:
            raise e


    def open(self):
        pass

    def type(self):
        self.keyboard.type(self.entity)
