import logging
from output.output import Edge
from typing import Dict, List

logger = logging.getLogger(__name__)

class Evaluator:
    def __init__(self, supply_chain: List[Edge], active_sites: list[tuple]):
        self.supply_chain = supply_chain
        self.active_sites = active_sites
        self.new_supply_chain: List[Edge] = []
        self.connector_edges: Dict[str: [Edge]] = {}

    def calculate_new_supply_chain(self):
        """
        This method takes the previous supply chain and updates it based on which sites are active.
        It returns a new supply chain object.
        """
        self.remove_non_active_sites()
        self.adjust_inflows_and_outflows()

    def remove_non_active_sites(self):
        for edge in self.supply_chain:
            if self.edge_is_active(edge):
                self.new_supply_chain.append(edge)
        logger.info(f"Removed {len(self.supply_chain) - len(self.new_supply_chain)} edges from supply chain.")
    
    def adjust_inflows_and_outflows(self):
        self.get_connector_edges()
        self.equate_amounts()
        self.replace_connector_edges()

    def edge_is_active(self, edge: Edge):
        return ((edge.source_name, edge.source_id) in self.active_sites) and ((edge.target_name, edge.target_id) in self.active_sites)
    
    def at_supply_stage(self, edge: Edge):
        return edge.stage == 'supply'
    
    def at_distribution_stage(self, edge: Edge):
        return edge.stage == 'distribution'
    
    def get_connector_edges(self):
        connector_edges = {}
        for edge in self.new_supply_chain:
            connector_edges = self.add_connector_edge(edge, connector_edges)
        self.connector_edges = connector_edges

    def add_connector_edge(self, edge: Edge, connector_edges):
        if edge.stage == 'supply':
            if edge.target_id not in connector_edges:
                connector_edges[edge.target_id] = edge
            else:
                connector_edges[edge.target_id] = connector_edges[edge.target_id].append(edge)
        elif edge.stage == 'distribution':
            if edge.source_id not in connector_edges:
                connector_edges[edge.source_id] = edge
            else:
                connector_edges[edge.source_id] = connector_edges[edge.target_id].append(edge)
        return connector_edges
    
    def equate_amounts(self):
        for node in self.connector_edges.values():
            inflow = 0
            outflow = 0
            for edge in node:
                if edge.stage == 'supply':
                    inflow += edge.amount
                elif edge.stage == 'distribution':
                    outflow += edge.amount
            
            if inflow >= outflow:
                flow_difference = inflow - outflow
                distributed_supply_shortage = flow_difference / len(node)
                for edge in node:
                    if edge.stage == 'distribution':
                        edge.amount -= distributed_supply_shortage
            elif inflow == outflow:
                continue
            else:
                raise Exception("Outflow greater than inflow.")
            
    def replace_connector_edges(self):
        for edge in self.new_supply_chain:
            edge = self.replace_connector_edge(edge)

    def replace_connector_edge(self, edge: Edge) -> Edge:
        if edge.stage == 'distribution':
            if edge.source_id in self.connector_edges.keys():
                equivalent_edges = self.connector_edges[edge.source_id]
                new_edge = self.get_matching_edge(equivalent_edges, edge)
                edge.amount = new_edge.amount
                return edge
        return edge

    def get_matching_edge(self, edges_list: List[Edge], edge_to_match: Edge):
        for edge in edges_list:
            if (edge.source_id, edge.source_name, edge.target_id, edge.target_name) == (edge_to_match.source_id, edge_to_match.source_name, edge_to_match.target_id, edge_to_match.target_name):
                return edge