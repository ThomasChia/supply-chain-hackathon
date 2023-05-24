from dataclasses import dataclass

@dataclass
class Vendor:
    name: str
    company: str
    location: str
    capacity: int
    additional_capacity: int
    sla_period: int
    onboarding_period: int
    cost_per_kg: float
    co2_emissions_per_kg: float

@dataclass
class VehicleDepots:
    company: str
    location: str
    transportation_range: float
    lead_time: int

@dataclass
class Warehouse:
    name: str
    location: str
    onboarding_period: int
    inventory_capacity: int
    storage_cost_per_kg: float

@dataclass
class Restaurant:
    name: str
    location: str
    restaurant_demand: float
    current_stock: float
    daily_total_demand: float
    daily_profit: float
    fixed_cost: float