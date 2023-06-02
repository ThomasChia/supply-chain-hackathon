import os

DEBUG = (os.getenv('DEBUG', 'False') == 'True')

vendors = {
    "vendor1": {"cost_per_kg": 10, "capacity": 100},
    "vendor2": {"cost_per_kg": 20, "capacity": 200},
    "vendor3": {"cost_per_kg": 50, "capacity": 300},
}

warehouses = {
    "warehouse1": {"storage_cost": 5, "inventory_capacity": 100},
    "warehouse2": {"storage_cost": 7, "inventory_capacity": 150},
    "warehouse3": {"storage_cost": 9, "inventory_capacity": 2000}
}

restaurants = {
    "restaurant1": {"restaurant_demand": 100, "transport_cost": 7, "inventory_capacity": 100},
    "restaurant2": {"restaurant_demand": 300, "transport_cost": 6, "inventory_capacity": 150},
    # Add more restaurants as needed
}

distance_cost = {
    ("vendor1", "warehouse1"): {"cost": 1},
    ("vendor1", "warehouse2"): {"cost": 6},
    ("vendor1", "warehouse3"): {"cost": 9},
    ("vendor2", "warehouse1"): {"cost": 12},
    ("vendor2", "warehouse2"): {"cost": 13},
    ("vendor2", "warehouse3"): {"cost": 10},
    ("vendor3", "warehouse1"): {"cost": 20},
    ("vendor3", "warehouse2"): {"cost": 10},
    ("vendor3", "warehouse3"): {"cost": 18},
}

distribution_cost = {
    ("warehouse1", "restaurant1"): {"cost": 1},
    ("warehouse1", "restaurant2"): {"cost": 6},
    ("warehouse1", "restaurant3"): {"cost": 9},
    ("warehouse2", "restaurant1"): {"cost": 12},
    ("warehouse2", "restaurant2"): {"cost": 13},
    ("warehouse2", "restaurant3"): {"cost": 10},
    ("warehouse3", "restaurant1"): {"cost": 20},
    ("warehouse3", "restaurant2"): {"cost": 10},
    ("warehouse3", "restaurant3"): {"cost": 18},
}

# Example distance data (you'll need to provide actual data)
supplier_to_warehouse_distances = [
    [10, 15, 20],  # Distance from Supplier 1 to Warehouse 1 and Warehouse 2 and 3
    [12, 13, 10],  # Distance from Supplier 2 to Warehouse 1 and Warehouse 2 and 3
    [8, 10, 9],   # Distance from Supplier 3 to Warehouse 1 and Warehouse 2 and 3
]

warehouse_to_restaurant_distances = [
    [5, 8],    # Distance from Warehouse 1 to Restaurant 1 and Restaurant 2
    [6, 7],    # Distance from Warehouse 2 to Restaurant 1 and Restaurant 2
]
