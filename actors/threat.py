from abc import ABC, abstractmethod
import pygame as pg


class Threat(ABC):

    def __init__(self, game):
        self.game = game
        self.all_positions = self.generate_positions()
        self.init()
        self.last_time = pg.time.get_ticks()
        self.sprite_position = None
        self.is_killed = False

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def get_start_position():
        pass

    @abstractmethod
    def get_points_for_kill():
        pass

    @abstractmethod
    def generate_positions(self):
        pass

    def can_update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_time) > self.game.animation_delay:
            self.last_time = current_time
            return True
        return False

    def do_kill(self):
        self.is_killed = True
        self.game.add_to_score(self.get_points_for_kill())
        # Sprite stays in threat_group so it remains visible during score pause

    def finalize_kill(self):
        """Remove sprite from group after score pause ends."""
        if self.sprite_position is not None:
            self.game.threat_group.remove(self.sprite_position)
            self.sprite_position = None

    def update(self):
        if self.is_killed:
            return

        if self.game.player.is_dying:
            return

        if not self.can_update():
            return

        if self.sprite_position is None:
            self.sprite_position = self.all_positions.get(self.get_start_position())
            return
        newPosition = self.all_positions.get(self.sprite_position.next_move)
        self.sprite_position.kill()
        if newPosition is not None:
            self.sprite_position = newPosition
        self.game.threat_group.add(self.sprite_position)
        self.game.croco_sound.play()
