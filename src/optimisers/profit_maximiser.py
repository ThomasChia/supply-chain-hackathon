from data_objects.flows import Distance, SupplierWarehouseDistance, WarehouseRestaurantDistance
from mapper import RouteCostMapper, VehicleCostMapper
from pulp import LpProblem, LpVariable, lpSum, LpMaximize
from data_objects.sites import Vendor, Warehouse, Restaurant
from typing import List
from data_objects.vehicles import Vehicle

class SupplyChainProfitMaximiser:
    CHICKEN_PRICE = 11.5

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
        self.supplier_warehouse_mapper = RouteCostMapper(supplier_warehouse_distances)
        self.warehouse_restaurant_mapper = RouteCostMapper(warehouse_restaurant_distances)
        self.vehicle_mapper = VehicleCostMapper(vehicles)
        self.problem = LpProblem("SupplyChainProfitMaximiser", LpMaximize)
        self.supply = LpVariable.dicts("supply", [(v.name, w.name) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
        self.distribution = LpVariable.dicts("distribution", [(w.name, r.name) for w in warehouses for r in restaurants], lowBound=0, cat="Integer")
        self.supplier_warehouse_logistics = LpVariable.dicts("supplier_warehouse_logistics", [(v.name, w.name, ve.company, ve.name) for v in vendors for w in warehouses for ve in vehicles], lowBound=0, cat="Integer")
        self.warehouse_restaurant_logistics = LpVariable.dicts("warehouse_restaurant_logistics", [(w.name, r.name, ve.company, ve.name) for w in warehouses for r in restaurants for ve in vehicles], lowBound=0, cat="Integer")

    def get_daily_chicken_sales(self):
        return lpSum(self.distribution[(w.name, r.name)] * self.CHICKEN_PRICE for w in self.warehouses for r in self.restaurants)
    
    def get_daily_non_chicken_sales(self):
        return lpSum(r.daily_total_demand - r.daily_chicken_demand for r in self.restaurants)
    
    def get_supply_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * v.cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_supply_to_warehouse_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_storage_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * w.storage_cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_warehouse_to_restaurant_cost(self):
        return lpSum(self.distribution[(w.name, r.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)
    
    def get_restaurant_fixed_costs(self):
        return lpSum(r.fixed_cost for r in self.restaurants)
    
    # def get_restaurant_revenue(self):
    #     return lpSum(self.distribution[(w.name, r.name)] * r.daily_profit for w in self.warehouses for r in self.restaurants)
    
    def get_co2_emissions_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles) + \
                lpSum(self.distribution[(w.name, r.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)
    
    def get_supply_to_warehouse_co2_emissions_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_to_restaurant_co2_emissions_cost(self):
        return lpSum(self.distribution[(w.name, r.name)] * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for w in self.warehouses for r in self.restaurants for ve in self.vehicles)

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
        self.problem += lpSum(self.supply[(vendor.name, w.name)] for w in self.warehouses)  <= vendor.capacity

    def add_vendor_logistics_constraint(self, vendor: Vendor, warehouse: Warehouse):
        '''
        Constraint for each vendor and warehouse combination their supply must be below the associated logistics capacity.
        '''
        self.problem += lpSum(self.supply[(vendor.name, warehouse.name)]) <= lpSum(self.supplier_warehouse_logistics[(vendor.name, warehouse.name, ve.company, ve.name)] * ve.capacity for ve in self.vehicles)

    def add_warehouse_capacity_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors) <= warehouse.inventory_capacity

    def add_warehouse_supply_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.distribution[(warehouse.name, r.name)] for r in self.restaurants) <= lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors)

    def add_warehouse_logistics_constraint(self, warehouse: Warehouse, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(warehouse.name, restaurant.name)]) <= lpSum(self.warehouse_restaurant_logistics[(warehouse.name, restaurant.name, ve.company, ve.name)] * ve.capacity for ve in self.vehicles)

    def add_restaurant_demand_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name)] for w in self.warehouses) >= restaurant.restaurant_demand

    def add_restaurant_stock_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name)] for w in self.warehouses) <= restaurant.daily_chicken_demand * 3

    def add_vehicle_number_availability_constraints_supplier_warehouse(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between suppliers and warehouses is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.supplier_warehouse_logistics[(v.name, w.name, ve.company, ve.name)] for v in vendors for w in warehouses) >= ve.number_available

    def add_vehicle_number_availability_constraints_warehouse_restaurant(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between warehouses and restaurants is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.warehouse_restaurant_logistics[(w.name, r.name, ve.company, ve.name)] for w in warehouses for r in restaurants) >= ve.number_available

    def print_results(self):
        if self.problem.status == 1:
            for v in self.vendors:
                for w in self.warehouses:
                    if self.supply[(v.name, w.name)].varValue > 0:
                        print(f"Supply {self.supply[(v.name, w.name)].varValue} units from {v.name} at a cost of {self.supply[(v.name, w.name)].varValue * v.cost_per_kg} and delivered to warehouse {w.name}.")
                        print(f"Inventory at warehouse {w.name} is {self.supply[(v.name, w.name)].varValue} units at a cost of {self.supply[(v.name, w.name)].varValue * w.storage_cost_per_kg}.")

                        for ve in self.vehicles:
                            print(f"Transport costs of {self.supply[(v.name, w.name)].varValue * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

            for w in self.warehouses:
                for r in self.restaurants:
                    if self.distribution[(w.name, r.name)].varValue > 0:
                        # print(f"Distribution {self.distribution[(w.name, r.name)]varValue} units from {w.name} to {r.name} at a cost of {self.distribution[(w.name, r.name)].varValue * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name]}.")

                        for ve in self.vehicles:
                            print(f"Transport costs of {self.distribution[(w.name, r.name)].varValue * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")
             
            restaurant_sales = {}
            for r in self.restaurants:
                restaurant_sales[r.name] = 0
                for w in self.warehouses:
                    if self.distribution[(w.name, r.name)].varValue > 0:
                        restaurant_sales[r.name] += self.distribution[(w.name, r.name)].varValue
            
            for r in restaurant_sales.keys():
                print(f"Daily chicken sales for {r} are {restaurant_sales[r]}.")   

            # self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)] for v in self.vendors for w in self.warehouses for ve in self.vehicles
            for v in self.vendors:
                for w in self.warehouses:
                    for ve in self.vehicles:
                        print(f"CO2 emissions of {self.supply[(v.name, w.name)].varValue * self.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

            for w in self.warehouses:
                for r in self.restaurants:
                    for ve in self.vehicles:
                        print(f"CO2 emissions of {self.distribution[(w.name, r.name)].varValue * self.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")            

            print(f"Total cost: {self.problem.objective.value()}")
        else:
            print("No optimal solution found.")

    def solve(self):
        total_profit = (
            self.get_daily_chicken_sales() +
            self.get_daily_non_chicken_sales() -
            self.get_supply_cost() -
            self.get_supply_to_warehouse_cost() -
            self.get_warehouse_storage_cost() -
            self.get_warehouse_to_restaurant_cost() -
            self.get_restaurant_fixed_costs()
        )
        #     self.get_supply_to_warehouse_co2_emissions_cost() +
        #     self.get_warehouse_to_restaurant_co2_emissions_cost()
        self.problem += total_profit

        self.add_vendor_constraints()
        self.add_warehouse_constraints()
        self.add_restaurant_constraints()
        self.add_vendor_warehouse_constraints()
        self.add_warehouse_restaurant_constraints()
        self.add_vehicle_constraints()

        self.problem.solve()

        self.print_results()


if __name__ == "__main__":
    vendors = [
        Vendor(name="Vendor A",
               location='London', 
               capacity=1200, 
               additional_capacity=1000, 
               sla_period=2, 
               onboarding_period=3, 
               cost_per_kg=0.4, 
               co2_emissions_per_kg=0.1),
        Vendor("Vendor B", 'Paris', 800, 1000, 2, 3, 0.6, 0.2),
        Vendor("Vendor C", 'Berlin', 1500, 1000, 2, 3, 0.3, 0.1),
        Vendor("Vendor D", 'Madrid', 1000, 1000, 2, 3, 0.5, 0.15),
        Vendor("Vendor E", 'Rome', 900, 1000, 2, 3, 0.7, 0.25)
    ]

    warehouses = [
        Warehouse("Warehouse 1", 'London', 2, 20, 1),
        Warehouse("Warehouse 2", 'Paris', 3, 1500, 2),
        Warehouse("Warehouse 3", 'Berlin', 5, 3000, 3),
    ]

    restaurants = [
        Restaurant(name="Restaurant 1",
                   location='Madrid',
                   restaurant_demand=800,
                   current_stock=600, 
                   daily_chicken_demand=300, 
                   daily_total_demand=400, 
                   daily_profit=100,
                   fixed_cost=50),
        Restaurant("Restaurant 2", 'Rome', 1200, 700, 200, 500, 150, 55),
    ]

    vehicles = [
        Vehicle(company="Cluck Logistics", 
                name="Class III Diesel Refrigerated Van", 
                location="London", 
                number_available=10, 
                capacity=1000, 
                cost_per_tonne_per_km=10, 
                co2_emissions_per_tonne_per_km=1),
        Vehicle("Cluck Logistics", "Deisel HGV Refrigerated Rigid", "London", 11, 1500, 15, 0.5),
        Vehicle("Cluck Logistics", "Deisel HGV Refrigerated Articulated", "Madrid", 12, 2000, 20, 0.6),
        Vehicle("Cluck Logistics", "Refrigerated Electric Van", "Berlin", 13, 2500, 25, 0.2),
        Vehicle("Feather Express", "Class III Diesel Refrigerated Van", "Paris", 14, 1200, 12, 0.4),
        Vehicle("Feather Express", "Deisel HGV Refrigerated Rigid", "Amsterdam", 15, 1700, 17, 0.5),
        Vehicle("Feather Express", "Deisel HGV Refrigerated Articulated", "Moscow", 15, 2200, 22, 0.6),
        Vehicle("Feather Express", "Refrigerated Electric Van", "Dublin", 13, 2700, 27, 0.2),
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

    supply_chain_optimizer = SupplyChainProfitMaximiser(vendors=vendors,
                                                        warehouses=warehouses,
                                                        restaurants=restaurants,
                                                        vehicles=vehicles,
                                                        supplier_warehouse_distances=supplier_warehouse_costs,
                                                        warehouse_restaurant_distances=warehouse_restaurant_costs)
    
    supply_chain_optimizer.solve()
