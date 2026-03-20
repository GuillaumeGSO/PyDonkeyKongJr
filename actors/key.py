import pygame as pg

from positions.graph_loader import load_position_graph

class Key():
    """
    The key is moving back and forth...
    """

    def __init__(self, game):
        self.game = game
        self.is_visible = True
        self.is_grabable = False
        self.all_positions = self.generate_positions()
        self.sprite_position = None
        self.last_time = pg.time.get_ticks()

    def can_update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_time) > self.game.animation_delay:
            self.last_time = current_time
            return True
        return False

    def update(self):

        if not self.is_visible:
            return

        if not self.can_update():
            return

        if self.sprite_position is None:
            self.sprite_position = self.all_positions.get("K00")
            return

        newPosition = self.all_positions.get(self.sprite_position.next_move)

        self.sprite_position.kill()
        if newPosition is not None:
            self.sprite_position = newPosition

        self.is_grabable = self.sprite_position.position_name == "K03"
        self.game.cage_group.add(self.sprite_position)

    def catch_key(self):
        self.sprite_position.kill()
        self.is_visible = False
        self.is_grabable = False
        self.game.cage.open_cage()

    def init_key(self):
        self.is_visible = True
        self.sprite_position = None

    def generate_positions(self):
        return load_position_graph("Key")
