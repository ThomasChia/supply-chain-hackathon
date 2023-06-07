from abc import ABC
from connectors.connection import DbConnection
import os


class Reader(ABC):
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')
    
    def __init__(self):
        self.USER = os.getenv('CSCUSER')
        self.PASSWORD = os.getenv('CSCPASSWORD')
        self.HOST = os.getenv('CSCHOST')
        self.PORT = os.getenv('CSCPORT')

    def list_to_sql(self, l)->str:
        if len(l) > 0:
            l = [str(i) for i in l]
            return "('"+"', '".join(l)+"')"
        else:
            return ''

    def get_connection(self):
        pass

    def read_query(self, query):
        pass