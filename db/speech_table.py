from db.general_connections import *


class SpeechTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO speech (intent_id, speech_text, speech_keywords) VALUES (%d, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, tuple_of_values)
        connection.commit()
