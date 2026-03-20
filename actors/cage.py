from positions.graph_loader import load_position_graph


class Cage():
    """
    The cage that disapear and the Mom's smile
    """

    def __init__(self, game):
        self.game = game
        self.all_positions = load_position_graph("Cage")
        self.smile_position = self.all_positions.get("CSM")
        self.fully_opened = False
        self.init_cage()

    def init_cage(self):
        self.game.cage_group.remove(self.smile_position)
        self.remaining_cage = 4
        self.fully_opened = False
        self.sprite_positions = [
            self.all_positions.get("C03"),
            self.all_positions.get("C02"),
            self.all_positions.get("C01"),
            self.all_positions.get("C00")
        ]
        self.game.cage_group.add(self.sprite_positions)

    CAGE_SCORES = {3: 9, 2: 13, 1: 7, 0: 15}

    def open_cage(self):
        cage_to_remove = self.sprite_positions.pop()
        self.game.cage_group.remove(cage_to_remove)
        self.remaining_cage -= 1
        self.game.add_to_score(self.CAGE_SCORES[self.remaining_cage])
        if self.remaining_cage == 0:
            self.show_smile()
            self.fully_opened = True

    def show_smile(self):
        self.game.cage_group.add(self.smile_position)
        self.game.add_to_score(25)

    def update(self):
        pass

