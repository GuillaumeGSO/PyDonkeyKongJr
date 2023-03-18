"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
# http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

"""

import os
import sys

import pygame as pg

from donkey_kong_jr import DonkeyKongJr
from settings import *


class App:

    def __init__(self):
        pg.init()
        pg.display.set_caption(SCREEN_NAME)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.bg = pg.image.load(os.path.join(
            "img", "EmptyScreen.png")).convert()

        # TO DISPLAY ORIGINAL SCREEN WITH ALL SPRITES
        # self.bg = pg.image.load(os.path.join(
        #     "positions", "FullScreen.png")).convert()

        self.screen.blit(self.bg, [0, 0])

        color = (255, 255, 0)
        self.screen.fill(color)

        self.clock = pg.time.Clock()
        self.game = DonkeyKongJr(self)

    def update(self):
        self.game.update()
        self.clock.tick(FPS)

    def draw(self):
        self.game.draw()
        pg.display.flip()

    def check_events(self):
        self.game.playerMove = None
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.game.playerMove = "LEFT"
                elif event.key == pg.K_RIGHT:
                    self.game.playerMove = "RIGHT"
                elif event.key == pg.K_UP:
                    self.game.playerMove = "UP"
                elif event.key == pg.K_DOWN:
                    self.game.playerMove = "DOWN"
                elif event.key == pg.K_SPACE:
                    self.game.playerMove = "JUMP"

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
