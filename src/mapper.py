from flows import Cost

class DistanceCostMapper:
    def __init__(self):
        self.mapping = {}

    def add_distance_cost(self, distance_cost: Cost):
        self.mapping[distance_cost.route_tuple] = distance_cost.cost

    def get_cost(self, distance_tuple: tuple[str, str]) -> float:
        return self.mapping.get(distance_tuple, 0.0)  # Return 0.0 if distance_tuple is not found