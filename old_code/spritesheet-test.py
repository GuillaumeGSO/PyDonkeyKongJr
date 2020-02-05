import spritesheet
import pygame
import time
from pygame.locals import*

run = True
win = pygame.display.set_mode((800,600),pygame.DOUBLEBUF, 32)

sprite_set = pygame.image.load("FullScreen.png").convert()
transColor = pygame.Color(254, 254, 254)
sprite_set.set_colorkey(transColor)
sprites = [sprite_set.subsurface([i*22,0,22,40]) for i in range(4)] # ligne qui t'intéresse
 
 
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT: run = False
 
    win.fill((70,100,50))
    for i, s in enumerate(sprites):
        win.blit(s, [i*200,200])
        pygame.draw.rect(win, (0,0,0), [i*200,200,22,40],1)
    pygame.display.flip()
    time.sleep(0.1)
 
pygame.quit()
"""
ss = spritesheet.spritesheet('FullScreen.png')
# Sprite is 16x16 pixels at location 0,0 in the file...
image = ss.image_at((0, 0, 16, 16))
images = []
# Load two images into an array, their transparent bit is (254, 254, 254)
images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(254, 254, 254))
"""

