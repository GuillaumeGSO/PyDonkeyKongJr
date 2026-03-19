import pygame as pg

from settings import SCORE_DELAY


class Score():
    """
    Display the score with sound, animating point increments via SCORE_DELAY.
    Points are queued by add_points() and consumed one-at-a-time in update().
    """

    def __init__(self, screen, sound):
        self.screen = screen
        self.score = 0
        self._pending = 0
        self._last_time = 0
        self._channel = None
        self.score_font = pg.font.Font("fonts/Open 24 Display St.ttf", 72)
        self.sound = sound
        self.score_surface = self.score_font.render(" 0", True, "black", (254, 254, 254))

    @property
    def is_counting(self):
        return self._pending > 0

    def add_points(self, points):
        self._pending += points

    def update(self):
        now = pg.time.get_ticks()
        if self._channel and self._channel.get_busy():
            return
        if self._pending > 0 and now - self._last_time >= SCORE_DELAY:
            self.score += 1
            self._pending -= 1
            self._last_time = now
            self._channel = self.sound.play()
        self.score_surface = self.score_font.render(
            " " + str(self.score), True, "black", (254, 254, 254))

    def draw(self):
        score_rect = self.score_surface.get_rect()
        score_rect.right = 685
        self.screen.blit(self.score_surface, score_rect)
