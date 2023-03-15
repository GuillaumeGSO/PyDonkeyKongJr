from settings import *
import pygame as pg
from actors.bird import Bird
from actors.cage import Cage
from actors.coco import Coco
from actors.key import Key
from actors.missed import Missed
from actors.player import Player
from actors.score import Score


class DonkeyKongJr:
    def __init__(self, app):
        self.app = app
        self.sprite_group: pg.sprite.Group = pg.sprite.Group()
        self.bird = Bird(self)
        self.cage = Cage(self)
        self.coco = Coco(self)
        self.key = Key(self)
        self.missed = Missed(self)
        self.score = Score(self)
        self.player = Player(self)
        self.playerMove = None


    def update(self):
        self.player.update(self.playerMove)
        self.bird.update()
        self.cage.update()
        self.coco.update()
        self.key.update()
        self.missed.update()
        self.score.update()

    def draw(self):
        self.sprite_group.clear(self.app.screen, self.app.bg)
        self.sprite_group.draw(self.app.screen)