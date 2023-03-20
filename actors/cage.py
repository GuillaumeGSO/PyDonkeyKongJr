import pygame as pg

from positions.SpritePosition import *
from settings import SCORE_DELAY


class Cage():
    """
    The cage that disapear and the Mom's smile
    """

    def __init__(self, game):
        self.game = game
        self.all_positions = self.generate_positions()
        self.smile_postion = self.all_positions.get("CSM")
        self.fully_opened = False
        self.init_cage()

    def init_cage(self):
        self.game.cage_group.remove(self.smile_postion)
        self.remaining_cage = 4
        self.fully_opened = False
        self.sprite_positions = [
            self.all_positions.get("C03"),
            self.all_positions.get("C02"),
            self.all_positions.get("C01"),
            self.all_positions.get("C00")
        ]
        self.game.cage_group.add(self.sprite_positions)

    def open_cage(self):
        cage_to_remove = self.sprite_positions.pop()
        self.game.cage_group.remove(cage_to_remove)
        self.remaining_cage -= 1
        self.game.add_to_score(25)
        if self.remaining_cage == 0:
            self.show_smile()
            self.fully_opened = True

    def show_smile(self):
        self.game.cage_group.add(self.smile_postion)
        pg.time.delay(SCORE_DELAY*2)
        self.game.add_to_score(50)

    def update(self):
        pass

    def generate_positions(self):
        d = {}
        b = "Cage"
        d["C00"] = SpritePosition("C00", b)
        d["C01"] = SpritePosition("C01", b)
        d["C02"] = SpritePosition("C02", b)
        d["C03"] = SpritePosition("C03", b)
        # smiling Mom
        d["CSM"] = SpritePosition("CSM", b)
        return d
