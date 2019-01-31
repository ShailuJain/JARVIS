from db.general_connections import *


def insert(tuple_of_values):
    assert isinstance(tuple_of_values, tuple)
    sql = "INSERT INTO users (name, gender, authority) VALUES (%s, %s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, tuple_of_values)
    connection.commit()
