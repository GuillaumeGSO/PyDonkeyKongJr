import pygame as pg

from positions.SpritePosition import *


class Key():
    """
    The key is moving back and forth...
    """

    def __init__(self, game):
        self.game = game
        self.isKilled = False
        self.allPositions = self.generatePositions()
        self.spritePosition: SpritePosition = None

    def update(self):
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("K00")
            return
        if self.isKilled:
            self.spritePosition.kill()
            return
        newPosition = self.allPositions.get(self.spritePosition.nextMove)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.cage_group.add(self.spritePosition)

    def catchKey(self):
        self.isKilled = True
        self.game.cage.openCage()

    def generatePositions(self):
        d = {}
        k = "Key"
        d["K00"] = SpritePosition("K00", k)
        d["K01"] = SpritePosition("K01", k)
        d["K02"] = SpritePosition("K02", k)
        d["K03"] = SpritePosition("K03", k)
        d["K02b"] = SpritePosition("K02", k)
        d["K01b"] = SpritePosition("K01", k)

        d["K00"].nextMove = "K01"
        d["K01"].nextMove = "K02"
        d["K02"].nextMove = "K03"
        d["K03"].nextMove = "K02b"
        d["K02b"].nextMove = "K01b"
        d["K01b"].nextMove = "K00"
        return d
