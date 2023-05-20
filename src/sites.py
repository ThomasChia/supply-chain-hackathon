from dataclasses import dataclass

@dataclass
class Vendor:
    name: str
    capacity: int
    cost_per_kg: float
    location: str

@dataclass
class Warehouse:
    name: str
    inventory_capacity: int
    storage_cost_per_kg: float
    location: str

@dataclass
class Restaurant:
    name: str
    restaurant_demand: float
    location: str