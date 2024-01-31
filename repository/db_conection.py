import psycopg2


class Conn:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='decanat', user='decanat',
                                     password='decanat', host='localhost')

    def exec_sql(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)

                self.conn.commit()

                return True
        except Exception as e:
            print(e)
            return False

    def exec_select_sql(self, sql):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)

                self.conn.commit()

                return cursor.fetchall()
        except Exception as e:
            print(e)
            return []
