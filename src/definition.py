from config import *
from pulp import LpProblem, LpVariable, lpSum, LpMinimize


problem = LpProblem("SupplyChainOptimization", LpMinimize)

supply = LpVariable.dicts("supply", [(v, w) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
# distance = LpVariable.dicts("distance", distance_cost, lowBound=0, cat="Integer")


total_cost = (
    lpSum(supply[(v, w)] * vendors[v]['cost_per_kg'] + distance_cost[(v, w)]['cost'] for v in vendors for w in warehouses)
)
problem += total_cost

for v in vendors:
    problem += lpSum(supply[(v, w)] for w in warehouses) <= vendors[v]['capacity']

for w in warehouses:
    problem += lpSum(supply[(v, w)] for v in vendors) <= warehouses[w]["inventory_capacity"]  # Supply cannot exceed warehouse inventory

# for d in distance_cost:
#     problem += lpSum(distance[(v, w)] for v in vendors for w in warehouses) <= 1

problem += lpSum(supply[(v, w)] for v in vendors for w in warehouses) >= 500
# problem += lpSum(distance[(v, w)] for v in vendors for w in warehouses) >= 1
# problem += lpSum(supply[v] for v in vendors) >= 1

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
        for w in warehouses:
            if supply[(v, w)].varValue > 0:
                print(f"Supply {supply[(v, w)].varValue} units from {v} at a cost of {supply[(v, w)].varValue * vendors[v]['cost_per_kg']} and delivered to warehouse {w}.")
                print(f"Transport costs of {distance_cost[(v, w)]['cost']} from {v} to {w}.")

    # for d in distance_cost:
    #     if distance_cost[d].varValue > 0:
    #         print(f"Distance {distance_cost[d].varValue} units from {d} at a cost of {distance[d].varValue * distance_cost[d]['cost']}.")

    # for w in warehouses:
    #     if warehouse_inventory[w].varValue > 0:
    #         print(f"Warehouse {w} inventory: {warehouse_inventory[w].varValue} units")

    # for r in restaurants:
    #     if restaurant_demand[r].varValue > 0:
    #         print(f"Restaurant {r} demand: {restaurant_demand[r].varValue} units")

    print(f"Total cost: {problem.objective.value()}")
else:
    print("No optimal solution found.")