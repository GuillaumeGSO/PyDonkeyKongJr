import pygame as pg

from positions.SpritePosition import *


class Coco():
    """
    The coconut falls when touched by monkey and respawn when monkey starts
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generatePositions()
        self.spritePosition: SpritePosition = None

    def update(self):
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("C00")
            return
        newPosition = self.allPositions.get(self.spritePosition.nextMove)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.weapon_group.add(self.spritePosition)

    def generatePositions(self):
        d = {}
        c = "Coco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        d["C02"] = SpritePosition("C02", c)
        d["C03"] = SpritePosition("C03", c)
        # No next move in position 0 : not falling without being touched
        d["C01"].nextMove = "C02"
        d["C02"].nextMove = "C03"
        return d
