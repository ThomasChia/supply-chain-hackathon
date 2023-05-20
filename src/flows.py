from dataclasses import dataclass

@dataclass
class DistanceCost:
    vendor: str
    warehouse: str
    cost: float

@dataclass
class DistributionCost:
    warehouse: str
    restaurant: str
    cost: float