import pygame as pg

from positions.graph_loader import load_position_graph


class Nut():
    """
    The coconut falls when touched by monkey and respawn when monkey starts.
    Falls at player speed. Pauses on each kill to score, then continues falling.
    Can kill multiple enemies in one drop.
    """

    def __init__(self, game):
        self.game = game
        self.all_positions = self.generate_positions()
        self.init_nut()

    def init_nut(self):
        self.is_visible = True
        self.sprite_position = None
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
        if self.sprite_position is None:
            self.sprite_position = self.all_positions.get("N00")
            return
        if not self.is_visible:
            return

        # Score pause: keep nut visible; game handles the unpause
        if self.game.is_score_paused:
            self.game.weapon_group.add(self.sprite_position)
            return

        # After any kill: instantly traverse remaining positions
        if self._instant_mode:
            self._advance_instant()
            return

        # Normal animated fall
        if self.must_fall():
            if self.can_update():
                self.sprite_position.kill()
                self.sprite_position = self.all_positions.get("N01")
        elif self.sprite_position.position_name != "N00":
            if self.can_update():
                next_name = self.sprite_position.next_move
                if next_name is not None:       # guard: N03 has no next_move
                    new_pos = self.all_positions.get(next_name)
                    self.sprite_position.kill()
                    if new_pos is not None:
                        self.sprite_position = new_pos

        if self.handle_threats():
            self.game.weapon_group.add(self.sprite_position)
            return

        self.handle_bottom()
        if not self.is_visible:
            self.sprite_position.kill()
            return

        self.game.weapon_group.add(self.sprite_position)

    def _advance_instant(self):
        """After a kill: move one position forward (no timer), check for more kills."""
        next_name = self.sprite_position.next_move
        if next_name is not None:
            self.sprite_position.kill()
            self.sprite_position = self.all_positions[next_name]

        if self.handle_threats():
            self.game.weapon_group.add(self.sprite_position)
            return

        self.handle_bottom()
        if not self.is_visible:
            self._instant_mode = False
            self.sprite_position.kill()
            return

        self.game.weapon_group.add(self.sprite_position)

    def must_fall(self) -> bool:
        player = self.game.player
        return (player.sprite_position is not None
                and player.sprite_position.position_name == "H2J"
                and self.sprite_position == self.all_positions.get("N00"))

    def handle_bottom(self):
        if self.sprite_position.position_name != "N03":
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

    def handle_threats(self) -> bool:
        entry = self.KILL_MAP.get(self.sprite_position.position_name)
        if entry is None:
            return False
        actor_type, target_pos = entry
        victims = self.game.crocos if actor_type == "Croco" else self.game.birds
        for victim in victims:
            if victim.sprite_position and victim.sprite_position.position_name == target_pos:
                victim.do_kill()        # do_kill() → add_to_score() → is_score_paused = True
                self._instant_mode = True
                if self.sprite_position.position_name == "N03":
                    self._killed_at_bottom = True
                return True
        return False

    def generate_positions(self):
        return load_position_graph("Nut")
