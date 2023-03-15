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
        self.threat_group: pg.sprite.Group = pg.sprite.Group()
        self.player_group: pg.sprite.Group = pg.sprite.Group()
        self.weapon_group: pg.sprite.Group = pg.sprite.Group()
        self.cage_group: pg.sprite.Group = pg.sprite.Group()
        self.info_group: pg.sprite.Group = pg.sprite.Group()

        self.bird = Bird(self)
        self.croco = Croco(self)
        self.cage = Cage(self)
        self.coco = Coco(self)
        self.key = Key(self)
        self.missed = Missed(self)
        self.score = Score(self)
        self.player = Player(self)
        self.playerMove = None

    def update(self):
        self.player.update(self.playerMove)
        self.croco.update()
        self.bird.update()
        self.cage.update()
        self.coco.update()
        self.key.update()
        self.missed.update()
        self.score.update()

    def draw(self):
        self.threat_group.clear(self.app.screen, self.app.bg)
        self.player_group.clear(self.app.screen, self.app.bg)
        self.weapon_group.clear(self.app.screen, self.app.bg)
        self.cage_group.clear(self.app.screen, self.app.bg)
        self.info_group.clear(self.app.screen, self.app.bg)
        self.threat_group.draw(self.app.screen)
        self.player_group.draw(self.app.screen)
        self.weapon_group.draw(self.app.screen)
        self.cage_group.draw(self.app.screen)
        self.info_group.draw(self.app.screen)
