import pygame as pg

WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BUE = [0,0,255]
YEOW = [238, 210, 0]
ORANGE = [255, 69, 0]
GREY = [120,120,120]
NEW_CHARS = [160, 160, 160]
TIES = [63, 38, 49]
DARK_GREEN = [30,57,22]

FPS = 60

TILE = 64

WIDTH = 15*TILE
HEIGHT = 10*TILE

# O_MAP_WIDTH = len(OVERWORLD[0]) * TILE
# O_MAP_HEIGHT = len(OVERWORLD) * TILE

# H_MAP_WIDTH = len(HOUSE[0]) * TILE
# H_MAP_HEIGHT = len(HOUSE) * TILE

ENEMY_NUMBER = 5
ENEMY_RESPAWN = False
SNAKE_DMG = .5

PLAYER_INV_MAX = 3
PLAYER_HEARTS = 5

JOY_MINIMUM = 0.004

TEXTS = {"start": "Press Enter/A to start", "inv_full": "You can't hold any more _!"}