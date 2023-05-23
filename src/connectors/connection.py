import code
import os
import psycopg2
from psycopg2 import extras
from  sqlalchemy.engine import Engine
from sqlalchemy import create_engine


class DbConnection(object):
    _db_name = 'csc'

    def __init__(self, user, password, host, port):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.cursor = self.connect()

    def connect(self):
        conn = psycopg2.connect(
            database=self._db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
            )
        return conn.cursor(cursor_factory=extras.RealDictCursor)
    
    def reader(self, query_string=None):
        self.cursor.execute(query_string)
        data = self.cursor.fetchall()
        self.cursor.close()
        return data
    

if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    connection = DbConnection(user=USER,
                              password=PASSWORD,
                              host=HOST,
                              port=PORT)
    
    query = """
    SELECT *
    FROM chicken_restaurants
    """

    data = connection.reader(query)

    code.interact(local=locals())