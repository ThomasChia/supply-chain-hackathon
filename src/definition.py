from config import *
from pulp import LpProblem, LpVariable, lpSum, LpMinimize

# Create the optimization problem
problem = LpProblem("SupplyChainOptimization", LpMinimize)

# Define decision variables
supply = LpVariable.dicts("Supply", ((v, w) for v in vendors for w in warehouses), lowBound=0, cat="Integer")
warehouse_inventory = LpVariable.dicts("WarehouseInventory", warehouses, lowBound=0, cat="Integer")
restaurant_demand = LpVariable.dicts("RestaurantDemand", restaurants, lowBound=0, cat="Integer")

# Define the objective function
total_cost = (
    lpSum(supply[v][w] * vendors[v]["cost"] for v in vendors for w in warehouses) +
    lpSum(warehouse_inventory[w] * warehouses[w]["storage_cost"] for w in warehouses) +
    lpSum(restaurant_demand[r] * restaurants[r]["transport_cost"] for r in restaurants)
)
problem += total_cost

# Define the supply and demand constraints
for v in vendors:
    problem += lpSum(supply[v][w] for w in warehouses) == 1  # Each vendor must supply one warehouse

for w in warehouses:
    problem += lpSum(supply[v][w] for v in vendors) <= warehouse_inventory[w]  # Supply cannot exceed warehouse inventory

for r in restaurants:
    problem += lpSum(supply[v][w] for v in vendors for w in warehouses) == restaurant_demand[r]  # Restaurant demand must be met

# Define the capacity constraint for each warehouse (if applicable)
# Add additional constraints as needed for your specific scenario

# Define the flow conservation constraint for each vendor (if applicable)
# Add additional constraints as needed for your specific scenario


# Solve the optimization problem
problem.solve()

# Check the status of the solution
if problem.status == 1:  # "Optimal" status code
    # Print the optimal solution
    for v in vendors:
        for w in warehouses:
            if supply[v][w].varValue > 0:
                print(f"Supply {supply[v][w].varValue} units from {v} to {w}")

    for w in warehouses:
        if warehouse_inventory[w].varValue > 0:
            print(f"Warehouse {w} inventory: {warehouse_inventory[w].varValue} units")

    for r in restaurants:
        if restaurant_demand[r].varValue > 0:
            print(f"Restaurant {r} demand: {restaurant_demand[r].varValue} units")

    print(f"Total cost: {problem.objective.value()}")
else:
    print("No optimal solution found.")