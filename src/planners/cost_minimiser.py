from data_objects.flows import SupplierWarehouseDistance, WarehouseRestaurantDistance
from data_objects.sites import Vendor, Warehouse, Restaurant
from data_objects.vehicles import Vehicle
import logging
from optimisers.optimiser import SupplyChainOptimisation
from optimisers.profit_maximiser import SupplyChainProfitMaximiser
import os
from output.outputter import OptimisationOutputter, JSONOutputter
from output.output import SupplyChain
from readers.restaurant_reader import RestaurantReader
from readers.supplier_warehouse_distances_reader import SupplierWarehouseDistanceReader
from readers.vehicle_reader import VehicleReader
from readers.vendor_reader import VendorReader
from readers.warehouse_reader import WarehouseReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader
from readers.warehouse_restaurant_distances_reader import WarehouseRestaurantDistanceReader
import time
from typing import List

logger = logging.getLogger(__name__)

class CostMinimiserPlanner:
    USER = os.getenv('CSCUSER')
    PASSWORD = os.getenv('CSCPASSWORD')
    HOST = os.getenv('CSCHOST')
    PORT = os.getenv('CSCPORT')

    def __init__(self,
                #  vendors_input,
                #  warehouses_input,
                #  restaurants_input,
                #  vehicles_input,
                #  supplier_warehouse_distance_input,
                #  warehouse_restaurant_distance_input
                 ):
        self.vendors_input: List[Vendor] = None
        self.warehouses_input: List[Warehouse] = None
        self.restaurants_input: List[Restaurant] = None
        self.vehicles_input: List[Vehicle] = None
        self.supplier_warehouse_distance_input: List[SupplierWarehouseDistance] = None
        self.warehouse_restaurant_distance_input: List[WarehouseRestaurantDistance] = None
        self.vendors = []
        self.warehouses = []
        self.restaurants = []
        self.vehicles = []
        self.supplier_warehouse_distance = []
        self.warehouse_restaurant_distance = []
        self.supply_chain: SupplyChain = None
        self.json_output = None

    def run(self):
        self.get_data()
        self.optimise()
        if self.optimiser.problem.status != 1:
            self.loose_optimise()
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
        self.optimiser = SupplyChainProfitMaximiser(vendors=self.vendors,
                                                    warehouses=self.warehouses,
                                                    restaurants=self.restaurants,
                                                    vehicles=self.vehicles,
                                                    supplier_warehouse_distances=self.supplier_warehouse_distance,
                                                    warehouse_restaurant_distances=self.warehouse_restaurant_distance)
    
        self.optimiser.solve()

    def create_output(self):
        logger.info("Building output.")
        outputter = OptimisationOutputter(optimiser=self.optimiser)
        self.supply_chain = outputter.create_table_output()
        self.supply_chain.get_totals()

        supply_chain_plan = self.supply_chain.plan_to_list()
        json_outputter = JSONOutputter(supply_chain_plan=supply_chain_plan,
                                       vendors=self.vendors,
                                       warehouses=self.warehouses,
                                       restaurants=self.restaurants)
        self.json_output = json_outputter.create_json()
