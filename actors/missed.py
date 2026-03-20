from positions.graph_loader import load_position_graph


class Missed():
    """
    Errors during the game : 3 lives only
    """

    def __init__(self, game):
        self.game = game
        self.all_positions = load_position_graph("Missed")
        self.sprite_position = None

    def miss(self, number):
        self.sprite_position = self.all_positions.get("M0" + str(number))
        self.game.info_group.add(self.sprite_position)

    def update(self):
        pass
