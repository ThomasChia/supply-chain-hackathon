import code
from connectors.connection import DbConnection
from data_objects.flows import SupplierWarehouseDistance
import os
from psycopg2 import extras
from readers.reader import Reader

class SupplierWarehouseDistanceReader(Reader):
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
        SELECT concat(farm_restaurant_id, ', ', warehouse_id) as route_tuple,
                distance_meters / 1000 as distance
        FROM warehouse_to_far_rest_mapping
        WHERE farm_restaurant_id ilike 'F%'
        """
        self.query = query

    def read_query(self):
        supplier_warehouse_distance = self.connection.reader(self.query)
        for distance in supplier_warehouse_distance:
            distance['route_tuple'] = tuple(distance['route_tuple'].split(', '))
        self.data = [SupplierWarehouseDistance(**distance) for distance in supplier_warehouse_distance]


if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = SupplierWarehouseDistanceReader()
    reader.build_query()
    supplier_warehouse_distances = reader.read_query()

    code.interact(local=locals())