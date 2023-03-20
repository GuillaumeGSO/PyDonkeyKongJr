import pygame as pg

from positions.SpritePosition import *


class Coco():
    """
    The coconut falls when touched by monkey and respawn when monkey starts.
    It kills all enemies when falling
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate_positions()
        self.init_coco()

    def init_coco(self):
        self.is_visible = True
        self.spritePosition = None

    def update(self):
        if self.spritePosition == None:
            self.spritePosition = self.allPositions.get("C00")
            return
        if not self.is_visible:
            self.spritePosition.kill()
            return

        if self.mustFall():
            newPosition = self.allPositions.get("C01")
        else:
            newPosition = self.allPositions.get(self.spritePosition.next_move)

        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition

        self.handleBottom()

        self.handleThreats()

        self.game.weapon_group.add(self.spritePosition)

    def mustFall(self) -> bool:
        collider = pg.sprite.spritecollideany(
            self.spritePosition, self.game.player_group)
        return collider != None and collider.position_name == "H2J" and self.spritePosition == self.allPositions.get("C00")

    def handleBottom(self):
        if self.spritePosition.position_name == "C03":
            self.is_visible = False

    def handleThreats(self):
        collider = pg.sprite.spritecollideany(
            self.spritePosition, self.game.threat_group)
        if collider != None:
            if collider.actor_type == "Bird":
                self.game.bird.do_kill()
            if collider.actor_type == "Croco":
                self.game.croco.do_kill()

    def generate_positions(self):
        d = {}
        c = "Coco"
        d["C00"] = SpritePosition("C00", c)
        d["C01"] = SpritePosition("C01", c)
        d["C02"] = SpritePosition("C02", c)
        d["C03"] = SpritePosition("C03", c)
        # No next move in position 0 : not falling without being touched
        d["C01"].next_move = "C02"
        d["C02"].next_move = "C03"

        return d
