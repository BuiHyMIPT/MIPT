# Пока не знаем, почему она еще ошиблась
import os
import sys
import unittest
import pygame

from src.main import check_collision, move_pipe, rotate_bird, bird_animation, get_score

# Add the path to the game module to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


class TestPlappyBird(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((432, 768))
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', '04B_19.ttf')), 35)
        self.bird_down = pygame.transform.scale2x(pygame.image.load(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'imgs', 'bird3.png')))).convert_alpha()
        self.bird_mid = pygame.transform.scale2x(pygame.image.load(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'imgs', 'bird2.png')))).convert_alpha()
        self.bird_up = pygame.transform.scale2x(pygame.image.load(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'imgs', 'bird1.png')))).convert_alpha()
        self.bird_list = [self.bird_down, self.bird_mid, self.bird_up]
        self.bird_index = 0
        self.bird = self.bird_list[self.bird_index]
        self.bird_rect = self.bird.get_rect(center=(100, 384))
        self.base = pygame.image.load(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'imgs', 'base.png'))).convert()
        self.base = pygame.transform.scale2x(self.base)
        self.base_x_pos = 0
        self.gravity = 0.25
        self.bird_movement = 0
        self.pipe_surface = pygame.image.load(
            os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'imgs', 'pipe.png'))).convert()
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.spawnpipe = pygame.USEREVENT
        pygame.time.set_timer(self.spawnpipe, 1500)
        self.pipe_height = [200, 250, 300, 350, 400]
        self.birdflap = pygame.USEREVENT + 1
        pygame.time.set_timer(self.birdflap, 100)
        self.score = 0
        self.high_score = 0
        self.game_active = False

    def test_bird_movement(self, expected_y=None):
        self.bird_movement = 5
        self.bird_rect.centery += self.bird_movement
        self.assertEqual(self.bird_rect.centery, expected_y)

    def test_create_pipe(self, game=None):
        bottom_pipe, top_pipe = game.create_pipe()
        self.assertEqual(bottom_pipe.centery, self.pipe_height[1])
        self.assertEqual(top_pipe.centery, self.pipe_height[1] - 820)

    def test_move_pipe(self):
        pipes = [self.pipe_surface.get_rect(midtop=(500, self.pipe_height[1]))]
        pipes = move_pipe(pipes)
        self.assertEqual(pipes[0].centerx, 495)

    def test_check_collision(self):
        pipes = [self.pipe_surface.get_rect(midtop=(100, 200))]
        self.bird_rect.centery = 150
        self.assertFalse(check_collision(pipes))
        self.bird_rect.centery = 250
        self.assertTrue(check_collision(pipes))

    def test_rotate_bird(self):
        rotated_bird = rotate_bird(self.bird)
        self.assertIsNotNone(rotated_bird)

    def test_bird_animation(self):
        new_bird, new_bird_rect = bird_animation()
        self.assertEqual(new_bird_rect.centery, 384)

    def test_get_score(self):
        pipes = [self.pipe_surface.get_rect(midtop=(100, 200))]
        self.bird_rect.centery = 150
        self.assertEqual(get_score(), 0)
        self.bird_rect.centery = 250
        self.assertEqual(get_score(), 1)

    def tearDown(self):
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
