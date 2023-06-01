from output.output import Edge
from typing import List

class Evaluator:
    def __init__(self, supply_chain: List[Edge], active_sites: list[str]):
        self.supply_chain = supply_chain
        self.active_sites = active_sites

    def calculate_new_supply_chain(self):
        """
        This method takes the previous supply chain and updates it based on which sites are active.
        It returns a new supply chain object.
        """
        pass