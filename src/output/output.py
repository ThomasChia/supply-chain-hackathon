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
    source_co2_emissions: float
    target_id: str
    target_name: str
    target_type: str
    target_cost: float
    target_co2_emissions: float
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

    def update_metrics_for_edge(self, edge: Edge):
        if edge.stage == 'supply':
            self.total_cost += edge.source_cost + edge.target_cost + edge.transport_cost
            self.total_co2_emissions += edge.source_co2_emissions + edge.target_co2_emissions + edge.transport_co2_emissions
        elif edge.stage == 'distribution':
            self.total_amount += edge.amount
            self.total_cost += edge.target_cost + edge.transport_cost
            self.total_co2_emissions += edge.target_co2_emissions + edge.transport_co2_emissions


class SupplyChain:
    def __init__(self, supply_chain:List[Edge]):
        self.supply_chain = supply_chain
        self.metrics: TotalOutput = TotalOutput(0, 0, 0)

    def get_totals(self):
        """
        This method returns the total amounts, costs, and co2 emissions for a given list of flow outputs.
        """
        for edge in self.supply_chain:
            self.metrics.update_metrics_for_edge(edge)

    @classmethod
    def append_edge(self, edge:Edge, supply_chain:List[Edge]):
        supply_chain = supply_chain.append(edge)

    def plan_to_list(self):
        supply_chain_dict = self.__dict__.copy()
        supply_chain_dict['supply_chain'] = [edge.__dict__ for edge in supply_chain_dict['supply_chain']]
        supply_chain_dict['metrics'] = supply_chain_dict['metrics'].__dict__
        return supply_chain_dict
    
    @classmethod
    def list_to_plan(self, supply_chain_list):
        supply_chain = []
        for edge in supply_chain_list:
            SupplyChain.append_edge(edge=Edge(**edge), supply_chain=supply_chain)
        supply_chain = SupplyChain(supply_chain)
        supply_chain.get_totals()
        return supply_chain

    def get_edge_by_source_and_target(self, source_id, source_name, target_id, target_name):
        for edge in self.supply_chain:
            if (edge.source_id, edge.source_name, edge.target_id, edge.target_name) == (source_id, source_name, target_id, target_name):
                return edge



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