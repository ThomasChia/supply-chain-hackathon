from abc import ABC, abstractmethod
from dataclasses import dataclass

class Distance(ABC):
    def __init__(self):
        self.route_tuple = ('', '')
        self.distance = 0

@dataclass
class SupplierWarehouseDistance(Distance):
    route_tuple: tuple[str, str]
    distance: float

@dataclass
class WarehouseRestaurantDistance(Distance):
    route_tuple: tuple[str, str]
    distance: float