import code
from connectors.connection import DbConnection
from data_objects.sites import Warehouse
import os
from psycopg2 import extras
from readers.reader import Reader

class WarehouseReader(Reader):
    def __init__(self, user, password, host, port):
        self.connection = DbConnection(user, password, host, port)
        self.query = ""

    def build_query(self):
        query = f"""
        SELECT site.warehouse_id as name,
                st_astext(site.coords) as location,
                company_info.onboarding_time__days_ as onboarding_period,
                site.available_freezer_capacity__sq_ft_ as inventory_capacity,
                ((site.cost_per_sq_ft_of_storage_per_week__gbp_ / 7) / 2) as storage_cost_per_kg
        FROM distribution_warehouses as site
        INNER JOIN distribution_companies as company_info
            ON site.company_name = company_info.company_name
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        return [Warehouse(**restaurant) for restaurant in restaurants]
    

if __name__ == '__main__':
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    reader = WarehouseReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(locals=locals())