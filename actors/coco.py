import pygame as pg

from positions.SpritePosition import *


class Coco():
    """
    The coconut falls when touched by monkey and respawn when monkey starts
    """

    def __init__(self, game):
        self.game = game
        self.isVisible = True
        self.allPositions = self.generatePositions()
        self.spritePosition: SpritePosition = None

    def update(self):
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("C00")
            return
        if not self.isVisible:
            self.spritePosition.kill()
            return

        # print("threat", pg.sprite.spritecollideany(
        #     self.spritePosition, self.game.threat_group))

        if self.mustFall():
            newPosition = self.allPositions.get("C01")
        else:
            newPosition = self.allPositions.get(self.spritePosition.nextMove)

        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition

        self.handleBottom()
        self.game.weapon_group.add(self.spritePosition)

    def mustFall(self) -> bool:
        collider = pg.sprite.spritecollideany(
            self.spritePosition, self.game.player_group)

        return collider != None and collider.positionName == "H2J" and self.spritePosition == self.allPositions.get("C00")

    def handleBottom(self):
        if self.spritePosition.positionName == "C03":
            self.isVisible = False

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
