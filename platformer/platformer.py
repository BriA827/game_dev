import pygame as pg
from settings import *
from components import *

def game(level):
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    dirt_image = pg.image.load("platformer/images/ground_dirt.png")
    grass_image = pg.image.load("platformer/images/ground.png")
    player_image = pg.image.load("platformer/images/side.png")
    enemy_image = pg.image.load("platformer/images/slime_normal.png")

    brick_list = []
    elevator_list = []
    door_list = []
    enemies = []
    blocked_list = []
    height_list = []

    playing = True

    for row in range(len(level)):
        y_loc = row * BRICK_HEIGHT
        for column in range(len(level[0])):
            x_loc = column * BRICK_WIDTH
            if level[row][column] == "1":
                brick = Brick(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,RED,screen, image=dirt_image)  
                brick_list.append(brick)  

            elif level[row][column] == "2":
                ele = Elevator(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,RED,screen, move=True)  
                elevator_list.append(ele)
                brick_list.append(ele)  

            elif level[row][column] == "l":
                hei = Elevator(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,YELLOW,screen) 
                height_list.append(hei) 

            elif level[row][column] == "p":
                me = Player(x_loc,y_loc,PLAYER_WIDTH,PLAYER_HEIGHT,YELLOW,screen, player_image) 
            
            elif level[row][column] == "m":
                mon = Enemy(x_loc+BRICK_WIDTH,y_loc,ENEMY_WIDTH,ENEMY_HEIGHT,GREEN,screen, 3, True, enemy_image)
                enemies.append(mon)
            
            elif level[row][column] == "e":
                ene = Enemy(x_loc+BRICK_WIDTH,y_loc,ENEMY_WIDTH,ENEMY_HEIGHT,GREEN,screen, 5, False, enemy_image)
                enemies.append(ene)
            
            elif level[row][column] == "b":
                blocked = Brick(x_loc,y_loc,BRICK_WIDTH,BRICK_HEIGHT,BACK,screen, image=None)
                blocked_list.append(blocked)
            
            elif level[row][column] == "d":
                end = Door(x_loc, y_loc-20, BRICK_WIDTH, DOOR_HEIGHT, GREY, screen)
                door_list.append(end)

            elif level[row][column] == "c":
                end = Crate(x_loc, y_loc-20, BRICK_WIDTH, DOOR_HEIGHT, screen)
                door_list.append(end)
    
    while playing == True:
        screen.fill(BACK)

        for e in elevator_list:
            e.draw()
            e.lift(height_list)

        for d in door_list:
            d.draw()

        for b in brick_list:
            b.draw()

        for e in enemies:
            e.draw()
            e.moving(blocked_list)

        me.update(brick_list, door_list, enemies)
        me.draw()
        me.end()

        if me.status == False:
            playing = False
            return "death"


        if me.win == True:
            playing = False
            return "next"

        pg.display.flip()
        clock.tick(FPS)

        for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                    return "done"

def gameend():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    die_text = 'You Died!'
    die_img = FONT.render(die_text, True, WHITE)

    playing = True 
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return playing
                elif event.key == pg.K_x:
                    return False
                
        screen.fill(BLACK)

        screen.blit(die_img, (WIDTH//2-60, HEIGHT//2 - 20))

        pg.display.flip()

        clock.tick(FPS)

def win(level):
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    win_text= 'You Won! Level: ' + str(level)
    win_img = FONT.render(win_text, True, WHITE)

    playing = True 
    while playing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return playing
                elif event.key == pg.K_x:
                    return False
                
        screen.fill(BLACK)

        screen.blit(win_img, (WIDTH//2-90, HEIGHT//2 - 20))

        pg.display.flip()

        clock.tick(FPS)

###########################################################

lev = 1

play = True

while play == True:
    end = game(LAYOUTS[lev-1])

    if end == "death":
        play = gameend()

    elif end == "next":
        if lev >= len(LAYOUTS):
            play = win(lev)
            lev = 1
        else:
            lev+=1

    elif end == "done":
        play = False

pg.quit()