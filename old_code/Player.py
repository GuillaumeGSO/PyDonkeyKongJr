import pygame

GREEN = (0, 255, 0)
SPRITE_BG= (254, 254, 254)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('spriteMonkey01.png').convert()
        self.image.set_colorkey(SPRITE_BG)
        self.rect = self.image.get_rect()