import pygame as pg

from positions.SpritePosition import *
from settings import ANIMATION_DELAY


class Croco():
    """
    Crocodile that starts from top and all the way down
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate_positions()
        self.init_croco()
        self.last_time = pg.time.get_ticks()
        # self.sound=makeSound("sounds/Croco.wav")

    def init_croco(self):
        self.is_killed = False
        self.spritePosition = None

    def can_update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_time) > ANIMATION_DELAY:
            self.last_time = current_time
            return True
        return False

    def update(self):

        if not self.can_update():
            return

        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("C00")
            return
        if self.is_killed:
            self.spritePosition.kill()
            return
        newPosition = self.allPositions.get(self.spritePosition.next_move)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.threat_group.add(self.spritePosition)

    def do_kill(self):
        self.is_killed = True
        # FIXME crocodile points are different at top and bottom
        self.game.add_to_score(5)

    def generate_positions(self):
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

        d["C00"].next_move = "C01"
        d["C01"].next_move = "C02"
        d["C02"].next_move = "C03"
        d["C03"].next_move = "C04"
        d["C04"].next_move = "C05"
        d["C05"].next_move = "C06"
        d["C06"].next_move = "C07"
        d["C07"].next_move = "C08"
        d["C08"].next_move = "C09"
        d["C09"].next_move = "C10"
        d["C10"].next_move = "C11"
        d["C11"].next_move = "C12"
        d["C12"].next_move = "C00"

        return d
