from flows import Cost, SupplierWarehouseCost, WarehouseRestaurantCost
from mapper import RouteCostMapper, VehicleCostMapper
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from sites import Vendor, Warehouse, Restaurant
from typing import List
from vehicles import Vehicle

class SupplyChainOptimisation:
    def __init__(self,
                 vendors: List[Vendor],
                 warehouses: List[Warehouse], 
                 restaurants: List[Restaurant],
                 vehicles: List[Vehicle], 
                 supplier_warehouse_costs: List[SupplierWarehouseCost], 
                 warehouse_restaurant_costs: List[WarehouseRestaurantCost]):
        self.vendors = vendors
        self.warehouses = warehouses
        self.restaurants = restaurants
        self.vehicles = vehicles
        self.supplier_warehouse_mapper = RouteCostMapper(supplier_warehouse_costs)
        self.warehouse_restaurant_mapper = RouteCostMapper(warehouse_restaurant_costs)
        self.vehicle_mapper = VehicleCostMapper(vehicles)
        self.problem = LpProblem("SupplyChainOptimization", LpMinimize)
        self.supply = LpVariable.dicts("supply", [(v.name, w.name) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
        self.distribution = LpVariable.dicts("distribution", [(w.name, r.name) for w in warehouses for r in restaurants], lowBound=0, cat="Integer")
        self.supplier_warehouse_logistics = LpVariable.dicts("supplier_warehouse_logistics", [(v.name, w.name, ve.name) for v in vendors for w in warehouses for ve in vehicles], lowBound=0, cat="Integer")
        self.warehouse_restaurant_logistics = LpVariable.dicts("warehouse_restaurant_logistics", [(w.name, r.name, ve.name) for w in warehouses for r in restaurants for ve in vehicles], lowBound=0, cat="Integer")

    def get_supply_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * v.cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_supply_to_warehouse_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.mapping[v.name, w.name] * self.vehicle_mapper.mapping[ve.name] for v in self.vendors for w in self.warehouses for ve in self.vehicles)
    
    def get_warehouse_storage_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * w.storage_cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_warehouse_to_restaurant_cost(self):
        return lpSum(self.distribution[(w.name, r.name)] * self.warehouse_restaurant_mapper.mapping[w.name, r.name] for w in self.warehouses for r in self.restaurants)
    
    def get_co2_emissions_cost(self):
        pass
        # return lpSum(self.)
    
    def get_supply_to_warehouse_co2_emissions_cost(self):
        pass

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

    def add_vehicle_constraints(self):
        for ve in self.vehicles:
            self.add_vehicle_number_availability_constraints_supplier_warehouse(ve)

    def add_vendor_limit_constraint(self, vendor: Vendor):
        self.problem += lpSum(self.supply[(vendor.name, w.name)] for w in self.warehouses)  <= vendor.capacity

    def add_vendor_logistics_constraint(self, vendor: Vendor, warehouse: Warehouse):
        '''
        Constraint for each vendor and warehouse combination their supply must be below the associated logistics capacity.
        '''
        self.problem += lpSum(self.supply[(vendor.name, warehouse.name)]) <= lpSum(self.supplier_warehouse_logistics[(vendor.name, warehouse.name, ve.name)] * ve.capacity for ve in self.vehicles)

    def add_warehouse_capacity_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors) <= warehouse.inventory_capacity

    def add_warehouse_supply_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.distribution[(warehouse.name, r.name)] for r in self.restaurants) <= lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors)

    def add_restaurant_demand_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name)] for w in self.warehouses) >= restaurant.restaurant_demand

    def add_vehicle_number_availability_constraints_supplier_warehouse(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between suppliers and warehouses is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.supplier_warehouse_logistics[(v.name, w.name, ve.name)] for v in vendors for w in warehouses) >= ve.number_available

    def add_vehicle_number_availability_constraints_warehouse_restaurant(self, ve: Vehicle):
        '''
        Constraint to ensure the number of vehicles used between warehouses and restaurants is less than or equal to the number of vehicles available.
        '''
        self.problem += lpSum(self.warehouse_restaurant_logistics[(w.name, r.name, ve.name)] for w in warehouses for r in restaurants) >= ve.number_available

    def print_results(self):
        if self.problem.status == 1:  # "Optimal" status code
            # Print the optimal solution
            for v in self.vendors:
                for w in self.warehouses:
                    if self.supply[(v.name, w.name)].varValue > 0:
                        print(f"Supply {self.supply[(v.name, w.name)].varValue} units from {v.name} at a cost of {self.supply[(v.name, w.name)].varValue * v.cost_per_kg} and delivered to warehouse {w.name}.")
                        print(f"Transport costs of {self.supply[(v.name, w.name)].varValue * self.supplier_warehouse_mapper.mapping[v.name, w.name]} from {v.name} to {w.name}.")

            for w in self.warehouses:
                for r in self.restaurants:
                    if self.distribution[(w.name, r.name)].varValue > 0:
                        print(f"Distribution {self.distribution[(w.name, r.name)].varValue} units from {w.name} to {r.name} at a cost of {self.distribution[(w.name, r.name)].varValue * self.warehouse_restaurant_mapper.mapping[w.name, r.name]}.")

            for v in self.vendors:
                for w in self.warehouses:
                    for ve in self.vehicles:
                        if self.supplier_warehouse_logistics[(v.name, w.name, ve.name)].varValue > 0:
                            print(f"Transport {self.supplier_warehouse_logistics[(v.name, w.name, ve.name)].varValue} units from {v.name} to {w.name} using {ve.name} at a cost of {self.supplier_warehouse_logistics[(v.name, w.name, ve.name)].varValue * ve.cost_per_tonne_per_km}.")

            print(f"Total cost: {self.problem.objective.value()}")
        else:
            print("No optimal solution found.")

    def solve(self):
        total_cost = (
            self.get_supply_cost() + 
            self.get_supply_to_warehouse_cost() +
            self.get_warehouse_storage_cost() +
            self.get_warehouse_to_restaurant_cost()
        )
        self.problem += total_cost

        self.add_vendor_constraints()
        self.add_warehouse_constraints()
        self.add_restaurant_constraints()
        self.add_vendor_warehouse_constraints()

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
        Warehouse("Warehouse 1", 'London', 2, 2000, 1),
        Warehouse("Warehouse 2", 'Paris', 1500, 2, 150),
        Warehouse("Warehouse 3", 'Berlin', 3000, 3, 200),
    ]

    restaurants = [
        Restaurant("Restaurant 1", 'Madrid', 800, 600, 300, 400, 100, 50),
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
        SupplierWarehouseCost((vendors[0].name, warehouses[0].name), 1),
        SupplierWarehouseCost((vendors[0].name, warehouses[1].name), 2),
        SupplierWarehouseCost((vendors[0].name, warehouses[2].name), 3),
        SupplierWarehouseCost((vendors[1].name, warehouses[0].name), 4),
        SupplierWarehouseCost((vendors[1].name, warehouses[1].name), 5),
        SupplierWarehouseCost((vendors[1].name, warehouses[2].name), 6),
        SupplierWarehouseCost((vendors[2].name, warehouses[0].name), 13),
        SupplierWarehouseCost((vendors[2].name, warehouses[1].name), 2),
        SupplierWarehouseCost((vendors[2].name, warehouses[2].name), 10),
        SupplierWarehouseCost((vendors[3].name, warehouses[0].name), 9),
        SupplierWarehouseCost((vendors[3].name, warehouses[1].name), 7),
        SupplierWarehouseCost((vendors[3].name, warehouses[2].name), 5),
        SupplierWarehouseCost((vendors[4].name, warehouses[0].name), 4),
        SupplierWarehouseCost((vendors[4].name, warehouses[1].name), 2),
        SupplierWarehouseCost((vendors[4].name, warehouses[2].name), 1)
    ]

    warehouse_restaurant_costs = [
        WarehouseRestaurantCost((warehouses[0].name, restaurants[0].name), 1),
        WarehouseRestaurantCost((warehouses[0].name, restaurants[1].name), 2),
        WarehouseRestaurantCost((warehouses[1].name, restaurants[0].name), 3),
        WarehouseRestaurantCost((warehouses[1].name, restaurants[1].name), 4),
        WarehouseRestaurantCost((warehouses[2].name, restaurants[0].name), 5),
        WarehouseRestaurantCost((warehouses[2].name, restaurants[1].name), 6),
    ]

    supply_chain_optimizer = SupplyChainOptimisation(vendors=vendors,
                                                     warehouses=warehouses,
                                                     restaurants=restaurants,
                                                     vehicles=vehicles,
                                                     supplier_warehouse_costs=supplier_warehouse_costs,
                                                     warehouse_restaurant_costs=warehouse_restaurant_costs)
    
    supply_chain_optimizer.solve()
