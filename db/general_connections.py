import pymysql.cursors
from abc import ABC, abstractmethod


class DBTable(ABC):
    __connection = pymysql.connect(host='localhost',
                                   user='jainshailesh91',
                                   password='shailujain123',
                                   db='jarvis',
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def select(cls, table_name: str, what: str = "*", condition: str = 1):
        sql = "SELECT " + what + " FROM " + table_name + " WHERE " + str(condition)
        print(sql)
        with cls.__connection.cursor() as cursor:
            cursor.execute(sql)
        result = cursor.fetchall()
        return result

    @classmethod
    def execute_query(cls, sql):
        with cls.__connection.cursor() as cursor:
            cursor.execute(sql)
        cls.__connection.commit()

    @classmethod
    @abstractmethod
    def insert(cls, tuple_of_values):
        pass
