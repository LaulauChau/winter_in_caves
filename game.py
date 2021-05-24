import pygame
import os
import random
import csv


pygame.init()

# Definition de la fenetre de jeu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Winter in Caves')

# Definition du nombre d'images par seconde
clock = pygame.time.Clock()
FPS = 60

# Definition des constantes/variables de jeu
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLUMNS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = len(os.listdir('img/tile'))
MAX_LEVELS = len(os.listdir('levels'))
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
start_intro = False

# Definition des actions du personnage
moving_left = False
moving_right = False
shoot = False
ball = False
ball_thrown = False

# Importation des images
grotte = pygame.image.load('img/background/0.png').convert_alpha()

start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()

img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

rock_img = pygame.image.load('img/items/0.png').convert_alpha()
ball_img = pygame.image.load('img/items/1.png').convert_alpha()

# Redimensionne les images

grotte = pygame.transform.scale(grotte, (SCREEN_WIDTH, SCREEN_HEIGHT))

rock_img = pygame.transform.scale(rock_img, (int(
    rock_img.get_width() * 1.5), int(rock_img.get_height() * 1.5)))

ball_img = pygame.transform.scale(ball_img, (int(
    ball_img.get_width() * 1.5), int(ball_img.get_height() * 1.5)))

# Definition des couleurs avec leurs code RGB
BACKGROUND = (65, 161, 209)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Definition de la police d'ecriture
font = pygame.font.SysFont('Futura', 30)


# Fonction permettant d'ecrire du texte a l'ecran
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Fonction permettant d'ajouter les images d'arriere-plan a l'ecran
def draw_background():
    screen.fill(BACKGROUND)
    width = grotte.get_width()
    for x in range(8):
        screen.blit(grotte, ((x * width) - bg_scroll, 0))


# Fonction permettant de remettre a zero les groupes d'images et donnees du monde
def reset_level():
    enemy_group.empty()
    rock_group.empty()
    ball_group.empty()
    water_group.empty()
    exit_group.empty()

    data = []
    for row in range(ROWS):
        r = [-1] * COLUMNS
        data.append(r)

    return data


# Groupe les images ensemble par type
rock_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
