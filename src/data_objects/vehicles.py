from dataclasses import dataclass
from typing import List

@dataclass
class Vehicle:
    company: str
    name: str
    locations: List[str]
    number_available: int
    capacity: float
    cost_per_kg_per_km: float
    co2_emissions_per_kg_per_km: float