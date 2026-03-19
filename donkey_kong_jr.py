import pygame as pg

from actors.bird import Bird
from actors.cage import Cage
from actors.nut import Nut
from actors.croco import Croco
from actors.key import Key
from actors.missed import Missed
from actors.player import Player
from actors.score import Score
from settings import *


class DonkeyKongJr:
    def __init__(self, app):
        self.app = app
        self.number_of_life = 0
        self.is_playing = True
        self.level = 0
        self.animation_delay = ANIMATION_DELAY

        self.missed_sound = app.missed_sound
        self.croco_sound  = app.croco_sound
        self.monkey_sound = app.monkey_sound

        self.player_group: pg.sprite.Group = pg.sprite.Group()
        self.weapon_group: pg.sprite.Group = pg.sprite.Group()
        self.cage_group: pg.sprite.Group = pg.sprite.Group()
        self.threat_group: pg.sprite.Group = pg.sprite.Group()
        self.info_group: pg.sprite.Group = pg.sprite.Group()

        self.birds = [Bird(self)]
        self.crocos = [Croco(self)]
        self.cage = Cage(self)
        self.nut = Nut(self)
        self.key = Key(self)
        self.missed = Missed(self)
        self.score = Score(self.app.screen, self.app.score_sound)
        self.player = Player(self)
        self.player_move = None
        self.is_score_paused = False

    def update(self):
        if self.is_score_paused:
            self.score.update()
            if not self.score.is_counting:
                self.is_score_paused = False
            self.nut.update()
            return

        self.player.update(self.player_move)
        for croco in self.crocos:
            croco.update()
        for bird in self.birds:
            bird.update()
        self.nut.update()
        self.key.update()
        self.score.update()
        self.missed.update()
        self.cage.update()

    def draw(self):
        self.app.screen.blit(self.app.bg, (0, 0))

        self.player_group.draw(self.app.screen)
        self.info_group.draw(self.app.screen)
        self.threat_group.draw(self.app.screen)
        self.weapon_group.draw(self.app.screen)
        self.cage_group.draw(self.app.screen)
        self.score.draw()

    def catch_key(self):
        self.key.catch_key()
        self._clear_path_threats()

    def _clear_path_threats(self):
        bird_danger = {"B00", "B01", "B02", "B03"}
        croco_danger = {"C10", "C11", "C12"}
        for bird in self.birds:
            if bird.spritePosition and bird.spritePosition.position_name in bird_danger:
                bird.do_kill()
        for croco in self.crocos:
            if croco.spritePosition and croco.spritePosition.position_name in croco_danger:
                croco.do_kill()

    def add_to_score(self, points):
        self.score.add_points(points)
        self.is_score_paused = True

    def add_missed(self):
        if INVINCIBLE:
            self.number_of_life = 0
        self.missed.miss(self.number_of_life)
        self.number_of_life += 1
        self.init_objects()
        if self.number_of_life == NUMBER_OF_LIFE:
            self.is_playing = False

    def init_objects(self):
        if self.cage.fully_opened:
            self.level += 1
            self.animation_delay = max(MIN_ANIMATION_DELAY, ANIMATION_DELAY - self.level * DIFFICULTY_STEP)
            self._maybe_spawn_enemy()
        if not self.key.is_visible:
            self.key.init_key()
        if not self.nut.is_visible:
            self.nut.init_nut()
        for croco in self.crocos:
            if croco.is_killed:
                croco.init()
        for bird in self.birds:
            if bird.is_killed:
                bird.init()
        if self.cage.fully_opened:
            self.cage.init_cage()

    def _maybe_spawn_enemy(self):
        if self.level % 2 == 1 and len(self.crocos) < MAX_CROCOS:
            self.crocos.append(Croco(self))
        elif self.level % 2 == 0 and len(self.birds) < MAX_BIRDS:
            self.birds.append(Bird(self))
