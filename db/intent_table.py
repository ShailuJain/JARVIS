from db.general_connections import *


class IntentTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO intents (intent_name, intent_action) VALUES (%s, %s)"
        with cls.connection.cursor() as cursor:
            cursor.execute(sql, tuple_of_values)
            cls.connection.commit()

    @classmethod
    def select(cls, table_name: str = "intents", condition: str = 1):
        return super(IntentTable, cls).select(table_name, condition)

    @classmethod
    def get_intent_name(cls, intent_id):
        result = cls.select("intent_id=" + str(intent_id))
        if result:
            return result[0]['intent_name']
        return "error"
