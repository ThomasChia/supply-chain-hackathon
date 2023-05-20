from dataclasses import dataclass

@dataclass
class Vehicle:
    company: str
    name: str
    number_available: int
    capacity: float
    cost_per_tonne_per_km: float