import pygame as pg

from positions.SpritePosition import *


class Missed():
    """
    Errors during the game : 3 lives only
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate_positions()
        self.spritePosition = None
        # self.sound = makeSound("sounds/Missed.wav")

    def miss(self, number):
        self.spritePosition = self.allPositions.get("M0" + str(number))
        self.game.info_group.add(self.spritePosition)

    def update(self):
        pass

    def generate_positions(self):
        d = {}
        b = "Missed"
        d["M00"] = SpritePosition("M00", b)
        d["M01"] = SpritePosition("M01", b)
        d["M02"] = SpritePosition("M02", b)
        return d
