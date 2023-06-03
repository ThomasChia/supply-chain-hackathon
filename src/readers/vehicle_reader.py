import code
from connectors.connection import DbConnection
from data_objects.vehicles import Vehicle
import os
from psycopg2 import extras
from readers.reader import Reader

class VehicleReader(Reader):
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
        SELECT depot.name as company,
               vehicle.type as name,
               depot.locations as locations,
               logisticcs.no_available as number_available,
               logisticcs.capacity_tonnes_ * 1000 as capacity,
               logisticcs.price_per_tonne / 1000 as cost_per_kg_per_km,
               vehicle.emissions_per_kg_km as co2_emissions_per_kg_per_km
        FROM logisticcs
        LEFT JOIN depot ON logisticcs.depot_id = depot.id
        LEFT JOIN vehicle ON logisticcs.vehicle_id = vehicle.id
        WHERE logisticcs.no_available > 0
        AND depot.is_active = TRUE
        """
        self.query = query

    def read_query(self):
        vehicles = self.connection.reader(self.query)
        self.data = [Vehicle(**vehicle) for vehicle in vehicles]


if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = VehicleReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(local=locals())