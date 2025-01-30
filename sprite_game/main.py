import pygame as pg
import random as rand
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

        tile_sheet = SpriteSheet("sprite_game/sprites/tilemap.png")
        self.bomb_image = tile_sheet.get_image(10*16-7, 8*16+9, 16, 16, 2, 2, True)

        self.flower_image = tile_sheet.get_image(17*2, 0, 16,16,4,4)
        self.grass_image = tile_sheet.get_image(17, 0, 16,16,4,4)
        self.green_image = tile_sheet.get_image(0, 0, 16,16,4,4)

        self.stone_image = tile_sheet.get_image(17*6, 17*10, 16,16,4,4)

        self.tree_images = []
        for y in range(3):
            for x in range(6,9):
                locx = 17 * x
                locy = 17 * y
                image = tile_sheet.get_image(locx, locy, 16, 16, 4, 4)
                image.set_colorkey(BLACK)
                self.tree_images.append(image)

        self.grass_sq = []
        for y in range(1,4):
            for x in range(0,3):
                locx = 17 * x
                locy = 17 * y
                image = tile_sheet.get_image(locx, locy, 16, 16, 4, 4)
                self.grass_sq.append(image)

        # zombie_sheet = SpriteSheet("sprite_game/sprites/spritesheet_characters.png")
        # self.green_player_image = zombie_sheet.get_image(0,0,57,44,True)
        # self.zombie_walk_image = zombie_sheet.get_image(425,0,37,44,True)

        chars_sheet = SpriteSheet("sprite_game/sprites/new_chars.png")
        self.king_still = chars_sheet.get_image(17,10*18-1, 32,46,True)

        self.king_right = []
        self.king_left = []
        self.king_up = []

        self.snake_images_r = []
        self.snake_images_l = []

        for i in range(10):
            if i <= 5:
                king_r = chars_sheet.get_image(784+(64*i),10*18-1, 32,46)
                king_r.set_colorkey(NEW_CHARS)
                self.king_right.append(king_r)
                king_l = pg.transform.flip(king_r, True, False)
                self.king_left.append(king_l)
            else:
                king_up = chars_sheet.get_image(784+64+(64*i),10*18-1, 32,46)
                king_up.set_colorkey(NEW_CHARS)
                self.king_up.append(king_up)

        for i in range(4):
            snake = chars_sheet.get_image(17+64*i, 17*18-1, 32,46)
            snake.set_colorkey(NEW_CHARS)
            self.snake_images_r.append(snake)
            snake = pg.transform.flip(snake, True, False)
            self.snake_images_l.append(snake)

        exp_sheet = SpriteSheet("sprite_game/sprites/explosion.png")
        self.exp_list = []

        for y in range(5):
            for x in range(5):
                locx = 64 * x
                locy = 64 * y
                image = exp_sheet.get_image(locx, locy, 64, 64, 1, 1, BLACK)
                self.exp_list.append(image)

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""
        
        self.wall_sprites = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()
        self.block_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()

        for row in range(len(MAP)):
            y_loc = row * (16*4)
            for column in range(len(MAP[0])):
                x_loc = column * (16*4)
                if MAP[row][column] == "-":
                    w = Wall(x_loc, y_loc, self.screen, self.stone_image)
                    self.wall_sprites.add(w)
                    self.block_sprites.add(w)
                    self.all_sprites.add(w)
                elif MAP[row][column] == "s":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[6])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif MAP[row][column] == "o":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[1])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif MAP[row][column] == "f":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[5])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif MAP[row][column] == "~":
                    s = Snake(x_loc, y_loc, self.screen, self.snake_images_r, self.snake_images_l, self, -1)
                    self.snake_sprites.add(s)
                    self.all_sprites.add(s)
                elif MAP[row][column] == "b":
                    b = Bomb(x_loc, y_loc, self.screen, self.bomb_image)
                    self.item_sprites.add(b)
                    self.all_sprites.add(b)

        self.player = Player(4*64, 64 ,self.screen, self.king_right, self.king_left, self.king_up, self)
        self.all_sprites.add(self.player)

        self.run()

    def update(self):
        """Run all updates."""

        if len(self.snake_sprites) == 0:
            s = Snake(rand.randint(70, 930), rand.randint(70, 530), self.screen, self.snake_images_r, self.snake_images_l, self, rand.choice([-1,1]))
            for i in self.wall_sprites:
                if s.rect.x == i.rect.x and s.rect.y == i.rect.y:
                    s.kill()
            self.snake_sprites.add(s)
            self.all_sprites.add(s)

        if "Bomb" in self.player.inv and self.player.use == True and self.player.hits:
            if self.player.hits[0] in self.wall_sprites:
                self.player.hits[0].kill()
                self.player.inv.remove("Bomb")
                cx, cy = self.player.hits[0].rect.center
                e = Explosion(cx-20, cy, self.screen, self.exp_list)
                self.all_sprites.add(e)
        
        self.all_sprites.update()

    def draw(self):
        """Fill screen, draw objects, flip."""
        self.screen.fill(BACK)

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
                    self.screen.blit(self.flower_image, (x_loc, y_loc))
                else:
                    self.screen.blit(self.grass_image, (x_loc, y_loc))

        self.all_sprites.draw(self.screen)

        pg.display.flip()

    def events(self):
        """Game loop events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False
 
            if event.type == pg.KEYDOWN and event.key == pg.K_e:
                self.player.use = True

            elif event.type == pg.KEYUP and event.key == pg.K_e:
                self.player.use = False

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