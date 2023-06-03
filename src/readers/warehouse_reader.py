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
               warehouse.lon as lon
        FROM warehouse
        LEFT JOIN distributor ON warehouse.distributor_id = distributor.id
        LEFT JOIN warehouse_transient ON warehouse_transient.name = warehouse.name
        WHERE warehouse.is_active = TRUE
        """
        self.query = query

    def read_query(self):
        warehouses = self.connection.reader(self.query)
        self.data = [Warehouse(**warehouse) for warehouse in warehouses]
    

if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = WarehouseReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(local=locals())