import pygame as pg

from positions.graph_loader import load_position_graph
from settings import INVINCIBLE, FPS, DEATH_BLINK_INTERVAL, DEATH_ANIMATION_DURATION


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
        if now - self.last_blink_time > DEATH_BLINK_INTERVAL:
            self.last_blink_time = now
            self.blink_visible = not self.blink_visible
            if self.blink_visible:
                self.game.player_group.add(self.sprite_position)
            else:
                self.sprite_position.kill()
        if now - self.death_start_time > DEATH_ANIMATION_DURATION:
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

        if player_move is None:
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

        if newPosition is not None:
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
        return load_position_graph("Monkey")
