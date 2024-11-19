import pygame as pg
from settings import *
from components import *

screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

brick_list = []
door_list = []
enemies = []
blocked_list = []

for row in range(len(LAYOUT)):
     y_loc = row * BRICK_HEIGHT
     for column in range(len(LAYOUT[0])):
        x_loc = column * BRICK_WIDTH
        if LAYOUT[row][column] == "1":
            brick = Brick(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,RED,screen)  
            brick_list.append(brick)  
        elif LAYOUT[row][column] == "p":
            me = Player(x_loc,y_loc,PLAYER_WIDTH,PLAYER_HEIGHT,YELLOW,screen) 
        elif LAYOUT[row][column] == "m":
            mon = Enemy(x_loc+BRICK_WIDTH,y_loc,ENEMY_WIDTH,ENEMY_HEIGHT,GREEN,screen, 3, True)
            enemies.append(mon)
        elif LAYOUT[row][column] == "e":
            ene = Enemy(x_loc+BRICK_WIDTH,y_loc,ENEMY_WIDTH,ENEMY_HEIGHT,GREEN,screen, 5, False)
            enemies.append(ene)
        elif LAYOUT[row][column] == "b":
            blocked = Brick(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,BACK,screen)
            blocked_list.append(blocked)
        elif LAYOUT[row][column] == "d":
            end = Door(x_loc, y_loc-20, BRICK_WIDTH, DOOR_HEIGHT, GREY, screen)
            door_list.append(end)

playing = True
end = False

def gamestart():
    while playing == True:
        screen.fill(BACK)

        for b in blocked_list:
            b.draw()

        for e in enemies:
            e.draw()
            e.moving(blocked_list)

        for d in door_list:
            d.draw()

        for b in brick_list:
            b.draw()

        me.update(brick_list, door_list, enemies)
        me.draw()
        me.end()

        if me.status == False:
            playing = False

        if me.win == True:
            screen.blit(WIN_IMG, (WIDTH//2-60, HEIGHT//2 - 40))
        
        pg.display.flip()
        clock.tick(FPS)

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False

def gameend():
    while playing == True:
        screen.fill(BACK)
        screen.blit(DIE_IMG, (WIDTH//2-60, HEIGHT//2 - 40))
        
        pg.display.flip()
        clock.tick(FPS)

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        playing = False


gamestart()
while playing == True:
    playing = gameend()
pg.quit()