import pygame as pg


class Score():
    """
    Display the score with sound
    """

    def __init__(self):
        self.score = 0
        self.score_font = pg.font.Font("fonts/Open 24 Display St.ttf", 72)
        # self.sound = makeSound("sounds/Score.wav")

    def update(self):
        self.score_surface = self.score_font.render(
            " " + str(self.score), True, "black", (254, 254, 254))

    def draw(self, screen):
        score_rect = self.score_surface.get_rect()
        score_rect.right = 685
        screen.blit(self.score_surface, score_rect)

    def addPoints(self, points):
        print("add score")
        self.score += points
        # self.draw_text(self.game.app.screen, self.score)
        # self.game.playSound(self.sound)
