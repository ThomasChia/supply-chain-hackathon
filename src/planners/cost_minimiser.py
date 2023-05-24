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
        self.vendors = []
        self.warehouses = []
        self.restaurants = []
        self.vehicles = []
        self.supplier_warehouse_distance = []
        self.warehouse_restaurant_distance = []

    def run(self):
        self.get_data()
        self.optimise()

    def get_data(self):
        vendors = VendorReader(self.vendors_input)
        vendors.run()
        self.vendors = vendors.data

        warehouses = WarehouseReader(self.warehouses_input)
        warehouses.run()
        self.warehouses = warehouses.data

        restaurants = RestaurantReader(self.restaurants_input)
        restaurants.run()
        self.restaurants = restaurants.data

        vehicles = VehicleReader(self.vehicles_input)
        vehicles.run()
        self.vehicles = vehicles.data

        supplier_warehouse_distances = SupplierWarehouseDistanceReader(self.supplier_warehouse_distance_input)
        supplier_warehouse_distances.run()
        self.supplier_warehouse_distance = supplier_warehouse_distances.data

        warehouse_restaurant_distances = WarehouseRestaurantDistanceReader(self.warehouse_restaurant_distance_input)
        warehouse_restaurant_distances.run()
        self.warehouse_restaurant_distance = warehouse_restaurant_distances.data

    def optimise(self):
        supply_chain_optimizer = SupplyChainOptimisation(vendors=self.vendors,
                                                         warehouses=self.warehouses,
                                                         restaurants=self.restaurants,
                                                         vehicles=self.vehicles,
                                                         supplier_warehouse_distances=self.supplier_warehouse_distance,
                                                         warehouse_restaurant_distances=self.warehouse_restaurant_distance)
        supply_chain_optimizer.solve()