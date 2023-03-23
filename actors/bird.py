# from pygame_functions import *
import pygame as pg
from actors.threat import Threat

from positions.SpritePosition import *
from settings import ANIMATION_DELAY


class Bird(Threat):
    """
    Bird crossing from left to right high, from right to left lower
    """

    def init(self):
        super()
        self.is_killed = False

    def get_start_position(self):
        return "B00"

    def get_points_for_kill(self):
        return 10

    def generate_positions(self):
        d = {}
        b = "Bird"
        d["B00"] = SpritePosition("B00", b)
        d["B01"] = SpritePosition("B01", b)
        d["B02"] = SpritePosition("B02", b)
        d["B03"] = SpritePosition("B03", b)
        d["B04"] = SpritePosition("B04", b)
        d["B05"] = SpritePosition("B05", b)
        d["B06"] = SpritePosition("B06", b)
        d["B07"] = SpritePosition("B07", b)

        d["B00"].next_move = "B01"
        d["B01"].next_move = "B02"
        d["B02"].next_move = "B03"
        d["B03"].next_move = "B04"
        d["B04"].next_move = "B05"
        d["B05"].next_move = "B06"
        d["B06"].next_move = "B07"
        d["B07"].next_move = "B00"

        return d
