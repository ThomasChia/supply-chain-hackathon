from config import *
from pulp import LpProblem, LpVariable, lpSum, LpMinimize


problem = LpProblem("SupplyChainOptimization", LpMinimize)

supply = LpVariable.dicts("supply", [(v, w) for v in vendors for w in warehouses], lowBound=0, cat='Continuous')
distribution = LpVariable.dicts("distance", [(w, r) for w in warehouses for r in restaurants], lowBound=0, cat="Integer")


total_cost = (
    # lpSum(supply[(v, w)] * vendors[v]['cost_per_kg'] + distance_cost[(v, w)]['cost'] * (1 if supply[(v, w)] > 0 else 0) for v in vendors for w in warehouses)
    # lpSum(supply[(v, w)] * vendors[v]['cost_per_kg'] + distance_cost[(v, w)]['cost'] * (1 if supply[(v, w)] > 0 else 0) for v in vendors for w in warehouses)
    lpSum(supply[(v, w)] * vendors[v]['cost_per_kg'] + 
          supply[(v, w)] * distance_cost[(v, w)]['cost'] for v in vendors for w in warehouses) +
    lpSum(distribution[(w, r)] * distribution_cost[(w, r)]['cost'] for w in warehouses for r in restaurants)
)
problem += total_cost

for v in vendors:
    problem += lpSum(supply[(v, w)] for w in warehouses) <= vendors[v]['capacity']

for w in warehouses:
    problem += lpSum(supply[(v, w)] for v in vendors) <= warehouses[w]["inventory_capacity"]  # Supply cannot exceed warehouse inventory
    problem += lpSum(distribution[(w, r)] for r in restaurants) <= lpSum(supply[(v, w)] for v in vendors)  # Supply cannot exceed warehouse original supply

for r in restaurants:
    problem += lpSum(distribution[(w, r)] for w in warehouses) >= restaurants[r]['restaurant_demand']  # Restaurant demand must be met

# for d in distance_cost:
#     problem += lpSum(distance[(v, w)] for v in vendors for w in warehouses) <= 1

problem += lpSum(supply[(v, w)] for v in vendors for w in warehouses) >= lpSum(restaurants[r]['restaurant_demand'] for r in restaurants)
# problem += lpSum(distance[(v, w)] for v in vendors for w in warehouses) >= 1
# problem += lpSum(supply[v] for v in vendors) >= 1

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
                print(f"Transport costs of {supply[(v, w)].varValue * distance_cost[(v, w)]['cost']} from {v} to {w}.")

    for w in warehouses:
        for r in restaurants:
            if distribution[(w, r)].varValue > 0:
                print(f"Distribution {distribution[(w, r)].varValue} units from {w} to {r} at a cost of {distribution[(w, r)].varValue * distribution_cost[(w, r)]['cost']}.")


    print(f"Total cost: {problem.objective.value()}")
else:
    print("No optimal solution found.")