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
    bow_image = tile_sheet.get_image(11*16-7, 9*16+9, 16, 16, 2, 2)
    bow_image.set_colorkey(BLACK) #looks for that color and makes transparent

    grass_image = tile_sheet.get_image(17*2, 0. 16,16,4,4)

    grass_sq = []
    for y in range(1,4):
        for x in range(0,3):
            locx = 17 * x
            locy = 17 * y
            image = tile_sheet.get_image(locx, locy, 16, 16, 4, 4)
            image.set_colorkey(BLACK)
            grass_sq.append(image)

    zombie_sheet = SpriteSheet("sprite_game/sprites/spritesheet_characters.png")
    green_player_image = zombie_sheet.get_image(0,0,57,44)
    green_player_image.set_colorkey(BLACK)
    zombie_walk_image = zombie_sheet.get_image(425,0,37,44)
    zombie_walk_image.set_colorkey(BLACK)

    chars_sheet = SpriteSheet("sprite_game/sprites/new_chars.png")
    king_still = chars_sheet.get_image(17,10*18-1, 32,46)
    king_still.set_colorkey(NEW_CHARS)

    
    while playing == True:
        screen.fill(BACK)

        for row in range(len(MAP)):
            y_loc = row * (16*4)
            for column in range(len(MAP[0])):
                x_loc = column * (16*4)
                if MAP[row][column] == "0":
                    screen.blit(grass_sq[0], (x_loc, y_loc))
                elif MAP[row][column] == "1":
                    screen.blit(grass_sq[1], (x_loc, y_loc))
                elif MAP[row][column] == "2":
                    screen.blit(grass_sq[2], (x_loc, y_loc))
                elif MAP[row][column] == "3":
                    screen.blit(grass_sq[3], (x_loc, y_loc))
                elif MAP[row][column] == "4":
                    screen.blit(grass_sq[4], (x_loc, y_loc))
                elif MAP[row][column] == "5":
                    screen.blit(grass_sq[5], (x_loc, y_loc))
                elif MAP[row][column] == "6":
                    screen.blit(grass_sq[6], (x_loc, y_loc))
                elif MAP[row][column] == "7":
                    screen.blit(grass_sq[7], (x_loc, y_loc))
                elif MAP[row][column] == "8":
                    screen.blit(grass_sq[8], (x_loc, y_loc))
                elif MAP[row][column] == "g":
                    screen.blit(grass_sq[5], (x_loc, y_loc))
        
        screen.blit(explosion_list[0], (100,100))
        screen.blit(bow_image, (100,200))
        screen.blit(green_player_image, (100,300))
        screen.blit(zombie_walk_image, (100,400))
        screen.blit(king_still, (100,500))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                playing = False
                pg.quit()

        pg.display.flip()
        
        clock.tick(FPS)


game()