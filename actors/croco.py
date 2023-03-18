import pygame as pg

from positions.SpritePosition import *


class Croco():
    """
    Crocodile that starts from top and all the way down
    """

    def __init__(self, game):
        self.game = game
        self.isKilled = False
        self.allPositions = self.generatePositions()
        self.spritePosition: SpritePosition = None
        # self.sound=makeSound("sounds/Croco.wav")

    def update(self):
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("C00")
            return
        if self.isKilled:
            self.spritePosition.kill()
            return
        newPosition = self.allPositions.get(self.spritePosition.nextMove)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.threat_group.add(self.spritePosition)

    def doKill(self):
        self.isKilled = True
        # FIXME crocoile points are different at top and bottom
        self.game.score.addPoints(5)

    def generatePositions(self):
        d = {}
        c = "Croco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        d["C02"] = SpritePosition("C02", c)
        d["C03"] = SpritePosition("C03", c)
        d["C04"] = SpritePosition("C04", c)
        d["C05"] = SpritePosition("C05", c)
        d["C06"] = SpritePosition("C06", c)
        d["C07"] = SpritePosition("C07", c)
        d["C08"] = SpritePosition("C08", c)
        d["C09"] = SpritePosition("C09", c)
        d["C10"] = SpritePosition("C10", c)
        d["C11"] = SpritePosition("C11", c)
        d["C12"] = SpritePosition("C12", c)

        d["C00"].nextMove = "C01"
        d["C01"].nextMove = "C02"
        d["C02"].nextMove = "C03"
        d["C03"].nextMove = "C04"
        d["C04"].nextMove = "C05"
        d["C05"].nextMove = "C06"
        d["C06"].nextMove = "C07"
        d["C07"].nextMove = "C08"
        d["C08"].nextMove = "C09"
        d["C09"].nextMove = "C09"
        d["C10"].nextMove = "C11"
        d["C11"].nextMove = "C12"
        d["C12"].nextMove = "C00"

        return d
