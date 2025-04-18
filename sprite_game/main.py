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
        pg.joystick.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        self.clock = pg.time.Clock()
        self.running = True
        self.load_images()

        # self.path = pg.font.match_font("sprite_game/Perfect DOS VGA 437.ttf", 0, 0)
        self.font = pg.font.SysFont("Perfect DOS VGA 437 Win", 30)
        self.joy = None

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
            img.set_alpha(150)
            self.floor_images.append(img)

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
        self.next_image = cursor_sheet.get_image(77,1,4,4,4.5,4.5)
        self.next_image.set_colorkey(WHITE)
        self.next_image = pg.transform.rotate(self.next_image, 45)

        self.track_image = cursor_sheet.get_image(72,1,4,4,2.5,2.5)
        self.track_image.set_colorkey(WHITE)
        self.track_image = pg.transform.rotate(self.track_image, 45)

        self.hearts = []
        for i in ["full", "half", "empty"]:
            heart = pg.image.load(f"platformer/images/hearts/heart_{i}.png")
            heart = pg.transform.scale(heart, (2*TILE/3, 2*TILE/3))
            self.hearts.append(heart)

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""
        # self.map = map
        self.text = False
        self.clear = True

        self.block_sprites = pg.sprite.Group()
        self.mask_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.tele_sprites = pg.sprite.Group()
        self.text_sprites = pg.sprite.Group()

        self.map_tiles = pg.sprite.Group()

        self.snake_spawns = []
            
        self.tile_map = pytmx.load_pygame("sprite_game/tiles/test.tmx")
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    pos = x*TILE,y*TILE
                    surf = pg.transform.scale(surf, (TILE,TILE))

                    # if layer.name == "trees_collide":
                    #     for obj in layer:
                    #         w = Wall(pos[0], pos[1], self.screen, TILE, TILE, image=surf, mask=True)
                    #         # self.mask_sprites.add(w)
                    #         self.block_sprites.add(w)
                    #         self.all_sprites.add(w)
                    
                    Tiled_Map(pos, surf, [self.map_tiles, self.all_sprites]) # key helper!!!!! 

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if layer.name == "sprites":
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        it = Item((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, im, obj.name)
                        self.item_sprites.add(it)
                        self.all_sprites.add(it)

                    elif layer.name == "collide":
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE)
                        self.block_sprites.add(w)

                    elif "sign" in obj.name:
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    elif layer.name == "interact":
                        im = pg.transform.scale(obj.image, (TILE,TILE))
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    elif obj.name == "player":
                        self.player = Player((obj.x/16)*TILE, (obj.y/16)*TILE,self.screen, self.king_right, self.king_left, self.king_up, self)
                        self.all_sprites.add(self.player)
                        self.player_alive = True

                    elif obj.name == "snake_spawn":
                        self.snake_spawns.append([(obj.x/16)*TILE, (obj.y/16)*TILE, (obj.width/16)*TILE, (obj.height/16)*TILE])

                    elif layer.name == "teleports":
                        if obj.image:
                            im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], image=im)
                            self.tele_sprites.add(t)
                            self.all_sprites.add(t)
                        else:
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], width=(obj.width/16)*TILE, height=(obj.height/16)*TILE)
                            self.tele_sprites.add(t)
        
        self.tracker = Tracker(self.player, self.snake_sprites, self.track_image, self)
        self.tracked = Marker(self.track_image)

        for y in range (1,3):
            for x in range(0, WIDTH, TILE):
                im = Background(x, HEIGHT-(TILE*y), self.floor_images[1])
                self.text_sprites.add(im)
        self.next_text = Next(WIDTH-(2*TILE), HEIGHT-TILE, self.screen, self.next_image)

        self.heart_sprites = Heart(self.hearts, PLAYER_HEARTS)

        self.game_viewer = Camera(self.tile_map.width*TILE, self.tile_map.height*TILE) # key helper!!!!!

        for i in self.item_sprites:
            self.player.inv[i.id] = 0

        self.run()

    def update(self):
        """Run all updates."""

        if len(self.snake_sprites) < ENEMY_NUMBER - self.player.k_count:
            spawn = rand.randint(0,len(self.snake_spawns)-1)
            x = rand.randrange(int(round(self.snake_spawns[spawn][0])), int(round(self.snake_spawns[spawn][0])) + int(round(self.snake_spawns[spawn][2])))
            y = rand.randrange(int(round(self.snake_spawns[spawn][1])), int(round(self.snake_spawns[spawn][1])) + int(round(self.snake_spawns[spawn][3])))
            s = Snake(x, y, self.screen, self.snake_images_r, self.snake_images_l, self)
            self.snake_sprites.add(s)
            self.all_sprites.add(s)

        if self.player.inv["bomb"] > 0:
            self.all_sprites.add(self.tracker)
            self.all_sprites.add(self.tracked)
            if self.player.use == True:
                self.player.inv["bomb"] -= 1
                e = Explosion(self.screen, self.exp_list, self)
                self.e_tick = pg.time.get_ticks()
                self.all_sprites.add(e) #FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if self.bomb_tick - self.e_tick < 10:
                    self.player.use = False
        else:
            self.all_sprites.remove(self.tracker)
            self.all_sprites.remove(self.tracked)

        self.all_sprites.update()
        self.block_sprites.update()
        self.game_viewer.update(self.player)

        self.heart_sprites.update(self.player.life)
        self.heart_sprites.bounce()

        if self.text !=False:
            self.text_sprite = TextBox(self.text, self.font, WHITE)

        if self.player_alive == False:
            self.playing = False

    def draw(self):
        """Fill screen, draw objects, flip."""

        self.map_tiles.draw(self.screen)
        for i in self.all_sprites:
            self.screen.blit(i.image, (self.game_viewer.get_view(i)))

        if self.clear == False:
            pg.draw.rect(self.screen, BLACK, (0,HEIGHT-(2.1*TILE), WIDTH, HEIGHT))
            for i in self.text_sprites:
                self.screen.blit(i.image, (i.rect.x, i.rect.y))
            self.screen.blit(self.text_sprite.image, (self.text_sprite.x,self.text_sprite.y))
            self.screen.blit(self.next_text.image, (self.next_text.rect.x, self.next_text.rect.y))
            self.next_text.bounce()
            #FIX TEXT GETTING TOO WIDE

        change = (TILE * self.heart_sprites.heart_num) - (TILE)
        for i in (self.heart_sprites.heart_values):
            self.screen.blit(self.heart_sprites.img_list[self.heart_sprites.heart_values[str(i)][0]], [self.heart_sprites.x + change, self.heart_sprites.heart_values[i][1]-15])
            change -= TILE-10

        pg.display.flip()

    def events(self):
        """Game loop events."""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if self.playing:
                    self.playing = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    self.player.use = True
                    self.bomb_tick = pg.time.get_ticks()
                elif event.key == pg.K_i :
                    t = "Inventory: "
                    for i in self.player.inv:
                        if self.player.inv[i] == 1:
                            t += f"{i.capitalize()}, "
                        elif self.player.inv[i] > 1:
                            t += f"{i.capitalize()} ({self.player.inv[i]}), "
                    if t[-2] == ",":
                        t = t[0:-2]
                    self.text = t
                    self.clear = False
                elif event.key == pg.K_RETURN:
                    self.clear = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_e:
                    self.player.use = False
                elif event.key == pg.K_RETURN:
                    self.text = None

            elif event.type == pg.JOYDEVICEADDED:
               self.joy = pg.joystick.Joystick(event.device_index)

            elif event.type == pg.JOYBUTTONDOWN:
                if event.dict["button"] == 0:
                    self.player.use = True
                    self.bomb_tick = pg.time.get_ticks()
                elif event.dict["button"] == 2:
                    t = "Inventory: "
                    for i in self.player.inv:
                        if self.player.inv[i] == 1:
                            t += f"{i.capitalize()}, "
                        elif self.player.inv[i] > 1:
                            t += f"{i.capitalize()} ({self.player.inv[i]}), "
                    if t[-2] == ",":
                        t = t[0:-2]
                    self.text = t
                    self.clear = False
                elif event.dict["button"] ==1 :
                    self.clear = True


    def run(self):
        """Contains main game loop."""
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def start_screen(self):
        """Screen to start game."""
        self.screen.fill(BLACK)
        self.screen.blit(self.font.render(TEXTS["start"], True, WHITE), (0, HEIGHT//2))
        pg.display.flip()
        
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return

    def game_over(self):
        """Screen to end game."""
        pass

############################## PLAY ###################################

game = Game()

while game.running:
    game.start_screen()
    game.new()
    game.game_over()

pg.quit()