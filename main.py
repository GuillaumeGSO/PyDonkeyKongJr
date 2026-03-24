"""
Thanks :
http://pica-pic.com/donkey_kong_jr/
https://www.youtube.com/watch?v=K9CoOYqqVLU
# http://www.github.com/stevepaget/pygame_functions
https://mamedev.emulab.it/haze/2017-new-focus/

https://www.homecomputermuseum.nl/en/collectie/nintendo/nintendo-donkey-kong-jr-game-watch/?srsltid=AfmBOooyZpKdw5h7MVzEfqAB4Fy5YgPEx6ScA9MCJDGOvq3HgaZholyS
"""

import asyncio
import os
import sys

import pygame as pg

from donkey_kong_jr import DonkeyKongJr
from settings import SCREEN_NAME, WIDTH, HEIGHT, FPS, DEVICE_SCREEN_RAW


class App:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(SCREEN_NAME)

        # Scale Device.png so its screen area maps exactly to WIDTH x HEIGHT
        raw_x, raw_y, raw_w, raw_h = DEVICE_SCREEN_RAW
        device_raw = pg.image.load(os.path.join("img", "Device.png"))
        scale_x = WIDTH / raw_w
        scale_y = HEIGHT / raw_h
        device_w = int(device_raw.get_width() * scale_x)
        device_h = int(device_raw.get_height() * scale_y)
        device_scaled = pg.transform.scale(device_raw, (device_w, device_h))
        self.device_offset = (int(raw_x * scale_x), int(raw_y * scale_y))

        self.screen = pg.display.set_mode((device_w, device_h))
        self.device_frame = device_scaled.convert_alpha()
        self.game_surface = pg.Surface((WIDTH, HEIGHT)).convert()
        self.bg = pg.image.load(os.path.join(
            "img", "EmptyScreen.png")).convert()

        # Semi-transparent LCD tint (grey-green) over the game area
        self.lcd_overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        self.lcd_overlay.fill((114, 129, 122, 128))  # grey-green, alpha=90/255

        self.game_surface.blit(self.bg, [0, 0])

        self.missed_sound = pg.mixer.Sound(os.path.join("sounds", "Missed.wav"))
        self.croco_sound  = pg.mixer.Sound(os.path.join("sounds", "Croco.wav"))
        self.monkey_sound = pg.mixer.Sound(os.path.join("sounds", "Monkey.wav"))
        self.score_sound  = pg.mixer.Sound(os.path.join("sounds", "Score.wav"))

        self.clock = pg.time.Clock()
        self.game = DonkeyKongJr(self)

    def update(self):
        self.game.update()
        self.clock.tick(FPS)

    def draw(self):
        self.game.draw()
        self.game_surface.blit(self.lcd_overlay, (0, 0))
        self.screen.blit(self.device_frame, (0, 0))
        self.screen.blit(self.game_surface, self.device_offset)
        pg.display.flip()

    def check_events(self):
        self.game.player_move = None
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.game_surface.blit(self.bg, [0, 0])
                    self.game = DonkeyKongJr(self)
                elif event.key == pg.K_LEFT:
                    self.game.player_move = "LEFT"
                elif event.key == pg.K_RIGHT:
                    self.game.player_move = "RIGHT"
                elif event.key == pg.K_UP:
                    self.game.player_move = "UP"
                elif event.key == pg.K_DOWN:
                    self.game.player_move = "DOWN"
                elif event.key == pg.K_SPACE:
                    self.game.player_move = "JUMP"

    async def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            await asyncio.sleep(0)


async def main():
    app = App()
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
