vendors = [
    {"name": "Vendor 1", "cost": 10},
    {"name": "Vendor 2", "cost": 12},
    {"name": "Vendor 3", "cost": 8},
    # Add more vendors as needed
]

warehouses = [
    {"name": "Warehouse 1", "transport_cost": 5, "storage_cost": 2},
    {"name": "Warehouse 2", "transport_cost": 4, "storage_cost": 3},
    # Add more warehouses as needed
]

restaurants = [
    {"name": "Restaurant 1", "transport_cost": 7},
    {"name": "Restaurant 2", "transport_cost": 6},
    # Add more restaurants as needed
]

# Example distance data (you'll need to provide actual data)
supplier_to_warehouse_distances = [
    [10, 15],  # Distance from Supplier 1 to Warehouse 1 and Warehouse 2
    [12, 13],  # Distance from Supplier 2 to Warehouse 1 and Warehouse 2
    [8, 10],   # Distance from Supplier 3 to Warehouse 1 and Warehouse 2
]

warehouse_to_restaurant_distances = [
    [5, 8],    # Distance from Warehouse 1 to Restaurant 1 and Restaurant 2
    [6, 7],    # Distance from Warehouse 2 to Restaurant 1 and Restaurant 2
]
