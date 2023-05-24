from data_objects.flows import Distance
from typing import List
from data_objects.vehicles import Vehicle

class RouteCostMapper:
    def __init__(self, route_distances: List[Distance]):
        self.distance_mapping = self.get_mapping(route_distances)

    def get_mapping(self, route_distances: List[Distance]) -> dict[tuple[str, str], float]:
        return {distance.route_tuple: distance.distance for distance in route_distances}

    def get_cost(self, distance_tuple: tuple[str, str]) -> float:
        return self.distance_mapping.get(distance_tuple, 0.0)  # Return 0.0 if distance_tuple is not found
    

class VehicleCostMapper:
    def __init__(self, vehicle_costs: List[Vehicle]):
        self.cost_mapping = self.get_cost_mapping(vehicle_costs)
        self.co2_mapping = self.get_co2_emissions_mapping(vehicle_costs)

    def get_cost_mapping(self, vehicle_costs: List[Vehicle]) -> dict[tuple[str, str], float]:
        return {(cost.company, cost.name): cost.cost_per_kg_per_km for cost in vehicle_costs}
    
    def get_co2_emissions_mapping(self, vehicle_costs: List[Vehicle]) -> dict[tuple[str, str], float]:
        return {(cost.company, cost.name): cost.co2_emissions_per_kg_per_km for cost in vehicle_costs}