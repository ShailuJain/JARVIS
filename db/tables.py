import random

from db.general_connections import *


class IntentTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO intents (intent_name, intent_action) VALUES (%s, %s)" % tuple_of_values
        super(IntentTable, cls).execute_query(sql)

    @classmethod
    def select(cls, table_name: str = "intents", what: str = "*", condition: str = 1):
        return super(IntentTable, cls).select(table_name, what, condition)

    @classmethod
    def get_intent_name(cls, intent_id):
        result = cls.select(what="intent_name", condition="intent_id=" + str(intent_id))
        if result:
            return result[0]['intent_name']
        return "error"


class RepliesTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO replies (reply_intent, reply_text) VALUES (%s, %s)" % tuple_of_values
        super(RepliesTable, cls).execute_query(sql)

    @classmethod
    def select(cls, table_name: str = "replies", what: str = "*", condition: str = 1):
        return super(RepliesTable, cls).select(table_name, what, condition)

    @classmethod
    def get_random_reply(cls, reply_type):
        result = cls.select(what="reply_text", condition="reply_type='" + str(reply_type) + "'")
        try:
            if result:
                return result[random.randrange(0, len(result))]['reply_text']
            else:
                return cls._get_error_reply()
        except Exception:
            return cls._get_error_reply()

    @classmethod
    def _get_error_reply(cls):
        result = cls.select(what="reply_text", condition="reply_type='error'")
        if result:
            return result[random.randrange(0, len(result))]['reply_text']


class SpeechTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO speech (intent_id, speech_text, speech_keywords) VALUES (%d, %s, %s)" % tuple_of_values
        super(SpeechTable, cls).execute_query(sql)

    @classmethod
    def select(cls, table_name: str = "speech", what: str = "*", condition: str = 1):
        return super(SpeechTable, cls).select(table_name, what, condition)


class UsersTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO users (name, gender, authority) VALUES (%s, %s, %s)" % tuple_of_values
        super(UsersTable, cls).execute_query(sql)

    @classmethod
    def select(cls, table_name: str = "users", what: str = "*", condition: str = 1):
        return super(UsersTable, cls).select(table_name, what, condition)
