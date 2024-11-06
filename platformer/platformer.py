import pygame as pg
from settings import *
from components import *

screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

brick_list = []
for row in range(len(LAYOUT)):
     y_loc = row * BRICK_HEIGHT
     for column in range(len(LAYOUT[0])):
        x_loc = column * BRICK_WIDTH
        if LAYOUT[row][column] == "1":
            brick = Brick(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,RED,screen)  
            brick_list.append(brick)  
        elif LAYOUT[row][column] == "p":
            me = Player(x_loc,y_loc,PLAYER_WIDTH,PLAYER_HEIGHT,YELLOW,screen) 
        elif LAYOUT[row][column] == "e":
            mon = Enemy(x_loc+BRICK_WIDTH,y_loc,ENEMY_WIDTH,ENEMY_HEIGHT,GREEN,screen, 5) 

playing = True

while playing == True:
    screen.fill(BLACK)
    me.draw()
    me.move()
    me.keys()

    me.draw()

    mon.draw()
    mon.move()
    if mon.x <= BRICK_WIDTH-5:
         mon.x = WIDTH+BRICK_WIDTH

    for b in brick_list:
         b.draw()
    
    pg.display.flip()
    clock.tick(FPS)

    for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False