#constants
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [238, 210, 0]
ORANGE = [255, 69, 0]
GREY = [120,120,120]

FPS = 60

LAYOUT = ["1111111111111111111111111111111111111111",
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
          "1            e             d           1",
          "1         111111         11111         1",
          "1                                      1",
          "1   p                                 e1",
          "1111111111111111111111111111111111111111"]

BRICK_WIDTH = 40
BRICK_HEIGHT = 40

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40

DOOR_HEIGHT = 60

WIDTH = BRICK_WIDTH * len(LAYOUT[0])
HEIGHT = BRICK_HEIGHT * len(LAYOUT)

GRAVITY = 1