# Pygame template - skeleton for a new pygame project
import pygame
import random
from Player import Player
from pygame.locals import *

WIDTH = 700
HEIGHT = 480
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SPRITE_BG= (254, 254, 254)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Jr.")
clock = pygame.time.Clock()

bg = pygame.image.load("EmptyScreen.png").convert()
screen.blit(bg, (0,0))

all_sprites = pygame.sprite.Group()


donkeys = []
donkeys.append({"x":75, "y":430, "img":pygame.image.load("spriteMonkey01.png").convert_alpha()}) 
donkeys.append({"x":150, "y":430, "img":pygame.image.load("spriteMonkey02.png").convert_alpha()})
donkeys.append({"x":210, "y":430, "img":pygame.image.load("spriteMonkey01.png").convert_alpha()})
donkeys.append({"x":270, "y":430, "img":pygame.image.load("spriteMonkey02.png").convert_alpha()})
donkeys.append({"x":350, "y":430, "img":pygame.image.load("spriteMonkey01.png").convert_alpha()})
donkeys.append({"x":430, "y":430, "img":pygame.image.load("spriteMonkey02.png").convert_alpha()})
donkeys.append({"x":510, "y":430, "img":pygame.image.load("spriteMonkey01.png").convert_alpha()})
donkeys.append({"x":590, "y":430, "img":pygame.image.load("spriteMonkey02.png").convert_alpha()})
donkeys.append({"x":670, "y":430, "img":pygame.image.load("spriteMonkey01.png").convert_alpha()})

#Init position of first Donkey
numDonkey=0
actualDonkey = donkeys[numDonkey]

perso = actualDonkey["img"]
perso.set_colorkey(SPRITE_BG)
position_perso = perso.get_rect()
position_perso.center = (actualDonkey["x"], actualDonkey["y"])

#all_sprites.add(perso)
# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_SPACE:
            print("Jump")
        if event.type == KEYDOWN and event.key == K_RIGHT:
            print("Right")
            if numDonkey < 8:
                numDonkey+=1
            actualDonkey=donkeys[numDonkey % len(donkeys)]
            perso = actualDonkey["img"]
            perso.set_colorkey(SPRITE_BG)
            position_perso = perso.get_rect()
            position_perso.center = (actualDonkey["x"], actualDonkey["y"])
        if event.type == KEYDOWN and event.key == K_LEFT:
            print("Left")
            if numDonkey > 1:
                numDonkey-=1
            actualDonkey=donkeys[numDonkey % len(donkeys)]
            perso = actualDonkey["img"]
            perso.set_colorkey(SPRITE_BG)
            position_perso = perso.get_rect()
            position_perso.center = (actualDonkey["x"], actualDonkey["y"])    
        if event.type == KEYDOWN and event.key == K_UP:
            print("Up")
            position_perso.y-=100
        if event.type == KEYDOWN and event.key == K_DOWN:
            print("Down")
            position_perso.y+=100
            
        screen.blit(bg, (0, 0))
        screen.blit(perso, position_perso)
        


    # Update
    all_sprites.update()

    # Draw / render
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

