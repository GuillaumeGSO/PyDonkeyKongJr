# from pygame_functions import *
import pygame as pg

from positions.SpritePosition import *


class Bird():
    """
    Bird crossing from left to right high, from right to left lower
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate_positions()
        self.init_bird()

    def init_bird(self):
        self.is_killed = False
        self.spritePosition = None

    def update(self):
        if self.is_killed:
            return

        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("B00")
            return
        newPosition = self.allPositions.get(self.spritePosition.next_move)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.threat_group.add(self.spritePosition)

    def do_kill(self):
        self.is_killed = True
        self.game.threat_group.remove(self.spritePosition)
        self.game.add_to_score(10)
        self.spritePosition == None

    def generate_positions(self):
        d = {}
        b = "Bird"
        d["B00"] = SpritePosition("B00", b)
        d["B01"] = SpritePosition("B01", b)
        d["B02"] = SpritePosition("B02", b)
        d["B03"] = SpritePosition("B03", b)
        d["B04"] = SpritePosition("B04", b)
        d["B05"] = SpritePosition("B05", b)
        d["B06"] = SpritePosition("B06", b)
        d["B07"] = SpritePosition("B07", b)

        d["B00"].next_move = "B01"
        d["B01"].next_move = "B02"
        d["B02"].next_move = "B03"
        d["B03"].next_move = "B04"
        d["B04"].next_move = "B05"
        d["B05"].next_move = "B06"
        d["B06"].next_move = "B07"
        d["B07"].next_move = "B00"

        return d
