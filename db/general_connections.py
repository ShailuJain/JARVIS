import pymysql.cursors


class DBTable:
    connection = pymysql.connect(host='localhost',
                                 user='jainshailesh91',
                                 password='shailujain123',
                                 db='core',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def select(cls, table_name: str, condition: str = 1):
        sql = "SELECT * FROM %s WHERE " + str(condition)
        print(sql)
        with cls.connection.cursor() as cursor:
            cursor.execute(sql, table_name)
        result = cursor.fetchall()
        return result

    
