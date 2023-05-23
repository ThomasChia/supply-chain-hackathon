import code
from connectors.connection import DbConnection
from data_objects.sites import Warehouse
from readers.reader import Reader

class WarehouseReader(Reader):
    def __init__(self, user, password, host, port):
        self.connection = DbConnection(user, password, host, port)
        self.query = ""

    def build_query(self):
        query = f"""
        SELECT site.name,
                site.coords,
                site.'onboarding_time__days_' as onboarding_period,
                site.'available_freezer_capacity__sq_ft' as inventory_capacity,
                ((site.'cost_per_sq_ft_of_storage_per_week__gbp_' / 7) / 2) as storage_cost_per_kg
        FROM distribution_warehouses
        INNER JOIN distribution_companies
            ON distribution_warehouses.company_name = distribution_companies.company_name
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        return [Warehouse(**restaurant) for restaurant in restaurants]
    

if __name__ == '__main__':
    reader = WarehouseReader()
    reader.build_query()
    warehouses = reader.read_query()

    code.interact(locals=locals())