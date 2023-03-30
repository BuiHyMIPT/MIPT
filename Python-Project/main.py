# CREATE BACKGROUND AND BASE OF GAME
import pygame
import sys
import random

pygame.init()

# create window
screen = pygame.display.set_mode((432, 768))

# set fps of the game
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# add gravity
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0

game_active = True

# create bg
bg = pygame.image.load('imgs/bg.png').convert()
bg = pygame.transform.scale2x(bg)

# create bird
bird_down = pygame.transform.scale2x(pygame.image.load('imgs/bird3.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('imgs/bird2.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('imgs/bird1.png')).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]  # 0 1 2
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('imgs/bird2.png').convert_alpha()
# bird = pygame.transform.scale2x(bird)

# create rect aground bird
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
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 820))
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


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


# tao ham xoay
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def get_score():
    global score, pipe_list
    for pipe in pipe_list:
        if 95 < pipe.centerx < 105 and bird_rect.centery < pipe.centery:
            score += 1
            return score
    return score


def get_high_score():
    return high_score


def draw_score(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(get_score()), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(get_score())}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 150))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(get_high_score())}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(216, 50))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score



# create pipe
pipe_surface = pygame.image.load('imgs/pipe.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# create timber for pipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height = [200, 250, 300, 350, 400]

# create timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 100)

# while loop of the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -5
            if event.key == pygame.K_1 and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()

    screen.blit(bg, (0, 0))
    if game_active:
        # bird
        bird_movement += gravity
        # tao ham xoay chim
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        draw_score('main game')
    else:
        high_score = update_score(score, high_score)
        draw_score('game_over')
    # base
    base_x_pos -= 1
    draw_base()
    # base1 -> base2-> base1 ...
    if base_x_pos <= -432:
        base_x_pos = 0
    pygame.display.update()
    clock.tick(80)
