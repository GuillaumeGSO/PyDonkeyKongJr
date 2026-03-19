import pygame as pg

from positions.SpritePosition import *


class Nut():
    """
    The coconut falls when touched by monkey and respawn when monkey starts.
    Falls at player speed. Pauses on each kill to score, then continues falling.
    Can kill multiple enemies in one drop.
    """

    def __init__(self, game):
        self.game = game
        self.allPositions = self.generate_positions()
        self.init_nut()

    def init_nut(self):
        self.is_visible = True
        self.is_paused = False
        self.pause_start_time = None
        self.spritePosition = None
        self.last_time = pg.time.get_ticks()

    def can_update(self):
        now = pg.time.get_ticks()
        if now - self.last_time > self.game.animation_delay / 4:
            self.last_time = now
            return True
        return False

    def update(self):
        if self.spritePosition is None:
            self.spritePosition = self.allPositions.get("N00")
            return
        if not self.is_visible:
            self.spritePosition.kill()
            return

        # Paused after a kill — wait one rhythm period then continue falling
        if self.is_paused:
            if pg.time.get_ticks() - self.pause_start_time >= self.game.animation_delay:
                self.is_paused = False
            self.game.weapon_group.add(self.spritePosition)
            return

        # Check threats at current position before advancing (closest stop point)
        if self.spritePosition.position_name not in ("N00", "N03"):
            if self.handleThreats():
                self.game.weapon_group.add(self.spritePosition)
                return

        # Advance at player speed
        if self.mustFall():
            if self.can_update():
                newPosition = self.allPositions.get("N01")
                self.spritePosition.kill()
                self.spritePosition = newPosition
        elif self.spritePosition.position_name != "N00":
            if self.can_update():
                newPosition = self.allPositions.get(self.spritePosition.next_move)
                self.spritePosition.kill()
                if newPosition is not None:
                    self.spritePosition = newPosition

        # Check threats at N03 before disappearing (lower platform crocs)
        if self.spritePosition.position_name == "N03":
            if self.handleThreats():
                self.game.weapon_group.add(self.spritePosition)
                return

        self.handleBottom()

        self.game.weapon_group.add(self.spritePosition)

    def mustFall(self) -> bool:
        player = self.game.player
        return (player.sprite_position is not None
                and player.sprite_position.position_name == "H2J"
                and self.spritePosition == self.allPositions.get("N00"))

    def handleBottom(self):
        if self.spritePosition.position_name == "N03":
            self.is_visible = False

    # Maps nut position → (actor type, target position name to kill)
    KILL_MAP = {
        "N01": ("Croco", "C02"),
        "N02": ("Bird",  "B04"),
        "N03": ("Croco", "C09"),
    }

    def handleThreats(self) -> bool:
        entry = self.KILL_MAP.get(self.spritePosition.position_name)
        if entry is None:
            return False
        actor_type, target_pos = entry
        victims = self.game.crocos if actor_type == "Croco" else self.game.birds
        for victim in victims:
            if victim.spritePosition and victim.spritePosition.position_name == target_pos:
                self.spritePosition.rect.x = victim.spritePosition.rect.x
                self.spritePosition.rect.y = victim.spritePosition.rect.y
                victim.do_kill()
                self.is_paused = True
                self.pause_start_time = pg.time.get_ticks()
                return True
        return False

    def generate_positions(self):
        d = {}
        c = "Nut"
        d["N00"] = SpritePosition("N00", c)
        d["N01"] = SpritePosition("N01", c)
        d["N02"] = SpritePosition("N02", c)
        d["N03"] = SpritePosition("N03", c)
        # No next move in position 0 : not falling without being touched
        d["N01"].next_move = "N02"
        d["N02"].next_move = "N03"

        return d
