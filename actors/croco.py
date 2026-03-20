from actors.threat import Threat
from positions.graph_loader import load_position_graph


class Croco(Threat):
    """
    Crocodile that starts from top and all the way down
    """

    def __init__(self, game):
        super().__init__(game)
        # self.sound=makeSound("sounds/Croco.wav")

    def init(self):
        super()
        self.is_killed = False

    def get_start_position(self):
        return "C00"

    UP_POSITIONS = {"C00", "C01", "C02", "C03", "C04"}

    def get_points_for_kill(self):
        if self.sprite_position.position_name in self.UP_POSITIONS:
            return 3
        return 9

    def generate_positions(self):
        return load_position_graph("Croco")
