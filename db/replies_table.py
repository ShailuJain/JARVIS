from db.general_connections import *


class RepliesTable(DBTable):

    @classmethod
    def insert(cls, tuple_of_values):
        assert isinstance(tuple_of_values, tuple)
        sql = "INSERT INTO replies (reply_intent, reply_text) VALUES (%s, %s)"
        with cls.connection.cursor() as cursor:
            cursor.execute(sql, tuple_of_values)
            cls.connection.commit()

    @classmethod
    def select(cls, table_name: str = "replies", condition: str = 1):
        return super(RepliesTable, cls).select(table_name, condition)

    @classmethod
    def select_with_reply_intent(cls, reply_intent):
        return cls.select("reply_intent="+str(reply_intent))
