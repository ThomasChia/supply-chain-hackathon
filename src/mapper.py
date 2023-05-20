from flows import Cost

class RouteCostMapper:
    def __init__(self):
        self.mapping = {}

    def add_distance_cost(self, route_cost: Cost):
        self.mapping[route_cost.route_tuple] = route_cost.cost

    def get_cost(self, distance_tuple: tuple[str, str]) -> float:
        return self.mapping.get(distance_tuple, 0.0)  # Return 0.0 if distance_tuple is not found