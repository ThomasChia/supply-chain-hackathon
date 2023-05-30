from data_objects.flows import Distance, SupplierWarehouseDistance, WarehouseRestaurantDistance
from data_objects.vehicles import Vehicle
import logging
from mapper import RouteCostMapper, VehicleCostMapper, SupplierCostMapper, WarehouseCostMapper
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from data_objects.sites import Vendor, Warehouse, Restaurant
import time
from typing import List

logger = logging.getLogger(__name__)

class SupplyChainOptimisation:
    def __init__(self,
                 vendors: List[Vendor],
                 warehouses: List[Warehouse], 
                 restaurants: List[Restaurant],
                 vehicles: List[Vehicle], 
                 supplier_warehouse_distances: List[SupplierWarehouseDistance], 
                 warehouse_restaurant_distances: List[WarehouseRestaurantDistance]):
        self.vendors = vendors
        self.warehouses = warehouses
        self.restaurants = restaurants
        self.vehicles = vehicles
        self.supplier_cost_mapper = SupplierCostMapper(vendors)
        self.warehouse_cost_mapper = WarehouseCostMapper(warehouses)
        self.supplier_warehouse_mapper = RouteCostMapper(supplier_warehouse_distances)
        self.warehouse_restaurant_mapper = RouteCostMapper(warehouse_restaurant_distances)
        self.vehicle_mapper = VehicleCostMapper(vehicles)
        self.problem = LpProblem("SupplyChainOptimization", LpMinimize)
        # supply is the amount of supply from each supplier to each warehouse
        self.supply = LpVariable.dicts("supply", [(v.name, w.name, ve.company, ve.name) for v in vendors for w in warehouses for ve in vehicles], lowBound=0, cat='Continuous')
        # distibution is the amount of chicken sent from each warehouse to each restaurant
        self.distribution = LpVariable.dicts("distribution", [(w.name, r.name, ve.company, ve.name) for w in warehouses for r in restaurants for ve in vehicles], lowBound=0, cat="Integer")

    def get_supply_cost(self):
        return lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] * v.cost_per_kg for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_supply_to_warehouse_cost(self):
        return lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_storage_cost(self):
        return lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] * w.storage_cost_per_kg for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_to_restaurant_cost(self):
        return lpSum(self.distribution[(w.name, r.name, ve.company, ve.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)
    
    def get_co2_emissions_cost(self):
        return lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles) + \
                lpSum(self.distribution[(w.name, r.name, ve.company, ve.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)
    
    def get_supply_to_warehouse_co2_emissions_cost(self):
        return lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_to_restaurant_co2_emissions_cost(self):
        return lpSum(self.distribution[(w.name, r.name, ve.company, ve.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)

    def add_vendor_constraints(self):
        for v in self.vendors:
            self.add_vendor_limit_constraint(v)

    def add_warehouse_constraints(self):
        for w in self.warehouses:
            self.add_warehouse_capacity_constraint(w)
            self.add_warehouse_supply_constraint(w)

    def add_vendor_warehouse_constraints(self):
        for v in self.vendors:
            for w in self.warehouses:
                self.add_vendor_logistics_constraint(v, w)

    def add_restaurant_constraints(self):
        for r in self.restaurants:
            self.add_restaurant_demand_constraint(r)

    def add_warehouse_restaurant_constraints(self):
        for w in self.warehouses:
            for r in self.restaurants:
                self.add_warehouse_logistics_constraint(w, r)

    def add_vehicle_constraints(self):
        for ve in self.vehicles:
            self.add_vehicle_number_availability_constraints_supplier_warehouse(ve)
            self.add_vehicle_number_availability_constraints_warehouse_restaurant(ve)

    def add_vendor_limit_constraint(self, vendor: Vendor):
        self.problem += lpSum(self.supply[(vendor.name, w.name, ve.company, ve.name)] for w in self.warehouses for ve in self.vehicles)  <= vendor.capacity

    def add_vendor_logistics_constraint(self, vendor: Vendor, warehouse: Warehouse):
        '''
        Constraint for each vendor and warehouse combination their supply must be below the associated logistics capacity.
        '''
        self.problem += lpSum(self.supply[(vendor.name, warehouse.name, ve.company, ve.name)] for ve in self.vehicles) <= lpSum(self.supply[(vendor.name, warehouse.name, ve.company, ve.name)] * ve.capacity for ve in self.vehicles)

    def add_warehouse_capacity_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.supply[(v.name, warehouse.name, ve.company, ve.name)] for v in self.vendors for ve in self.vehicles) <= warehouse.inventory_capacity

    def add_warehouse_supply_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.distribution[(warehouse.name, r.name, ve.company, ve.name)] for r in self.restaurants for ve in self.vehicles) <= lpSum(self.supply[(v.name, warehouse.name, ve.company, ve.name)] for v in self.vendors for ve in self.vehicles)

    def add_warehouse_logistics_constraint(self, warehouse: Warehouse, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(warehouse.name, restaurant.name, ve.company, ve.name)] for ve in self.vehicles) <= lpSum(self.distribution[(warehouse.name, restaurant.name, ve.company, ve.name)] * ve.capacity for ve in self.vehicles)

    def add_restaurant_demand_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name, ve.company, ve.name)] for w in self.warehouses for ve in self.vehicles) >= restaurant.restaurant_demand

    def add_restaurant_stock_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name, ve.company, ve.name)] for w in self.warehouses for ve in self.vehicles) <= restaurant.restaurant_demand * 3

    def add_vehicle_number_availability_constraints_supplier_warehouse(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between suppliers and warehouses is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.supply[(v.name, w.name, ve.company, ve.name)] for v in self.vendors for w in self.warehouses) >= ve.number_available

    def add_vehicle_number_availability_constraints_warehouse_restaurant(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between warehouses and restaurants is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.distribution[(w.name, r.name, ve.company, ve.name)] for w in self.warehouses for r in self.restaurants) >= ve.number_available

    def print_results(self):
        if self.problem.status == 1:
            for v in self.vendors:
                for w in self.warehouses:
                    for ve in self.vehicles:
                        if self.supply[(v.name, w.name, ve.company, ve.name)].varValue > 0:
                            logger.info(f"Supply {self.supply[(v.name, w.name, ve.company, ve.name)].varValue} units from {v.name} at a cost of {self.supply[(v.name, w.name, ve.company, ve.name)].varValue * v.cost_per_kg} and delivered to warehouse {w.name}.")
                            logger.info(f"Inventory at warehouse {w.name} is {self.supply[(v.name, w.name, ve.company, ve.name)].varValue} units at a cost of {self.supply[(v.name, w.name, ve.company, ve.name)].varValue * w.storage_cost_per_kg}.")
                            logger.info(f"Transport costs of {self.supply[(v.name, w.name, ve.company, ve.name)].varValue * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

            for w in self.warehouses:
                for r in self.restaurants:
                    for ve in self.vehicles:
                        if self.distribution[(w.name, r.name, ve.company, ve.name)].varValue > 0:
                            logger.info(f"Transport costs of {self.distribution[(w.name, r.name, ve.company, ve.name)].varValue * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")

            for v in self.vendors:
                for w in self.warehouses:
                    for ve in self.vehicles:
                        if self.supply[(v.name, w.name, ve.company, ve.name)].varValue > 0:
                            logger.info(f"CO2 emissions of {self.supply[(v.name, w.name, ve.company, ve.name)].varValue * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

            for w in self.warehouses:
                for r in self.restaurants:
                    for ve in self.vehicles:
                        if self.distribution[(w.name, r.name, ve.company, ve.name)].varValue > 0:
                            logger.info(f"CO2 emissions of {self.distribution[(w.name, r.name, ve.company, ve.name)].varValue * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")            

            logger.info(f"Total cost: {self.problem.objective.value()}")
        else:
            logger.warning("No optimal solution found.")

    def solve(self):
        logger.info("Building optimisation problem.")
        total_cost = (
            self.get_supply_cost() + 
            self.get_supply_to_warehouse_cost() +
            self.get_warehouse_storage_cost() +
            self.get_warehouse_to_restaurant_cost() +
            self.get_supply_to_warehouse_co2_emissions_cost() +
            self.get_warehouse_to_restaurant_co2_emissions_cost()
        )
        self.problem += total_cost

        self.add_vendor_constraints()
        self.add_warehouse_constraints()
        self.add_restaurant_constraints()
        self.add_vendor_warehouse_constraints()
        self.add_warehouse_restaurant_constraints()
        self.add_vehicle_constraints()

        logger.info(f"Solving optimisation for {len(self.problem._variables)} variables and {len(self.problem.constraints)} constraints.")
        start_time = time.time()

        self.problem.solve()

        end_time = time.time()
        logger.info(f"Optimiser solved in {end_time - start_time}.")


if __name__ == "__main__":
    vendors = [
        Vendor(name="Vendor A",
               company="Company A",
               location='London', 
               capacity=1200, 
               additional_capacity=1000, 
               sla_period=2, 
               onboarding_period=3, 
               cost_per_kg=0.4, 
               co2_emissions_per_kg=0.1),
        Vendor("Vendor B", "Company B", 'Paris', 800, 1000, 2, 3, 0.6, 0.2),
        Vendor("Vendor C", "Company C", 'Berlin', 1500, 1000, 2, 3, 0.3, 0.1),
        Vendor("Vendor D", "Company D", 'Madrid', 1000, 1000, 2, 3, 0.5, 0.15),
        Vendor("Vendor E", "Company E", 'Rome', 900, 1000, 2, 3, 0.7, 0.25)
    ]

    warehouses = [
        Warehouse("Warehouse 1", 'London', 2, 20, 1),
        Warehouse("Warehouse 2", 'Paris', 3, 1500, 2),
        Warehouse("Warehouse 3", 'Berlin', 5, 3000, 3),
    ]

    restaurants = [
        Restaurant("Restaurant 1", 'Madrid', 800, 600, 300, 400, 50),
        Restaurant("Restaurant 2", 'Rome', 1200, 700, 200, 500, 55),
    ]

    vehicles = [
        Vehicle(company="Cluck Logistics", 
                name="Class III Diesel Refrigerated Van", 
                locations=["London"], 
                number_available=10, 
                capacity=1000, 
                cost_per_kg_per_km=10, 
                co2_emissions_per_kg_per_km=1),
        Vehicle("Cluck Logistics", "Deisel HGV Refrigerated Rigid", ["London"], 11, 1500, 15, 0.5),
        Vehicle("Cluck Logistics", "Deisel HGV Refrigerated Articulated", ["Madrid"], 12, 2000, 20, 0.6),
        Vehicle("Cluck Logistics", "Refrigerated Electric Van", ["Berlin"], 13, 2500, 25, 0.2),
        Vehicle("Feather Express", "Class III Diesel Refrigerated Van", ["Paris"], 14, 1200, 12, 0.4),
        Vehicle("Feather Express", "Deisel HGV Refrigerated Rigid", ["Amsterdam"], 15, 1700, 17, 0.5),
        Vehicle("Feather Express", "Deisel HGV Refrigerated Articulated", ["Moscow"], 15, 2200, 22, 0.6),
        Vehicle("Feather Express", "Refrigerated Electric Van", ["Dublin"], 13, 2700, 27, 0.2),
    ]

    supplier_warehouse_costs = [
        SupplierWarehouseDistance((vendors[0].name, warehouses[0].name), 1),
        SupplierWarehouseDistance((vendors[0].name, warehouses[1].name), 2),
        SupplierWarehouseDistance((vendors[0].name, warehouses[2].name), 3),
        SupplierWarehouseDistance((vendors[1].name, warehouses[0].name), 4),
        SupplierWarehouseDistance((vendors[1].name, warehouses[1].name), 5),
        SupplierWarehouseDistance((vendors[1].name, warehouses[2].name), 6),
        SupplierWarehouseDistance((vendors[2].name, warehouses[0].name), 13),
        SupplierWarehouseDistance((vendors[2].name, warehouses[1].name), 2),
        SupplierWarehouseDistance((vendors[2].name, warehouses[2].name), 10),
        SupplierWarehouseDistance((vendors[3].name, warehouses[0].name), 9),
        SupplierWarehouseDistance((vendors[3].name, warehouses[1].name), 7),
        SupplierWarehouseDistance((vendors[3].name, warehouses[2].name), 5),
        SupplierWarehouseDistance((vendors[4].name, warehouses[0].name), 4),
        SupplierWarehouseDistance((vendors[4].name, warehouses[1].name), 2),
        SupplierWarehouseDistance((vendors[4].name, warehouses[2].name), 1)
    ]

    warehouse_restaurant_costs = [
        WarehouseRestaurantDistance((warehouses[0].name, restaurants[0].name), 1),
        WarehouseRestaurantDistance((warehouses[0].name, restaurants[1].name), 2),
        WarehouseRestaurantDistance((warehouses[1].name, restaurants[0].name), 3),
        WarehouseRestaurantDistance((warehouses[1].name, restaurants[1].name), 4),
        WarehouseRestaurantDistance((warehouses[2].name, restaurants[0].name), 5),
        WarehouseRestaurantDistance((warehouses[2].name, restaurants[1].name), 6),
    ]

    supply_chain_optimizer = SupplyChainOptimisation(vendors=vendors,
                                                     warehouses=warehouses,
                                                     restaurants=restaurants,
                                                     vehicles=vehicles,
                                                     supplier_warehouse_distances=supplier_warehouse_costs,
                                                     warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    supply_chain_optimizer.solve()
