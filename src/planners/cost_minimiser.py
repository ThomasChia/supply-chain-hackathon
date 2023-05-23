from optimisers.optimiser import SupplyChainOptimisation
import os
from readers.restaurant_reader import RestaurantReader
from readers.supplier_warehouse_distances_reader import SupplierWarehouseDistanceReader
from readers.vehicle_reader import VehicleReader
from readers.vendor_reader import VendorReader
from readers.warehouse_reader import WarehouseReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader

class CostMinimiserPlanner:
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    def __init__(self,
                 vendors_input,
                 warehouses_input,
                 restaurants_input,
                 vehicles_input,
                 supplier_warehouse_distance_input,
                 warehouse_restaurant_distance_input):
        self.vendors_input = vendors_input
        self.warehouses_input = warehouses_input
        self.restaurants_input = restaurants_input
        self.vehicles_input = vehicles_input
        self.supplier_warehouse_distance_input = supplier_warehouse_distance_input
        self.warehouse_restaurant_distance_input = warehouse_restaurant_distance_input

    def run(self):
        pass

    def get_data(self):
        vendors = VendorReader()


# USER = os.getenv('CSCUSER')
# PASSWORD = os.getenv('CSCPASSWORD')
# HOST = os.getenv('CSCHOST')
# PORT = os.getenv('CSCPORT')

# reader = WarehouseRestaurantDistanceReader(user=USER,
#                          password=PASSWORD, 
#                          host=HOST, 
#                          port=PORT)
# reader.build_query()
# warehouse_restaurant_distance = reader.read_query()