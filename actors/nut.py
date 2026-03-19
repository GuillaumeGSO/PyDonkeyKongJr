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
        self.spritePosition = None
        self.last_time = pg.time.get_ticks()
        self._instant_mode = False
        self._killed_at_bottom = False
        self._bottom_arrival_time = None

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
            return

        # Score pause: keep nut visible; game handles the unpause
        if self.game.is_score_paused:
            self.game.weapon_group.add(self.spritePosition)
            return

        # After any kill: instantly traverse remaining positions
        if self._instant_mode:
            self._advance_instant()
            return

        # Normal animated fall
        if self.mustFall():
            if self.can_update():
                self.spritePosition.kill()
                self.spritePosition = self.allPositions.get("N01")
        elif self.spritePosition.position_name != "N00":
            if self.can_update():
                next_name = self.spritePosition.next_move
                if next_name is not None:       # guard: N03 has no next_move
                    new_pos = self.allPositions.get(next_name)
                    self.spritePosition.kill()
                    if new_pos is not None:
                        self.spritePosition = new_pos

        if self.handleThreats():
            self.game.weapon_group.add(self.spritePosition)
            return

        self.handleBottom()
        if not self.is_visible:
            self.spritePosition.kill()
            return

        self.game.weapon_group.add(self.spritePosition)

    def _advance_instant(self):
        """After a kill: move one position forward (no timer), check for more kills."""
        next_name = self.spritePosition.next_move
        if next_name is not None:
            self.spritePosition.kill()
            self.spritePosition = self.allPositions[next_name]

        if self.handleThreats():
            self.game.weapon_group.add(self.spritePosition)
            return

        self.handleBottom()
        if not self.is_visible:
            self._instant_mode = False
            self.spritePosition.kill()
            return

        self.game.weapon_group.add(self.spritePosition)

    def mustFall(self) -> bool:
        player = self.game.player
        return (player.sprite_position is not None
                and player.sprite_position.position_name == "H2J"
                and self.spritePosition == self.allPositions.get("N00"))

    def handleBottom(self):
        if self.spritePosition.position_name != "N03":
            return
        if self._killed_at_bottom:
            # Score finished for C09 kill: disappear immediately
            self.is_visible = False
            return
        # No kill at N03: wait one rhythm beat before disappearing
        now = pg.time.get_ticks()
        if self._bottom_arrival_time is None:
            self._bottom_arrival_time = now
        elif now - self._bottom_arrival_time >= self.game.animation_delay / 4:
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
                victim.do_kill()        # do_kill() → add_to_score() → is_score_paused = True
                self._instant_mode = True
                if self.spritePosition.position_name == "N03":
                    self._killed_at_bottom = True
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
