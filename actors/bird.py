from actors.threat import Threat
from positions.graph_loader import load_position_graph


class Bird(Threat):
    """
    Bird crossing from left to right high, from right to left lower
    """

    def init(self):
        super()
        self.is_killed = False

    def get_start_position(self):
        return "B00"

    def get_points_for_kill(self):
        return 6

    def generate_positions(self):
        return load_position_graph("Bird")
