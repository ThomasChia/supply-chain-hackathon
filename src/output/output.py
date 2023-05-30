from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Output:
    stage: str
    source: str
    source_type: str
    target: str
    target_type: str
    vehicle_company: str
    vehicle_type: str
    amount: float
    cost: float
    co2_emissions: float

@dataclass
class TotalOutput:
    total_amount: float
    total_cost: float
    total_co2_emissions: float