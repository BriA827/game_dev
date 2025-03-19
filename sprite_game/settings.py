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

OVERWORLD = [
       "----------------------------",
       "- 01112                g   -",
       "- 34445   g       lmcr     -",
       "- 64448           LMMR     -",
       "- g345            [_D]     -",
       "-  345      g              -",
       "-  345    o          g     -",
       "-  678    sf          01111-",
       "-     g              044444-",
       "-                   0444444-",
       "-                  04444444-",
       "- g            g   34444444-",
       "-                  34444444-",
       "----------------------------"
]

HOUSE = ["[______________]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[              ]",
         "[_________D____]",
]

#ints = dirt_path, g = flowers, - = wall, o/s/f = tree, ~ = snake, blank = grass, b = bomb, h = house
#lmcr = leftroof, middleroof, chimney, rightroof --- LMR = leftwall, middlewall, rightwall --- [_D] = side, wall, door, side

TILE = 64

WIDTH = 1200
HEIGHT = 800

# O_MAP_WIDTH = len(OVERWORLD[0]) * TILE
# O_MAP_HEIGHT = len(OVERWORLD) * TILE

# H_MAP_WIDTH = len(HOUSE[0]) * TILE
# H_MAP_HEIGHT = len(HOUSE) * TILE

# ENEMY_NUMBER = 2