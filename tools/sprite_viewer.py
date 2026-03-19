import os
import sys

import pygame as pg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from positions.SpritePosition import SpritePosition
from settings import WIDTH, HEIGHT

ACTOR_TYPES = ["Bird", "Cage", "Croco", "Key", "Missed", "Monkey", "Nut"]


class SpriteViewer:
    """
    Shows all sprites placed at their calibrated positions on the empty background.
    Press SPACE to toggle between the sprite layout and the arcade reference screenshot.
    Press ESC to quit.
    """

    def __init__(self):
        pg.init()
        pg.display.set_caption("Sprite Viewer — SPACE: toggle reference | ESC: quit")
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.empty_bg = pg.image.load("img/EmptyScreen.png").convert()
        self.full_bg = pg.image.load("tools/img/FullScreen.png").convert()
        self.sprites = []
        self.show_reference = False
        self._load_all_sprites()

    def _load_all_sprites(self):
        for actor_type in ACTOR_TYPES:
            positions = SpritePosition.getAllPositions(actor_type)
            for name, (x, y) in positions.items():
                img_path = f"img/sprites/{actor_type}/{name}.png"
                if os.path.isfile(img_path):
                    image = pg.image.load(img_path).convert_alpha()
                    rect = image.get_rect()
                    rect.x, rect.y = x, y
                    self.sprites.append((image, rect))

    def run(self):
        clock = pg.time.Clock()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
                ):
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.show_reference = not self.show_reference

            if self.show_reference:
                self.screen.blit(self.full_bg, (0, 0))
            else:
                self.screen.blit(self.empty_bg, (0, 0))
                for image, rect in self.sprites:
                    self.screen.blit(image, rect)

            pg.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    SpriteViewer().run()
