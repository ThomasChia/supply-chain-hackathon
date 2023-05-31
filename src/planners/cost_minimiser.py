import logging
from optimisers.optimiser import SupplyChainOptimisation
import os
from output.outputter import OptimisationOutputter
from readers.restaurant_reader import RestaurantReader
from readers.supplier_warehouse_distances_reader import SupplierWarehouseDistanceReader
from readers.vehicle_reader import VehicleReader
from readers.vendor_reader import VendorReader
from readers.warehouse_reader import WarehouseReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader
import time

logger = logging.getLogger(__name__)

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
        if self.optimiser.problem.status != 1:
            pass
        self.create_output()

    def get_data(self):
        vendors = VendorReader(self.vendors_input)
        vendors.run()
        self.vendors = vendors.data
        logger.info(f"Read {len(self.vendors)} vendors from db.")

        warehouses = WarehouseReader(self.warehouses_input)
        warehouses.run()
        self.warehouses = warehouses.data
        logger.info(f"Read {len(self.warehouses)} warehouses from db.")

        restaurants = RestaurantReader(self.restaurants_input)
        restaurants.run()
        self.restaurants = restaurants.data
        logger.info(f"Read {len(self.restaurants)} restaurants from db.")

        vehicles = VehicleReader(self.vehicles_input)
        vehicles.run()
        self.vehicles = vehicles.data
        logger.info(f"Read {len(self.vehicles)} vehicles from db.")

        supplier_warehouse_distances = SupplierWarehouseDistanceReader(self.supplier_warehouse_distance_input)
        supplier_warehouse_distances.run()
        self.supplier_warehouse_distance = supplier_warehouse_distances.data

        warehouse_restaurant_distances = WarehouseRestaurantDistanceReader(self.warehouse_restaurant_distance_input)
        warehouse_restaurant_distances.run()
        self.warehouse_restaurant_distance = warehouse_restaurant_distances.data

        logger.info("Read all data.")

    def optimise(self):
        self.optimiser = SupplyChainOptimisation(vendors=self.vendors,
                                                 warehouses=self.warehouses,
                                                 restaurants=self.restaurants,
                                                 vehicles=self.vehicles,
                                                 supplier_warehouse_distances=self.supplier_warehouse_distance,
                                                 warehouse_restaurant_distances=self.warehouse_restaurant_distance)
    
        self.optimiser.solve()

    def loose_optimise(self):
        pass

    def create_output(self):
        logger.info("Building output.")
        outputter = OptimisationOutputter(optimiser=self.optimiser)
        outputter.create_table_output()
