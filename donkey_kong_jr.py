import pygame as pg

from actors.bird import Bird
from actors.cage import Cage
from actors.coco import Coco
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
        self.player_group: pg.sprite.Group = pg.sprite.Group()
        self.weapon_group: pg.sprite.Group = pg.sprite.Group()
        self.cage_group: pg.sprite.Group = pg.sprite.Group()
        self.threat_group: pg.sprite.Group = pg.sprite.Group()
        self.info_group: pg.sprite.Group = pg.sprite.Group()

        self.bird = Bird(self)
        self.croco = Croco(self)
        self.cage = Cage(self)
        self.coco = Coco(self)
        self.key = Key(self)
        self.missed = Missed(self)
        self.score = Score(self.app.screen)
        self.player = Player(self)
        self.player_move = None

    def update(self):
        self.croco.update()
        self.bird.update()
        self.coco.update()
        if self.is_playing:
            self.player.update(self.player_move)
        self.key.update()
        self.score.update()
        self.missed.update()
        self.cage.update()

    def draw(self):
        if self.is_playing:
            self.player_group.clear(self.app.screen, self.app.bg)

        self.info_group.clear(self.app.screen, self.app.bg)
        self.threat_group.clear(self.app.screen, self.app.bg)
        self.cage_group.clear(self.app.screen, self.app.bg)
        self.weapon_group.clear(self.app.screen, self.app.bg)

        if self.is_playing:
            self.player_group.draw(self.app.screen)

        self.info_group.draw(self.app.screen)
        self.threat_group.draw(self.app.screen)
        self.weapon_group.draw(self.app.screen)
        self.cage_group.draw(self.app.screen)
        self.score.draw()

    def catch_key(self):
        self.key.catch_key()

    def add_to_score(self, points):
        self.score.add_points(points)

    def add_missed(self):
        self.missed.miss(self.number_of_life)
        self.number_of_life += 1
        if self.number_of_life == NUMBER_OF_LIFE:
            self.is_playing = False

    def init_objects(self):
        if not self.key.is_visible:
            self.key.init_key()
        if not self.coco.is_visible:
            self.coco.init_coco()
        if self.cage.fully_opened:
            self.cage.init_cage()
