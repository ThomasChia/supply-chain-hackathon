from abc import ABC, abstractmethod
import logging
from optimisers.optimiser import SupplyChainOptimisation
from output.output import Output, TotalOutput

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
        return super().create_table_output()

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