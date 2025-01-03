import pygame as pg
from settings import *
from components import *

def game():
    pg.init()
    screen = pg.display.set_mode([WIDTH, HEIGHT])
    clock = pg.time.Clock()

    playing = True

    explosion_sheet = SpriteSheet("sprite_game/sprites/explosion.png")
    explosion_list = []
    for y in range(5):
        for x in range(5):
            locx = 64 * x
            locy = 64 * y
            image = explosion_sheet.get_image(locx, locy, 64, 64)
            explosion_list.append(image)
    
    while playing == True:
        screen.fill(BACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
                pg.quit()

        # pg.display.flip()
        
        clock.tick(FPS)

play = True
# play = False

while play:
   game()

pg.quit()