import pygame as pg

#constants
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [238, 210, 0]
ORANGE = [255, 69, 0]
GREY = [120,120,120]

BACK = BLACK

FPS = 60

BLANK = ["1111111111111111111111111111111111111111",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1111111111111111111111111111111111111111"]

LAYOUT_1=["1111111111111111111111111111111111111111",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1  p                              d   e1",
          "1111111111111111111111111111111111111111"]

LAYOUT_2 = ["1111111111111111111111111111111111111111",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                           d          1",
          "1                          111         1",
          "1               b  m   b               1",
          "1                111111                1",
          "1        b  m  b                       1",
          "1         11111                        1",
          "1                                      1",
          "1  p                                  e1",
          "1111111111111111111111111111111111111111"]

LAYOUT_3 = ["1111111111111111111111111111111111111111",
          "1                                      1",
          "1  p                                   1",
          "111111                                 1",
          "1                                      1",
          "1      222                             1",
          "1                                      1",
          "1                                      1",
          "1           222                        1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1",
          "1                                      1"]


LAYOUTS = [LAYOUT_1, LAYOUT_2, LAYOUT_3]

BRICK_WIDTH = 40
BRICK_HEIGHT = 40

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40

DOOR_HEIGHT = 60

WIDTH = BRICK_WIDTH * len(LAYOUT_1[0])
HEIGHT = BRICK_HEIGHT * len(LAYOUT_1)

GRAVITY = 1

pg.font.init()
FONT = pg.font.SysFont('comicsans', 40)