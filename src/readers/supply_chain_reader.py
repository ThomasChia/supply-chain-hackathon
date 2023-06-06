from connectors.connection import DbConnection
from psycopg2 import extras
from output.output import Edge, SupplyChain, TotalOutput
from readers.reader import Reader


class SupplyChainReader(Reader):
    def __init__(self, filters=[]):
        super().__init__()
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters
        self.data: SupplyChain = None

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        query = f"""
        SELECT geometry,
               properties,
               metrics
        FROM planopt
        """
        self.query = query

    def read_query(self):
        supply_chain = self.connection.reader(self.query)
        metrics = [TotalOutput(**link['metrics']) for link in supply_chain[:1]]
        self.data = SupplyChain([Edge(**link['properties']) for link in supply_chain])
        self.data.metrics = metrics[0]