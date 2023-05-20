from flows import Cost, SupplierWarehouseCost, WarehouseRestaurantCost
from mapper import RouteCostMapper
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from sites import Vendor, Warehouse, Restaurant
from typing import List

class SupplyChainOptimisation:
    def __init__(self,
                 vendors: List[Vendor],
                 warehouses: List[Warehouse], 
                 restaurants: List[Restaurant], 
                 supplier_warehouse_costs: List[SupplierWarehouseCost], 
                 warehouse_restaurant_costs: List[WarehouseRestaurantCost]):
        self.vendors = vendors
        self.warehouses = warehouses
        self.restaurants = restaurants
        self.supplier_warehouse_mapper = RouteCostMapper(supplier_warehouse_costs)
        self.warehouse_restaurant_mapper = RouteCostMapper(warehouse_restaurant_costs)
        self.problem = LpProblem("SupplyChainOptimization", LpMinimize)
        self.supply = LpVariable.dicts("supply", [(v.name, w.name) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
        self.distribution = LpVariable.dicts("distance", [(w.name, r.name) for w in warehouses for r in restaurants], lowBound=0, cat="Integer")

    def get_supply_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * v.cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_supply_to_warehouse_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * self.supplier_warehouse_mapper.mapping[v.name, w.name] for v in self.vendors for w in self.warehouses)
    
    def get_warehouse_storage_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * w.storage_cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_warehouse_to_restaurant_cost(self):
        return lpSum(self.distribution[(w.name, r.name)] * self.warehouse_restaurant_mapper.mapping[w.name, r.name] for w in self.warehouses for r in self.restaurants)

    def add_vendor_constraints(self):
        for v in self.vendors:
            self.add_vendor_limit_constraint(v)

    def add_warehouse_constraints(self):
        for w in self.warehouses:
            self.add_warehouse_capacity_constraint(w)
            self.add_warehouse_supply_constraint(w)

    def add_restaurant_constraints(self):
        for r in self.restaurants:
            self.add_restaurant_demand_constraint(r)

    def add_vendor_limit_constraint(self, vendor: Vendor):
        self.problem += lpSum(self.supply[(vendor.name, w.name)] for w in self.warehouses)  <= vendor.capacity

    def add_warehouse_capacity_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors) <= warehouse.inventory_capacity

    def add_warehouse_supply_constraint(self, warehouse: Warehouse):
        self.problem += lpSum(self.distribution[(warehouse.name, r.name)] for r in self.restaurants) <= lpSum(self.supply[(v.name, warehouse.name)] for v in self.vendors)

    def add_restaurant_demand_constraint(self, restaurant: Restaurant):
        self.problem += lpSum(self.distribution[(w.name, restaurant.name)] for w in self.warehouses) >= restaurant.restaurant_demand

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

        self.problem.solve()

        self.print_results()


if __name__ == "__main__":
    vendors = [
        Vendor("Vendor A", 1200, 0.4, 'London'),
        Vendor("Vendor B", 800, 0.6, 'Paris'),
        Vendor("Vendor C", 1500, 0.3, 'Berlin'),
        Vendor("Vendor D", 1000, 0.5, 'Madrid'),
        Vendor("Vendor E", 900, 0.7, 'Rome'),
    ]

    warehouses = [
        Warehouse("Warehouse 1", 2000, 1, 'London'),
        Warehouse("Warehouse 2", 1500, 2, 'Paris'),
        Warehouse("Warehouse 3", 3000, 3, 'Berlin'),
    ]

    restaurants = [
        Restaurant("Restaurant 1", 800, 'Madrid'),
        Restaurant("Restaurant 2", 1200, 'Rome'),
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

    supply_chain_optimizer = SupplyChainOptimisation(vendors,
                                                     warehouses,
                                                     restaurants,
                                                     supplier_warehouse_costs,
                                                     warehouse_restaurant_costs)
    
    supply_chain_optimizer.solve()
