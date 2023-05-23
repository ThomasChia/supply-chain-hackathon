from dataclasses import dataclass

@dataclass
class Vehicle:
    company: str
    name: str
    location: str
    number_available: int
    capacity: float
    cost_per_tonne_per_km: float
    co2_emissions_per_tonne_per_km: float