import code
from connectors.connection import DbConnection
from data_objects.sites import Warehouse
import os
from psycopg2 import extras
from readers.reader import Reader

class WarehouseReader(Reader):
    def __init__(self, filters=[]):
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters
        self.data = []

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        query = f"""
        SELECT warehouse.name as name,
               warehouse.city as location,
               distributor.onboarding_time as onboarding_period,
               warehouse_transient.freezer_cap_sq_ft as inventory_capacity,
               ((warehouse_transient.storage_cost_sq_ft / 7) / 2) as storage_cost_per_kg,
               warehouse.lat as lat,
               warehouse.long as long
        FROM warehouse
        LEFT JOIN distributor ON warehouse.distributor_id = distributor.id
        LEFT JOIN warehouse_transient ON warehouse_transient.name = warehouse.name
        WHERE distributor.is_active = TRUE
        """
        self.query = query

    def read_query(self):
        warehouses = self.connection.reader(self.query)
        self.data = [Warehouse(**warehouse) for warehouse in warehouses]

class WarehouseIDReader(Reader):
    def __init__(self, distributors):
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.distributors = distributors
        self.data = []

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        distributor_list = super().list_to_sql(self.distributors)
        distributor_filter = '' if distributor_list == '' else f"WHERE distributor.id in {distributor_list}"
        query = f"""
        SELECT warehouse.name
        FROM warehouse
        LEFT JOIN distributor
        ON warehouse.distributor_id = distributor.id
        {distributor_filter}
        """
        self.query = query

    def read_query(self):
        warehouse_ids = self.connection.reader(self.query)
        self.data = [warehouse_id for warehouse_id in warehouse_ids]
    

if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = WarehouseReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(local=locals())