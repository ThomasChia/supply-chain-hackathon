from connectors.connection import DbConnection
from abc import ABC


class Reader(ABC):
    def __init__(self):
        pass

    def get_connection(self):
        pass

    def read_query(self, query):
        pass