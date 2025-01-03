import pygame as pg
from settings import *
from components import *

def game():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    playing = True
    
    while playing == True:
        screen.fill(BACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
                pg.quit()

        # pg.display.flip()
        
        clock.tick(FPS)

# play = True
play = False

while play:
   game()

pg.quit()