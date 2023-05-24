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
        SELECT logistics.company_name as company,
                logistics.vehicle as name,
                logistics.locations as locations,
                logistics.no___available as number_available,
                logistics.capacity__tonnes_ as capacity,
                logistics.price_per_tonne___km__gbp_ as cost_per_tonne_per_km,
                co2_emissions.co2_emissions__kwh_tkm_ as co2_emissions_per_tonne_per_km
        FROM logistics
        LEFT JOIN co2_emissions
        ON logistics.vehicle = co2_emissions.vehicle_type
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