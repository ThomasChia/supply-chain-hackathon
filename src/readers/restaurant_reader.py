from connectors.connection import DbConnection
from data_objects.sites import Restaurant
from readers.reader import Reader

class RestaurantReader(Reader):
    def __init__(self, filters=[]):
        super().__init__()
        self.connection = DbConnection(Reader.USER, Reader.PASSWORD, Reader.HOST, Reader.PORT)
        self.query = ""
        self.filters = filters

    def build_query(self):
        query = f"""
        SELECT location.name,
                location.coords,
                'demand.Fried Chicken Sold Daily(kg)' as restaurant_demand,
                'demand.Current Stock of Raw Chicken (kgs)' as current_stock,
                'demand.Restaurant Total Daily Sales(£)' as daily_total_demand,
                'demand.Restaurant Daily Profits(£)' as daily_profit,
                'demand.Restaurant fixed costs(£)' as fixed_cost
        FROM chicken_restaurants as location
        INNER JOIN chicken_restaurants_demand as demand
            ON chicken_restaurants.id = chicken_restaurants_demand.id
        """
        self.query = query

    def read_query(self):
        restaurants = self.connection.reader(self.query)
        return [Restaurant(**restaurant) for restaurant in restaurants]