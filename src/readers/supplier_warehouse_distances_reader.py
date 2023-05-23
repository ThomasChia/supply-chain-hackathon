import code
from connectors.connection import DbConnection
from data_objects.flows import SupplierWarehouseDistance
import os
from psycopg2 import extras
from readers.reader import Reader

class SupplierWarehouseDistanceReader(Reader):
    def __init__(self, user, password, host, port):
        self.connection = DbConnection(user, password, host, port)
        self.query = ""

    def build_query(self):
        query = f"""
        SELECT concat(farm_restaurant_id, ', ', warehouse_id) as route_tuple,
                distance_meters as distance
        FROM warehouse_to_far_rest_mapping
        """
        self.query = query

    def read_query(self):
        supplier_warehouse_distance = self.connection.reader(self.query)
        for distance in supplier_warehouse_distance:
            distance['route_tuple'] = tuple(distance['route_tuple'].split(', '))
        return [SupplierWarehouseDistance(**distance) for distance in supplier_warehouse_distance]


if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = SupplierWarehouseDistanceReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(locals=locals())