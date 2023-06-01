from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

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
class Edge:
    stage: str
    source_id: str
    source_name: str
    source_type: str
    source_cost: float
    target_id: str
    target_name: str
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

class SupplyChain:
    def __init__(self, supply_chain:List[Edge]):
        self.supply_chain_plan = supply_chain

    def get_totals(self):
        """
        This method will return the total amounts, costs, and co2 emissions for a given list of flow outputs.
        """
        pass

    def plan_to_list():
        pass



test_resp = {
    'plan': [{'stage': 'str',
                'source_id': 'str',
                'source_name': 'str',
                'source_type': 'str',
                'source_cost': 1,
                'source_emissions': 1,
                'target_id': 'str',
                'target_name': 'str',
                'target_type': 'str',
                'target_cost': 1,
                'target_emissions': 1,
                'vehicle_company': 'str',
                'vehicle_type': 'str',
                'amount': 1,
                'transport_cost': 1,
                'transport_co2_emissions': 1}, ],
    'metrics': {'total_profit': 1,
                'total_cost': 1,
                'total_co2_emissions': 1}
}