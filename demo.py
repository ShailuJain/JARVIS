

def open_entity():
    print("OPen")


def type_entity():
    print("Type")


intent_action_mapping = {
            "open": open_entity,
            "type": type_entity
        }

intent_action_mapping['hello']
