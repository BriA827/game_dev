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

BACK = [30,57,22]

FPS = 60

MAP = ["----------------------------",
       "- 01112                    -",
       "- 34445   g                -",
       "- 64448                    -",
       "- g345    b            g   -",
       "-  345      g              -",
       "-  345    o                -",
       "-  678    sf          01111-",
       "-     g              044444-",
       "-                   0444444-",
       "-                  04444444-",
       "-   s          g   34444444-",
       "-                  34444444-",
       "----------------------------"]

#ints = dirt_path, g = flowers, - = wall, o/s/f = tree, ~ = snake, blank = grass, b = bomb

TILE = 64

WIDTH = 1000
HEIGHT = 600

MAP_WIDTH = len(MAP[0]) * 64
MAP_HEIGHT = len(MAP) * 64