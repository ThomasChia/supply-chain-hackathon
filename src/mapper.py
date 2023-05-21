from flows import Cost
from typing import List
from vehicles import Vehicle

class RouteCostMapper:
    def __init__(self, route_costs: List[Cost]):
        self.mapping = self.get_mapping(route_costs)

    def get_mapping(self, route_costs: List[Cost]) -> dict[tuple[str, str], float]:
        return {cost.route_tuple: cost.cost for cost in route_costs}

    def get_cost(self, distance_tuple: tuple[str, str]) -> float:
        return self.mapping.get(distance_tuple, 0.0)  # Return 0.0 if distance_tuple is not found
    

class VehicleCostMapper:
    def __init__(self, vehicle_costs: List[Vehicle]):
        self.mapping = self.get_mapping(vehicle_costs)

    def get_mapping(self, vehicle_costs: List[Vehicle]) -> dict[str, float]:
        return {cost.name: cost.cost_per_tonne_per_km for cost in vehicle_costs}