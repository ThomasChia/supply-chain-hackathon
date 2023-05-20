from flows import SupplierWarehouseCost, WarehouseRestaurantCost
from pulp import LpProblem, LpVariable, lpSum, LpMinimize
from sites import Vendor, Warehouse, Restaurant
from typing import List

class SupplyChainOptimization:
    def __init__(self,
                 vendors: List[Vendor],
                 warehouses: List[Warehouse], 
                 restaurants: List[Restaurant], 
                 distance_costs: List[DistanceCost], 
                 distribution_costs: List[DistributionCost]):
        self.vendors = vendors
        self.warehouses = warehouses
        self.restaurants = restaurants
        self.distance_costs = distance_costs
        self.distribution_costs = distribution_costs
        self.problem = LpProblem("SupplyChainOptimization", LpMinimize)
        self.supply = LpVariable.dicts("supply", [(v.name, w.name) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
        self.distribution = LpVariable.dicts("distance", [(w.name, r.name) for w in warehouses for r in restaurants], lowBound=0, cat="Integer")

    def get_supply_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * v.cost_per_kg for v in self.vendors for w in self.warehouses)
    
    def get_supply_to_warehouse_cost(self):
        return lpSum(self.supply[(v.name, w.name)] * distance_cost.cost)
        # return lpSum(self.supply[(v, w)] * distance_cost.cost for v in self.vendors for w in self.warehouses for distance_cost in self.distance_costs if distance_cost.vendor == v and distance_cost.warehouse == w)
    
    def get_warehouse_to_restaurant_cost(self):
        return lpSum(self.distribution[(w.name, r.name)] * w.storage_cost_per_kg for w in self.warehouses for r in self.restaurants)

    def add_distribution_cost(self, distribution_cost):
        self.distribution_costs.append(distribution_cost)

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

    def solve(self):
        total_cost = (
            lpSum(self.supply[(v.name, w.name)] * v.cost_per_kg + 
                  self.supply[(v.name, w.name)] * next((dc.cost for dc in self.distance_costs if dc.vendor == v and dc.warehouse == w), 0)
                  for v in vendors for w in warehouses) +
            lpSum(self.distribution[(w.name, r.name)] * next((dc.cost for dc in self.distribution_costs if dc.warehouse == w and dc.restaurant == r), 0)
                  for w in warehouses for r in restaurants)
        )
        self.problem += total_cost

        # Solve the optimization problem
        self.problem.solve()

        # Check the status of the solution
        if self.problem.status == 1:  # "Optimal" status code
            # Print the optimal solution
            for v in vendors:
                for w in warehouses:
                    if self.supply[(v.name, w.name)].varValue > 0:
                        print(f"Supply {self.supply[(v.name, w.name)].varValue} units from {v.name} at a cost of {self.supply[(v.name, w.name)].varValue * v.cost_per_kg} and delivered to warehouse {w.name}.")
                        print(f"Transport costs of {self.supply[(v.name, w.name)].varValue * next((dc.cost for dc in self.distance_costs if dc.vendor == v and dc.warehouse == w), 0)} from {v.name} to {w.name}.")

            for w in warehouses:
                for r in restaurants:
                    if self.distribution[(w.name, r.name)].varValue > 0:
                        print(f"Distribution {self.distribution[(w.name, r.name)].varValue} units from {w.name} to {r.name} at a cost of {self.distribution[(w.name, r.name)].varValue * next((dc.cost for dc in self.distribution_costs if dc.warehouse == w and dc.restaurant == r), 0)}.")

            print(f"Total cost: {self.problem.objective.value()}")
        else:
            print("No optimal solution found.")