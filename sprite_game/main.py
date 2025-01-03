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
            image.set_colorkey(BLACK) #looks for that color and makes transparent
            explosion_list.append(image)

    tile_sheet = SpriteSheet("sprite_game/sprites/tilemap.png")
    bow_image = tile_sheet.get_image(16*10+11, 16*11+10, 16, 16)
    bow_image.set_colorkey(BLACK) #looks for that color and makes transparent
    
    while playing == True:
        screen.fill(BACK)
        
        screen.blit(explosion_list[0], (100,100))
        screen.blit(bow_image, (200,200))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
                pg.quit()

        pg.display.flip()
        
        clock.tick(FPS)


game()