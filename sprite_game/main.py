import pygame as pg
from settings import *
from components import *

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.running = True
        self.load_images()

    def load_images(self):
        """Load and get images."""

        explosion_sheet = SpriteSheet("sprite_game/sprites/explosion.png")
        self.explosion_list = []
        for y in range(5):
            for x in range(5):
                locx = 64 * x
                locy = 64 * y
                image = explosion_sheet.get_image(locx, locy, 64, 64)
                image.set_colorkey(BLACK) #looks for that color and makes transparent
                self.explosion_list.append(image)

        tile_sheet = SpriteSheet("sprite_game/sprites/tilemap.png")
        self.bow_image = tile_sheet.get_image(11*16-7, 9*16+9, 16, 16, 2, 2)
        self.bow_image.set_colorkey(BLACK) #looks for that color and makes transparent

        self.grass_image = tile_sheet.get_image(17*2, 0, 16,16,4,4)

        self.grass_sq = []
        for y in range(1,4):
            for x in range(0,3):
                locx = 17 * x
                locy = 17 * y
                image = tile_sheet.get_image(locx, locy, 16, 16, 4, 4)
                image.set_colorkey(BLACK)
                self.grass_sq.append(image)

        zombie_sheet = SpriteSheet("sprite_game/sprites/spritesheet_characters.png")
        self.green_player_image = zombie_sheet.get_image(0,0,57,44)
        self.green_player_image.set_colorkey(BLACK)
        self.zombie_walk_image = zombie_sheet.get_image(425,0,37,44)
        self.zombie_walk_image.set_colorkey(BLACK)

        chars_sheet = SpriteSheet("sprite_game/sprites/new_chars.png")
        self.king_still = chars_sheet.get_image(17,10*18-1, 32,46)
        self.king_still.set_colorkey(NEW_CHARS)

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""

        self.run()

    def update(self):
        """Run all updates."""
        pass

    def draw(self):
        """Fill screen, draw objects, flip."""
        self.screen.fill(BLACK)

        for row in range(len(MAP)):
            y_loc = row * (16*4)
            for column in range(len(MAP[0])):
                x_loc = column * (16*4)
                if MAP[row][column] == "0":
                    self.screen.blit(self.grass_sq[0], (x_loc, y_loc))
                elif MAP[row][column] == "1":
                    self.screen.blit(self.grass_sq[1], (x_loc, y_loc))
                elif MAP[row][column] == "2":
                    self.screen.blit(self.grass_sq[2], (x_loc, y_loc))
                elif MAP[row][column] == "3":
                    self.screen.blit(self.grass_sq[3], (x_loc, y_loc))
                elif MAP[row][column] == "4":
                    self.screen.blit(self.grass_sq[4], (x_loc, y_loc))
                elif MAP[row][column] == "5":
                    self.screen.blit(self.grass_sq[5], (x_loc, y_loc))
                elif MAP[row][column] == "6":
                    self.screen.blit(self.grass_sq[6], (x_loc, y_loc))
                elif MAP[row][column] == "7":
                    self.screen.blit(self.grass_sq[7], (x_loc, y_loc))
                elif MAP[row][column] == "8":
                    self.screen.blit(self.grass_sq[8], (x_loc, y_loc))
                elif MAP[row][column] == "g":
                    self.screen.blit(self.grass_image, (x_loc, y_loc))
        
        self.screen.blit(self.explosion_list[0], (100,100))
        self.screen.blit(self.bow_image, (100,200))
        self.screen.blit(self.green_player_image, (100,300))
        self.screen.blit(self.zombie_walk_image, (100,400))
        self.screen.blit(self.king_still, (100,500))

        pg.display.flip()

    def events(self):
        """Game loop events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False

    def run(self):
        """Contains main game loop."""
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def show_start_screen(self):
        """Screen to start game."""
        pass

    def game_over(self):
        """Screen to end game."""
        pass

############################## PLAY ###################################

game = Game()
game.show_start_screen()

while game.running:
    game.new()
    game.game_over()

pg.quit()