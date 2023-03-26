import pygame as pg

from positions.SpritePosition import *
from settings import ANIMATION_DELAY, INVINCIBLE


class Player():
    """
    One and only one player.
    It should contains all of its different locations and sprites
    """

    def __init__(self, game):
        self.game = game
        self.is_new_turn = True
        self.all_positions = self.generate_positions()
        self.sprite_position = None
        self.player_move = None
        self.last_time = pg.time.get_ticks()
        # self.sound = makeSound("sounds/Monkey.wav")

    def can_update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_time) > ANIMATION_DELAY / 4:
            self.last_time = current_time
            return True
        return False

    def update(self, player_move):

        if not self.game.is_playing:
            return

        if self.is_new_turn:
            self.start_of_game()

        if player_move == None:
            newPosition = self.all_positions.get(
                self.sprite_position.next_move)
        elif player_move == "JUMP":
            newPosition = self.all_positions.get(
                self.sprite_position.jump_move)
        elif player_move == "LEFT":
            newPosition = self.all_positions.get(
                self.sprite_position.left_move)
        elif player_move == "RIGHT":
            newPosition = self.all_positions.get(
                self.sprite_position.right_move)
        elif player_move == "UP":
            newPosition = self.all_positions.get(self.sprite_position.up_move)
        elif player_move == "DOWN":
            newPosition = self.all_positions.get(
                self.sprite_position.down_move)

        temp = self.handle_key()
        if temp != None:
            newPosition = temp

        self.handle_fall()

        self.handle_threats()

        if newPosition != None:
            if not self.can_update():
                return
            self.sprite_position.kill()
            self.sprite_position = newPosition
            self.game.player_group.add(self.sprite_position)
            player_move = None

    def start_of_game(self):

        self.game.player_group.empty()
        self.sprite_position = self.all_positions.get("L0G")
        self.game.player_group.add(self.sprite_position)

        if self.sprite_position.position_name == "L0G" and self.is_new_turn:
            self.game.init_objects()
            self.is_new_turn = False

    def handle_key(self):
        if self.sprite_position.position_name == "H4J":
            if self.game.key.is_grabable:
                self.game.catch_key()
                # Grab key
                return self.all_positions.get("H5O")
            # miss key
            return self.all_positions.get("H7F")
        # do nothing
        return None

    def handle_fall(self):
        if self.sprite_position.position_name == "H7L":
            self.game.add_missed()

    def handle_threats(self):
        collider = pg.sprite.spritecollideany(
            self.sprite_position, self.game.threat_group)
        if collider != None and collider.position_name == self.sprite_position.eater_name:
            self.game.add_missed()

            if not INVINCIBLE and self.game.is_playing:
                self.start_of_game()

    def generate_positions(self):
        d = {}
        m = "Monkey"
        # Lower level
        d["L0G"] = SpritePosition("L0G", m)
        d["L0H"] = SpritePosition("L0H", m)
        d["L1G"] = SpritePosition("L1G", m)
        d["L1J"] = SpritePosition("L1J", m)
        d["L2G"] = SpritePosition("L2G", m)
        d["L2H"] = SpritePosition("L2H", m)
        d["L3G"] = SpritePosition("L3G", m)
        d["L3H"] = SpritePosition("L3H", m)
        d["L4G"] = SpritePosition("L4G", m)
        d["L4J"] = SpritePosition("L4J", m)
        d["L5G"] = SpritePosition("L5G", m)
        d["L5H"] = SpritePosition("L5H", m)

        # Higher level
        d["H0G"] = SpritePosition("H0G", m)
        d["H1G"] = SpritePosition("H1G", m)
        d["H1H"] = SpritePosition("H1H", m)
        d["H2G"] = SpritePosition("H2G", m)
        d["H2J"] = SpritePosition("H2J", m)
        d["H3G"] = SpritePosition("H3G", m)
        d["H3J"] = SpritePosition("H3J", m)
        # Juming to the key
        d["H4J"] = SpritePosition("H4J", m)
        # Taking the key
        d["H5T"] = SpritePosition("H5T", m)
        # Opening the cage and win
        d["H5O"] = SpritePosition("H5O", m)
        d["H6W"] = SpritePosition("H6W", m)
        # Fail to get the key and loose
        d["H7F"] = SpritePosition("H7F", m)
        d["H7L"] = SpritePosition("H7L", m)

        # Updating of positions
        # Lower level
        d["L0G"].jump_move = "L0H"
        d["L0G"].right_move = "L1G"

        d["L0H"].down_move = "L0G"
        d["L0H"].right_move = "L1J"

        d["L1G"].jump_move = "L1J"
        d["L1G"].left_move = "L0G"
        d["L1G"].right_move = "L2G"

        d["L1J"].next_move = "L1G"

        d["L2G"].jump_move = "L2H"
        d["L2G"].left_move = "L1G"
        d["L2G"].right_move = "L3G"

        d["L2H"].left_move = "L1J"
        d["L2H"].right_move = "L3H"
        d["L2H"].down_move = "L2G"

        d["L3G"].jump_move = "L3H"
        d["L3G"].left_move = "L2G"
        d["L3G"].right_move = "L4G"

        d["L3H"].left_move = "L2H"
        d["L3H"].right_move = "L4J"
        d["L3H"].down_move = "L3G"

        d["L4G"].jump_move = "L4J"
        d["L4G"].left_move = "L3G"
        d["L4G"].right_move = "L5G"

        d["L4J"].next_move = "L4G"

        d["L5G"].jump_move = "L5H"
        d["L5G"].left_move = "L4G"

        d["L5H"].left_move = "L4J"
        d["L5H"].up_move = "H0G"
        d["L5H"].down_move = "L5G"

        # Higher level
        d["H0G"].left_move = "H1G"
        d["H0G"].down_move = "L5H"

        d["H1G"].jump_move = "H1H"
        d["H1G"].left_move = "H2G"
        d["H1G"].right_move = "H0G"

        d["H1H"].down_move = "H1G"

        d["H2G"].jump_move = "H2J"
        d["H2G"].left_move = "H3G"
        d["H2G"].right_move = "H1G"

        d["H2J"].next_move = "H2G"
        d["H2J"].left_move = "H3G"

        d["H3G"].jump_move = "H3J"
        d["H3G"].left_move = "H7F"
        d["H3G"].up_move = "H4J"
        d["H3G"].right_move = "H2G"

        d["H3J"].next_move = "H3G"

        # Taking the key
        d["H5T"].next_move = "H5O"
        # Opening the cage and win
        d["H5O"].next_move = "H6W"
        d["H6W"].next_move = "L0G"
        # Fail to get the key and loose
        d["H7F"].next_move = "H7L"
        d["H7L"].next_move = "L0G"

        # Threats
        d["L0G"].eater_name = "C11"
        d["L0H"].eater_name = "B01"
        d["L1G"].eater_name = "C10"
        d["L1J"].eater_name = "B02"
        d["L2G"].eater_name = "C09"
        d["L2H"].eater_name = "B03"
        d["L3G"].eater_name = "C08"
        d["L3H"].eater_name = "B04"
        d["L4G"].eater_name = "C07"
        d["L4J"].eater_name = "B05"
        d["L5G"].eater_name = "C06"
        d["L5H"].eater_name = "B06"
        d["H0G"].eater_name = "C04"
        d["H1G"].eater_name = "C03"
        d["H2G"].eater_name = "C02"
        d["H3G"].eater_name = "C01"

        return d
