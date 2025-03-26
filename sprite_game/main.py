import pygame as pg
import random as rand
from maps import Tiled_Map
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
                king_r = chars_sheet.get_image(786+(TILE*i),10*18-1, 30,46,1.1,1.1)
                king_r.set_colorkey(NEW_CHARS)
                self.king_right.append(king_r)
                king_l = pg.transform.flip(king_r, True, False)
                self.king_left.append(king_l)
            else:
                king_up = chars_sheet.get_image(784+TILE+(TILE*i),10*18-1, 30,46,1.1,1.1)
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

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""
        # self.map = map

        self.block_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()

        self.map_tiles = pg.sprite.Group()
            
        self.tile_map = pytmx.load_pygame("sprite_game/tiles/test.tmx")
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = x*TILE,y*TILE
                    surf = pg.transform.scale(surf, (TILE,TILE))
                    Tiled_Map(pos, surf, [self.map_tiles, self.all_sprites]) #key helper!!!!!
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if layer.name == "sprites":
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        it = Item((obj.x/16)*64, (obj.y/16)*64, self.screen, im, obj.name)
                        self.item_sprites.add(it)
                        self.all_sprites.add(it)

                    elif layer.name == "collide" and obj.name != "tree":
                        w = Wall((obj.x/16)*64, (obj.y/16)*64, self.screen, (obj.height/16)*64, (obj.width/16)*64)
                        self.block_sprites.add(w)

                    elif "sign" in obj.name:
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        w = Wall((obj.x/16)*64, (obj.y/16)*64, self.screen, (obj.height/16)*64, (obj.width/16)*64, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    elif layer.name == "interact":
                        im = pg.transform.scale(obj.image, (TILE,TILE))
                        w = Wall((obj.x/16)*64, (obj.y/16)*64, self.screen, (obj.height/16)*64, (obj.width/16)*64, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    elif obj.name == "snake":
                        s = Snake((obj.x/16)*64, (obj.y/16)*64, self.screen, self.snake_images_r, self.snake_images_l, self)
                        self.snake_sprites.add(s)
                        self.all_sprites.add(s)

                    elif obj.name == "player":
                        self.player = Player((obj.x/16)*64, (obj.y/16)*64,self.screen, self.king_right, self.king_left, self.king_up, self)
                        self.all_sprites.add(self.player)

        self.game_viewer = Camera(self.tile_map.width*TILE, self.tile_map.height*TILE)

        self.run()

    def update(self):
        """Run all updates."""
        self.all_sprites.update()
        self.block_sprites.update()
        self.game_viewer.update(self.player)

    def draw(self):
        """Fill screen, draw objects, flip."""

        self.map_tiles.draw(self.screen)
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

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_i:
                    print(self.player.inv)

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
    # game.game_over()

pg.quit()