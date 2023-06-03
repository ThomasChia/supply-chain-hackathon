from connectors.connection import DbConnection
from data_objects.sites import Restaurant
from readers.reader import Reader

class RestaurantReader(Reader):
    def __init__(self, filters=[]):
        super().__init__()
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters
        self.data = []

    def run(self):
        self.build_query()
        self.read_query()

    def build_query(self):
        query = f"""
        SELECT id,
               name,
               nearest_city as location,
               restaurant_demand,
               current_stock,
               daily_total_demand,
               daily_profit,
               fixed_cost,
               description,
               lat,
               long
        FROM retaurant
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        self.data = [Restaurant(**restaurant) for restaurant in restaurants]