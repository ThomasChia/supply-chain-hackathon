import code
from connectors.connection import DbConnection
from data_objects.flows import WarehouseRestaurantDistance
import os
from psycopg2 import extras
from readers.reader import Reader

class WarehouseRestaurantDistanceReader(Reader):
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
        SELECT concat(warehouse_id, ', ', farm_restaurant_id) as route_tuple,
                distance_meters / 1000 as distance
        FROM warehouse_to_far_rest_mapping
        WHERE farm_restaurant_id ilike 'R%'
        """
        self.query = query

    def read_query(self):
        warehouse_restaurant_distance = self.connection.reader(self.query)
        for distance in warehouse_restaurant_distance:
            distance['route_tuple'] = tuple(distance['route_tuple'].split(', '))
        self.data = [WarehouseRestaurantDistance(**distance) for distance in warehouse_restaurant_distance]


if __name__ == '__main__':
    reader = WarehouseRestaurantDistanceReader()
    reader.build_query()
    warehouse_restaurant_distances = reader.read_query()

    code.interact(local=locals())