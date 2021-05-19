import pygame
import os
import random
import csv

# Initialise pygame
pygame.init()

# Constantes pour definir taille de la fenetre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# Variables pour creer la fenetre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Winter in Caves')

# Images par secondes
clock = pygame.time.Clock()
FPS = 60

# Variable de jeu
GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = len(os.listdir('img/tile'))
level = 1

# Variable d'action du personnages
moving_left = False
moving_right = False
shoot = False
projectile = False
projectile_thrown = False

# Charge les sprites
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

rock_img = pygame.image.load('img/items/0.png').convert_alpha()
rock_img = pygame.transform.scale(rock_img, (int(rock_img.get_width() * 1.5), int(rock_img.get_height() * 1.5)))

projectile_img = pygame.image.load('img/items/1.png').convert_alpha()
projectile_img = pygame.transform.scale(projectile_img, (int(projectile_img.get_width() * 1.5), int(projectile_img.get_height() * 1.5)))

# Groupe les sprites ensembles
rock_groupe = pygame.sprite.Group()
projectile_groupe = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()


# Couleurs
BACKGROUND = (65, 161, 209)  # Code RGB
RED = (255, 0, 0)  # Pour simuler un sol
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)