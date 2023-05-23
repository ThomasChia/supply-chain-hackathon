import psycopg2
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
        return conn.cursor()
    
    def reader(self, query_string=None):
        self.cursor.execute(query_string)
        data = self.cursor.fetchall()
        return data