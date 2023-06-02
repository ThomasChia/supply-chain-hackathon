from typing import List
from data_objects.flows import Distance
from data_objects.sites import Vendor, Warehouse
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
    
class SupplierCostMapper:
    def __init__(self, suppliers: List[Vendor]):
        self.supplier_mapping = self.get_cost_mapping(suppliers)
        self.supplier_co2_mapping = self.get_co2_mapping(suppliers)

    def get_cost_mapping(self, suppliers: List[Vendor])  -> dict[str, float]:
        return {supplier.name: supplier.cost_per_kg for supplier in suppliers}
    
    def get_co2_mapping(self, suppliers: List[Vendor]) -> dict[str, float]:
        return {supplier.name: float(supplier.co2_emissions_per_kg) for supplier in suppliers}
    
class WarehouseCostMapper:
    def __init__(self, warehouses: List[Warehouse]):
        self.warehouse_mapping = self.get_cost_mapping(warehouses)

    def get_cost_mapping(self, warehouses: List[Warehouse])  -> dict[str, float]:
        return {warehouse.name: warehouse.storage_cost_per_kg for warehouse in warehouses}
    
# class SupplierEmissionsMapper:
#     def __init__(self, suppliers: List[Vendor]):
#         self.supplier_mapping