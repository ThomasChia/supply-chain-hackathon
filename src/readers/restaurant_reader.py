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
        SELECT location.id as name,
                st_astext(location.coords) as location,
                demand.fried_chicken_sold_daily_kg_ as restaurant_demand,
                demand.current_stock_of_raw_chicken__kgs_ as current_stock,
                demand.restaurant_total_daily_sales_gbp_ as daily_total_demand,
                demand.restaurant_daily_profits_gbp_ as daily_profit,
                demand.restaurant_fixed_costs_gbp_ as fixed_cost
        FROM chicken_restaurants as location
        INNER JOIN chicken_restaurants_demand as demand
            ON location.id = demand.restaurant_id
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        self.data = [Restaurant(**restaurant) for restaurant in restaurants]