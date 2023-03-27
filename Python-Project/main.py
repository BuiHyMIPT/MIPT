# CREATE BACKGROUND AND BASE OF GAME
import pygame
import sys
import random

pygame.init()

# create window
screen = pygame.display.set_mode((432, 768))

# set fps of the game (fast or slow)
clock = pygame.time.Clock()

# add gravity
gravity = 0.25
bird_movement = 0

# create bg
bg = pygame.image.load('imgs/bg.png').convert()
bg = pygame.transform.scale2x(bg)

# create bird
bird = pygame.image.load('imgs/bird2.png').convert()
bird = pygame.transform.scale2x(bird)

# create rect aground the bird
bird_rect = bird.get_rect(center=(100, 384))

# create base
base = pygame.image.load('imgs/base.png').convert()
base = pygame.transform.scale2x(base)

base_x_pos = 0


# all functions of the game
def draw_base():
    screen.blit(base, (base_x_pos, 650))
    screen.blit(base, (base_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # random_pipe_pos = random.randrange(50, 400)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 800))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# create pipe
pipe_surface = pygame.image.load('imgs/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# create timber
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -11
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    screen.blit(bg, (0, 0))
    # bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird, bird_rect)
    # pipe
    pipe_list = move_pipe(pipe_list)
    draw_pipe(pipe_list)
    # base
    base_x_pos -= 1
    draw_base()
    # base1 -> base2-> base1 ...
    if base_x_pos <= -432:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(100)
