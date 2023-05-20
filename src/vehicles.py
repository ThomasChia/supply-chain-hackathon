from dataclasses import dataclass

@dataclass
class Vehicle:
    name: str
    number_available: str
    capacity: float
    cost_per_tonne_per_km: float