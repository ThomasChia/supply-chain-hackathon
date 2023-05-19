from config import *
from pulp import LpProblem, LpVariable, lpSum, LpMinimize


problem = LpProblem("SupplyChainOptimization", LpMinimize)

supply = LpVariable.dicts("supply", [(v, w) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
distance = LpVariable.dicts("Distance", distance_cost, lowBound=0, cat="Integer")


total_cost = (
    lpSum(supply[(v, w)] * vendors[v]['cost_per_kg'] + distance_cost[d]['cost'] for v in vendors for w in warehouses for d in distance_cost)
)
problem += total_cost

for v in vendors:
    for w in warehouses:
        problem += lpSum(supply[(v, w)]) <= vendors[v]['capacity']

for d in distance_cost:
    problem += lpSum(distance[d] for d in distance_cost) <= 1

problem += lpSum(supply[(v, w)] for v in vendors for w in warehouses) >= 500
problem += lpSum(distance[d] for d in distance_cost) >= 1
# problem += lpSum(supply[v] for v in vendors) >= 1

for w in warehouses:
    problem += lpSum(supply[(v, w)] for v in vendors) <= warehouses[w]["inventory_capacity"]  # Supply cannot exceed warehouse inventory

# for r in restaurants:
#     problem += lpSum(supply[(v, w)] for v in vendors for w in warehouses) == restaurant_demand[r]  # Restaurant demand must be met

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
        if supply[v].varValue > 0:
            print(f"Supply {supply[v].varValue} units from {v} at a cost of {supply[v].varValue * vendors[v]['cost_per_kg']}.")

    for d in distance_cost:
        if distance[d].varValue > 0:
            print(f"Distance {distance[d].varValue} units from {d} at a cost of {distance[d].varValue * distance_cost[d]['cost']}.")

    # for w in warehouses:
    #     if warehouse_inventory[w].varValue > 0:
    #         print(f"Warehouse {w} inventory: {warehouse_inventory[w].varValue} units")

    # for r in restaurants:
    #     if restaurant_demand[r].varValue > 0:
    #         print(f"Restaurant {r} demand: {restaurant_demand[r].varValue} units")

    print(f"Total cost: {problem.objective.value()}")
else:
    print("No optimal solution found.")