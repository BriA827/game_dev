import pygame as pg
from settings import *
from components import *

screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

me = Player(20,800,50,70,YELLOW,screen)
brick = Player(600,800,50,70,RED,screen)

playing = True

while playing == True:
    screen.fill(BLACK)
    me.draw()
    me.move()
    me.keys()

    brick.draw()

    
    pg.display.flip()
    clock.tick(FPS)

    for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False