from abc import ABC, abstractmethod
import pygame as pg
from positions.SpritePosition import SpritePosition

from settings import ANIMATION_DELAY


class Threat(ABC):

    def __init__(self, game):
        self.game = game
        self.all_positions = self.generate_positions()
        self.init()
        self.last_time = pg.time.get_ticks()
        self.spritePosition = None
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
        if (current_time - self.last_time) > ANIMATION_DELAY:
            self.last_time = current_time
            return True
        return False

    def do_kill(self):
        self.is_killed = True
        self.game.threat_group.remove(self.spritePosition)
        self.game.add_to_score(self.get_points_for_kill())
        self.spritePosition: SpritePosition == None

    def update(self):
        if self.is_killed:
            return

        if not self.can_update():
            return

        if self.spritePosition == None:
            self.spritePosition = self.all_positions.get(
                self.get_start_position())
            return
        newPosition = self.all_positions.get(self.spritePosition.next_move)
        self.spritePosition.kill()
        if newPosition != None:
            self.spritePosition = newPosition
        self.game.threat_group.add(self.spritePosition)
