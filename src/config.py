# vendors = [
#     {"name": "Vendor 1", "cost": 10},
#     {"name": "Vendor 2", "cost": 12},
#     {"name": "Vendor 3", "cost": 8},
#     # Add more vendors as needed
# ]

# warehouses = [
#     {"name": "Warehouse 1", "transport_cost": 5, "storage_cost": 2},
#     {"name": "Warehouse 2", "transport_cost": 4, "storage_cost": 3},
#     # Add more warehouses as needed
# ]

vendors = {
    "vendor1": {"cost_per_kg": 10, "capacity": 100},
    "vendor2": {"cost_per_kg": 20, "capacity": 200},
    "vendor3": {"cost_per_kg": 50, "capacity": 300},
}

warehouses = {
    "warehouse1": {"storage_cost": 5, "inventory_capacity": 100},
    "warehouse2": {"storage_cost": 7, "inventory_capacity": 150},
    "warehouse3": {"storage_cost": 9, "inventory_capacity": 200}
}

restaurants = {
    "restaurant1": {"transport_cost": 7},
    "restaurant2": {"transport_cost": 6},
    # Add more restaurants as needed
}

distance_cost = {
    ("vendor1", "warehouse1"): {"cost": 1},
    ("vendor1", "warehouse2"): {"cost": 6},
    ("vendor1", "warehouse3"): {"cost": 9},
    ("vendor2", "warehouse1"): {"cost": 12},
    ("vendor2", "warehouse2"): {"cost": 13},
    ("vendor2", "warehouse3"): {"cost": 10},
    ("vendor3", "warehouse1"): {"cost": 8},
    ("vendor3", "warehouse2"): {"cost": 10},
    ("vendor3", "warehouse3"): {"cost": 9},
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
