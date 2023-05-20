from abc import ABC, abstractmethod
from dataclasses import dataclass

class Cost(ABC):
    def __init__(self):
        self.route_tuple = None
        self.cost = None

@dataclass
class SupplierWarehouseCost(Cost):
    route_tuple: tuple[str, str]
    cost: float

@dataclass
class WarehouseRestaurantCost(Cost):
    route_tuple: tuple[str, str]
    cost: float