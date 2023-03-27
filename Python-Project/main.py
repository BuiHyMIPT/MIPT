# CREATE BACKGROUND AND BASE OF GAME
import pygame
import sys
import os

pygame.init()

# create window
screen = pygame.display.set_mode((432, 768))

# set fps of the game (fast or slow)
clock = pygame.time.Clock()

# create bg
bg = pygame.image.load('imgs/bg.png')
bg = pygame.transform.scale2x(bg)

# create base
base = pygame.image.load('imgs/base.png')
base = pygame.transform.scale2x(base)

base_x_pos = 0

# base run
def draw_base():
    screen.blit(base, (base_x_pos, 630))
    screen.blit(base, (base_x_pos + 432, 630))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg, (0, 0))
    base_x_pos -= 1
    draw_base()
    # base1 -> base2-> base1 ...
    if base_x_pos <= -432:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(100)
