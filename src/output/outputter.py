from abc import ABC, abstractmethod
from collections import defaultdict
import logging
from optimisers.optimiser import SupplyChainOptimisation
from output.output import (VendorOutput,
                           WarehouseOutput,
                           RestaurantOutput,
                           Edge,
                           SupplyChain,
                           TotalOutput)
from typing import List

logger = logging.getLogger(__name__)

class Outputter(ABC):

    @abstractmethod
    def create_table_output(self):
        pass

    @abstractmethod
    def print_output(self):
        pass

class OptimisationOutputter(Outputter):
    def __init__(self, optimiser: SupplyChainOptimisation):
        self.optimiser = self.confirm_optimal_solution(optimiser)

    def confirm_optimal_solution(self, optimiser: SupplyChainOptimisation):
        if optimiser.problem.status == 1:
            return optimiser
        else:
            logger.warning("No optimal solution found.")
            return
        
    def create_table_output(self):
        supply_output = []
        for supply in self.optimiser.supply:
            if self.optimiser.supply[supply].varValue > 0:
                flow_output = self.create_flow_output(supply, self.optimiser.supply, supply=True)
                supply_output.append(flow_output)
            
        distribution_output = []
        for distribution in self.optimiser.distribution:
            if self.optimiser.distribution[distribution].varValue > 0:
                flow_output = self.create_flow_output(distribution, self.optimiser.distribution, supply=False)
                distribution_output.append(flow_output)

        supply_output.extend(distribution_output)
        return SupplyChain(supply_output)

    def print_output(self):
        if self.optimiser:
            self.print_supply_output()
            self.print_distribution_output()
            self.print_supply_co2_output()
            self.print_distribution_co2_output()
            self.print_total_cost()
        
    def print_supply_output(self):
        for v in self.optimiser.vendors:
            for w in self.optimiser.warehouses:
                for ve in self.optimiser.vehicles:
                    if self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue > 0:
                        logger.info(f"Supply {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue} units from {v.name} at a cost of {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue * v.cost_per_kg} and delivered to warehouse {w.name}.")
                        logger.info(f"Inventory at warehouse {w.name} is {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue} units at a cost of {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue * w.storage_cost_per_kg}.")
                        logger.info(f"Transport costs of {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue * self.optimiser.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.optimiser.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

    def print_distribution_output(self):
        for w in self.optimiser.warehouses:
            for r in self.optimiser.restaurants:
                for ve in self.optimiser.vehicles:
                    if self.optimiser.distribution[(w.name, r.name, ve.company, ve.name)].varValue > 0:
                        logger.info(f"Transport costs of {self.optimiser.distribution[(w.name, r.name, ve.company, ve.name)].varValue * self.optimiser.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.optimiser.vehicle_mapper.cost_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")


    def print_supply_co2_output(self):
        for v in self.optimiser.vendors:
            for w in self.optimiser.warehouses:
                for ve in self.optimiser.vehicles:
                    if self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue > 0:
                        logger.info(f"CO2 emissions of {self.optimiser.supply[(v.name, w.name, ve.company, ve.name)].varValue * self.optimiser.supplier_warehouse_mapper.distance_mapping[v.name, w.name] * self.optimiser.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {v.name} to {w.name} using {ve.name} from {ve.company}.")

    def print_distribution_co2_output(self):
        for w in self.optimiser.warehouses:
            for r in self.optimiser.restaurants:
                for ve in self.optimiser.vehicles:
                    if self.optimiser.distribution[(w.name, r.name, ve.company, ve.name)].varValue > 0:
                        logger.info(f"CO2 emissions of {self.optimiser.distribution[(w.name, r.name, ve.company, ve.name)].varValue * self.optimiser.warehouse_restaurant_mapper.distance_mapping[w.name, r.name] * self.optimiser.vehicle_mapper.co2_mapping[(ve.company, ve.name)]} from {w.name} to {r.name} using {ve.name} from {ve.company}.")            

    def print_total_cost(self):
        logger.info(f"Total cost: {self.optimiser.problem.objective.value()}")

    def create_flow_output(self, flow, chain, supply=True):
        source_id = flow[0]
        source_name = flow[0]
        target_id = flow[1]
        target_name = flow[1]
        vehicle_company = flow[2]
        vehicle_type = flow [3]
        amount = chain[flow].varValue

        if supply:
            stage = 'supply'
            source_type = 'farm'
            source_cost = chain[flow].varValue * self.optimiser.supplier_cost_mapper.supplier_mapping[source_id]
            source_co2_emissions = chain[flow].varValue * self.optimiser.supplier_cost_mapper.supplier_co2_mapping[source_id]
            target_type = 'warehouse'
            target_cost = chain[flow].varValue * self.optimiser.warehouse_cost_mapper.warehouse_mapping[target_id]
            target_co2_emissions = 0
            transport_cost = chain[flow].varValue * self.optimiser.supplier_warehouse_mapper.distance_mapping[(source_id, target_id)] * self.optimiser.vehicle_mapper.cost_mapping[(vehicle_company, vehicle_type)]
            transport_co2_emissions = chain[flow].varValue * self.optimiser.supplier_warehouse_mapper.distance_mapping[(source_id, target_id)] * self.optimiser.vehicle_mapper.co2_mapping[(vehicle_company, vehicle_type)]
        else:
            stage = 'distribution'
            source_type = 'warehouse'
            source_cost = chain[flow].varValue * self.optimiser.warehouse_cost_mapper.warehouse_mapping[source_id]
            source_co2_emissions = 0
            target_type = 'restaurant'
            target_cost = 0
            target_co2_emissions = 0
            transport_cost = chain[flow].varValue * self.optimiser.warehouse_restaurant_mapper.distance_mapping[(source_id, target_id)] * self.optimiser.vehicle_mapper.cost_mapping[(vehicle_company, vehicle_type)]
            transport_co2_emissions = chain[flow].varValue * self.optimiser.warehouse_restaurant_mapper.distance_mapping[(source_id, target_id)] * self.optimiser.vehicle_mapper.co2_mapping[(vehicle_company, vehicle_type)]

        return Edge(stage=stage,
                    source_id=source_id,
                    source_name=source_name,
                    source_type=source_type,
                    source_cost=source_cost,
                    source_co2_emissions=source_co2_emissions,
                    target_id=target_id,
                    target_name=target_name,
                    target_type=target_type,
                    target_cost=target_cost,
                    target_co2_emissions=target_co2_emissions,
                    vehicle_company=vehicle_company,
                    vehicle_type=vehicle_type,
                    amount=amount,
                    transport_cost=transport_cost,
                    transport_co2_emissions=transport_co2_emissions)
    
    def create_site_from_flow(self, flow_list: List[Edge]):
        amounts = defaultdict(float)
        cost = defaultdict(float)
        emissions = defaultdict(float)
        for flow in flow_list:
            amounts[flow.source] += flow.amount
