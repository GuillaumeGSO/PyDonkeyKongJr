import pygame as pg


class Score():
    """
    Display the score with sound
    """

    def __init__(self, screen, sound):
        self.screen = screen
        self.score = 0
        self.score_font = pg.font.Font("fonts/Open 24 Display St.ttf", 72)
        self.sound = sound

    def update(self):
        self.score_surface = self.score_font.render(
            " " + str(self.score), True, "black", (254, 254, 254))

    def draw(self):
        score_rect = self.score_surface.get_rect()
        score_rect.right = 685
        self.screen.blit(self.score_surface, score_rect)

    def add_points(self, points):
        for _ in range(points):
            self.score += 1
            self.update()
            self.draw()
            pg.display.update()
            channel = self.sound.play()
            if channel:
                while channel.get_busy():
                    pg.time.wait(10)
