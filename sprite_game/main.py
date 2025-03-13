import pygame as pg
import random as rand
from settings import *
from components import *
import pytmx

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

        self.house_images = []
        for y in range(4,8):
            for x in range(4):
                locx = 17 * x
                locy = 17 * y
                image = tile_sheet.get_image(locx, locy, 16, 16, 4, 4)
                self.house_images.append(image)

        self.floor_images = []
        for i in range(4):
            wood = SpriteSheet(f"sprite_game/sprites/spr_wood_texture_{i}.png")
            img = wood.get_image(0,0, 16,16, 4,4)
            self.floor_images.append(img)

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
                king_r = chars_sheet.get_image(786+(TILE*i),10*18-1, 30,46)
                king_r.set_colorkey(NEW_CHARS)
                self.king_right.append(king_r)
                king_l = pg.transform.flip(king_r, True, False)
                self.king_left.append(king_l)
            else:
                king_up = chars_sheet.get_image(784+TILE+(TILE*i),10*18-1, 30,46)
                king_up.set_colorkey(NEW_CHARS)
                self.king_up.append(king_up)

        for i in range(4):
            snake = chars_sheet.get_image(17+TILE*i, 17*18-1, 32,46)
            snake.set_colorkey(NEW_CHARS)
            self.snake_images_r.append(snake)
            snake = pg.transform.flip(snake, True, False)
            self.snake_images_l.append(snake)

        exp_sheet = SpriteSheet("sprite_game/sprites/explosion.png")
        self.exp_list = []

        for y in range(5):
            for x in range(5):
                locx = TILE * x
                locy = TILE * y
                image = exp_sheet.get_image(locx, locy, TILE, TILE, 1, 1, BLACK)
                self.exp_list.append(image)

        cursor_sheet = SpriteSheet("sprite_game/sprites/cursor.png")
        self.cursor_image = cursor_sheet.get_image(11,1,16,16)
        self.cursor_image.set_colorkey(WHITE)
        self.track_image = cursor_sheet.get_image(72,1,4,4,2.5,2.5)
        self.track_image.set_colorkey(WHITE)
        self.track_image = pg.transform.rotate(self.track_image, 45)

    def new(self, map, start):
        """Create all game objects, sprites, and groups. Call run() method"""
        self.map = map
        
        self.wall_sprites = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()
        self.block_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.door_sprites = pg.sprite.Group()

        self.tile_map = pytmx.load_pygame("/Users/242413/Desktop/game_dev/tiles/test.tmx")
        # print(dir(self.tile_map))
        for row in range(len(map)):
            y_loc = row * TILE
            for column in range(len(map[0])):
                x_loc = column * TILE
                if map == OVERWORLD:
                    b = Background(x_loc, y_loc, self.grass_image)
                    self.all_sprites.add(b)
                elif map == HOUSE:
                    b = Background(x_loc, y_loc, self.floor_images[1])
                    self.all_sprites.add(b)

                if map[row][column] == "0":
                    b = Background(x_loc, y_loc, self.grass_sq[0])
                    self.all_sprites.add(b)
                elif map[row][column] == "1":
                    b = Background(x_loc, y_loc, self.grass_sq[1])
                    self.all_sprites.add(b)
                elif map[row][column] == "2":
                    b = Background(x_loc, y_loc, self.grass_sq[2])
                    self.all_sprites.add(b)
                elif map[row][column] == "3":
                    b = Background(x_loc, y_loc, self.grass_sq[3])
                    self.all_sprites.add(b)
                elif map[row][column] == "4":
                    b = Background(x_loc, y_loc, self.grass_sq[4])
                    self.all_sprites.add(b)
                elif map[row][column] == "5":
                    b = Background(x_loc, y_loc, self.grass_sq[5])
                    self.all_sprites.add(b)
                elif map[row][column] == "6":
                    b = Background(x_loc, y_loc, self.grass_sq[6])
                    self.all_sprites.add(b)
                elif map[row][column] == "7":
                    b = Background(x_loc, y_loc, self.grass_sq[7])
                    self.all_sprites.add(b)
                elif map[row][column] == "8":
                    b = Background(x_loc, y_loc, self.grass_sq[8])
                    self.all_sprites.add(b)
                elif map[row][column] == "g":
                    b = Background(x_loc, y_loc, self.flower_image)
                    self.all_sprites.add(b)

                if map[row][column] == "-":
                    w = Wall(x_loc, y_loc, self.screen, self.stone_image)
                    self.wall_sprites.add(w)
                    self.block_sprites.add(w)
                    self.all_sprites.add(w)
                elif map[row][column] == "s":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[6])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif map[row][column] == "o":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[1])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif map[row][column] == "f":
                    t = Wall(x_loc, y_loc, self.screen, self.tree_images[5])
                    self.tree_sprites.add(t)
                    self.block_sprites.add(t)
                    self.all_sprites.add(t)
                elif map[row][column] == "b":
                    b = Bomb(x_loc, y_loc, self.screen, self.bomb_image)
                    self.item_sprites.add(b)
                    self.all_sprites.add(b)
                elif map[row][column] == "~":
                    s = Snake(x_loc, y_loc, self.screen, self.snake_images_r, self.snake_images_l, self)
                    self.snake_sprites.add(s)
                    self.all_sprites.add(s)
                elif map[row][column] == "l":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[0])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "m":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[1])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "c":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[3])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "r":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[2])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "L":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[4])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "M":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[5])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "R":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[6])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "[":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[8])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "_":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[9])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)
                elif map[row][column] == "D":
                    n = Door(x_loc, y_loc, self.screen, self.house_images[13], self)
                    self.wall_sprites.add(n)
                    self.door_sprites.add(n)
                    self.all_sprites.add(n)
                elif map[row][column] == "]":
                    n = Wall(x_loc, y_loc, self.screen, self.house_images[11])
                    self.wall_sprites.add(n)
                    self.all_sprites.add(n)
                    self.block_sprites.add(n)

        self.player = Player(start[0], start[1] ,self.screen, self.king_right, self.king_left, self.king_up, self)
        self.all_sprites.add(self.player)

        if self.map == OVERWORLD:
            self.tracker = Tracker(self.player, self.snake_sprites, self.cursor_image, self)
            self.all_sprites.add(self.tracker)
            self.tracked = Marker(self.track_image)
            self.all_sprites.add(self.tracked)

        if self.map == OVERWORLD:
            self.game_viewer = Camera(O_MAP_WIDTH, O_MAP_HEIGHT)
        elif self.map == HOUSE:
             self.game_viewer = Camera(H_MAP_WIDTH, H_MAP_HEIGHT)

        self.run()

    def update(self):
        """Run all updates."""

        if len(self.snake_sprites) < ENEMY_NUMBER and self.map == OVERWORLD:
            s = Snake(rand.randint(70, 930), rand.randint(70, 530), self.screen, self.snake_images_r, self.snake_images_l, self)
            self.snake_sprites.add(s)
            self.all_sprites.add(s)

        if "Bomb" in self.player.inv and self.player.use == True and self.player.hits:
            if self.player.hits[0] in self.wall_sprites:
                self.player.hits[0].kill()
                # self.player.inv.remove("Bomb")
                cx, cy = self.player.hits[0].rect.center
                e = Explosion(cx-20, cy, self.screen, self.exp_list)
                self.all_sprites.add(e)
        
        self.all_sprites.update()

        self.game_viewer.update(self.player)

        new_map = self.player.collide_door()
        if new_map:
            hits = pg.sprite.spritecollide(self.player, self.door_sprites, False)
            if new_map == OVERWORLD:
                new_start = None
                for i in range(len(new_map)):
                    if "D" in new_map[i]:
                       new_start = [new_map[i].index("D")*TILE, i*TILE + TILE]
            elif new_map == HOUSE:
                new_start = None
                for i in range(len(new_map)):
                    if "D" in new_map[i]:
                       new_start = [new_map[i].index("D")*TILE, i*TILE - TILE]
            game.new(new_map, new_start)

    def draw(self):
        """Fill screen, draw objects, flip."""
        if self.map == OVERWORLD:
            self.screen.fill(DARK_GREEN)
        elif self.map == HOUSE:
            self.screen.fill(BLACK)

        # self.all_sprites.draw(self.screen)
        for i in self.all_sprites:
            self.screen.blit(i.image, (self.game_viewer.get_view(i)))

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
    game.new(OVERWORLD, (4*TILE, 2*TILE))
    # game.game_over()

pg.quit()