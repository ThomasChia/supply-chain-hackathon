from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class VendorOutput:
    site: str
    site_type: str
    amount: float
    cost: float
    co2_emissions: float

@dataclass
class WarehouseOutput:
    site: str
    site_type: str
    amount: float
    storage_cost: float
    co2_emissions: float

@dataclass
class RestaurantOutput:
    site: str
    site_type: str
    amount: float
    co2_emissions: float

@dataclass
class FlowOutput:
    stage: str
    source: str
    source_type: str
    source_cost: float
    target: str
    target_type: str
    target_cost: float
    vehicle_company: str
    vehicle_type: str
    amount: float
    transport_cost: float
    transport_co2_emissions: float

@dataclass
class TotalOutput:
    total_amount: float
    total_cost: float
    total_co2_emissions: float