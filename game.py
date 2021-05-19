import pygame
import os
import random
import csv


pygame.init()


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Winter in Caves')

clock = pygame.time.Clock()
FPS = 500

GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = len(os.listdir('img/tile'))
MAX_LEVELS = 3
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

moving_left = False
moving_right = False
shoot = False
ball = False
ball_thrown = False

sky = pygame.image.load('img/background/sky.png').convert_alpha()
rocks = pygame.image.load('img/background/rocks.png').convert_alpha()
ground_1 = pygame.image.load('img/background/ground_1.png').convert_alpha()
ground_2 = pygame.image.load('img/background/ground_2.png').convert_alpha()
ground_3 = pygame.image.load('img/background/ground_3.png').convert_alpha()
clouds_1 = pygame.image.load('img/background/clouds_1.png').convert_alpha()
clouds_2 = pygame.image.load('img/background/clouds_2.png').convert_alpha()

sky = pygame.transform.scale(sky, (SCREEN_WIDTH, SCREEN_HEIGHT))
rocks = pygame.transform.scale(rocks, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_1 = pygame.transform.scale(ground_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_2 = pygame.transform.scale(ground_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_3 = pygame.transform.scale(ground_3, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds_1 = pygame.transform.scale(clouds_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds_2 = pygame.transform.scale(clouds_2, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

rock_img = pygame.image.load('img/items/0.png').convert_alpha()
rock_img = pygame.transform.scale(rock_img, (int(
    rock_img.get_width() * 1.5), int(rock_img.get_height() * 1.5)))

ball_img = pygame.image.load('img/items/1.png').convert_alpha()
ball_img = pygame.transform.scale(ball_img, (int(
    ball_img.get_width() * 1.5), int(ball_img.get_height() * 1.5)))


BACKGROUND = (65, 161, 209)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


font = pygame.font.SysFont('Futura', 30)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_background():
    screen.fill(BACKGROUND)
    width = sky.get_width()
    for x in range(8):
        screen.blit(sky, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(rocks, ((x * width) - bg_scroll * 0.55, 0))
        screen.blit(clouds_1, ((x * width) - bg_scroll * 0.60, 0))
        screen.blit(clouds_2, ((x * width) - bg_scroll * 0.65, 0))
        screen.blit(ground_1, ((x * width) - bg_scroll * 0.70, 0))
        screen.blit(ground_2, ((x * width) - bg_scroll * 0.75, 0))
        screen.blit(ground_3, ((x * width) - bg_scroll * 0.8, 0))


def reset_level():
	enemy_group.empty()
	rock_group.empty()
	ball_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data


rock_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
