import pygame as pg

from positions.SpritePosition import *
from settings import INVINCIBLE, FPS


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
        self.is_dying = False
        self.death_start_time = 0
        self.last_blink_time = 0
        self.blink_visible = True
        self.collision_start_time = None
        self.h7f_entry_time = None
        self.last_jump_time = 0
        self.jump_apex_time = None

    def can_update(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_time) > self.game.animation_delay / 4:
            self.last_time = current_time
            return True
        return False

    def can_jump(self):
        current_time = pg.time.get_ticks()
        if (current_time - self.last_jump_time) > self.game.animation_delay:
            self.last_jump_time = current_time
            return True
        return False

    def trigger_death(self):
        if self.is_dying:
            return
        self.is_dying = True
        self.death_start_time = pg.time.get_ticks()
        self.last_blink_time = pg.time.get_ticks()
        self.blink_visible = True
        self.game.missed_sound.play()

    def update_death_animation(self):
        now = pg.time.get_ticks()
        if now - self.last_blink_time > 200:
            self.last_blink_time = now
            self.blink_visible = not self.blink_visible
            if self.blink_visible:
                self.game.player_group.add(self.sprite_position)
            else:
                self.sprite_position.kill()
        if now - self.death_start_time > 2000:
            self.is_dying = False
            self.blink_visible = True
            self.game.player_group.add(self.sprite_position)
            self.game.add_missed()
            if self.game.is_playing:
                self.start_of_game()

    def update(self, player_move):

        if not self.game.is_playing:
            self.game.player_group.empty()
            return

        if self.is_dying:
            self.update_death_animation()
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

        if player_move is None and self.jump_apex_time is not None:
            if pg.time.get_ticks() - self.jump_apex_time < self.game.animation_delay:
                newPosition = None
            else:
                self.jump_apex_time = None
        elif player_move in ("LEFT", "RIGHT", "UP", "DOWN"):
            self.jump_apex_time = None

        temp = self.handle_key()
        key_triggered = temp is not None
        if key_triggered:
            newPosition = temp

        self.handle_fall()

        self.handle_threats()

        if self.sprite_position.position_name == "H7F":
            if self.h7f_entry_time is None:
                self.h7f_entry_time = pg.time.get_ticks()
            if pg.time.get_ticks() - self.h7f_entry_time < self.game.animation_delay:
                return
            self.h7f_entry_time = None
        else:
            self.h7f_entry_time = None

        if newPosition != None:
            if player_move == "JUMP":
                if not self.can_jump():
                    return
                self.jump_apex_time = pg.time.get_ticks()
                eater = self.sprite_position.eater_name
                croco_jumped = eater is not None and any(
                    t.position_name == eater for t in self.game.threat_group
                )
            else:
                croco_jumped = False
                if not key_triggered and not self.can_update():
                    return
            prev_position_name = self.sprite_position.position_name
            self.sprite_position.kill()
            self.sprite_position = newPosition
            self.game.player_group.add(self.sprite_position)
            self.game.monkey_sound.play()
            if croco_jumped:
                self.game.add_to_score(1)
            if prev_position_name == "H6W":
                self.game.init_objects()
            player_move = None

    def start_of_game(self):

        self.game.player_group.empty()
        self.sprite_position = self.all_positions.get("L0G")
        self.game.player_group.add(self.sprite_position)
        self.collision_start_time = None
        self.jump_apex_time = None

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
            self.trigger_death()

    def grace_period(self):
        return max(0, self.game.animation_delay - 1000 // FPS)

    def handle_threats(self):
        eater = self.sprite_position.eater_name
        collider = next((t for t in self.game.threat_group if t.position_name == eater), None) if eater else None
        if collider is not None:
            if not INVINCIBLE:
                if self.collision_start_time is None:
                    self.collision_start_time = pg.time.get_ticks()
                elif pg.time.get_ticks() - self.collision_start_time >= self.grace_period():
                    self.trigger_death()
        else:
            self.collision_start_time = None

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
