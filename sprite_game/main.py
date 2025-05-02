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

        self.explode_sound = pg.mixer.Sound("sprite_game/sounds/explosion.wav")

        # self.path = pg.font.match_font("sprite_game/Perfect DOS VGA 437.ttf", 0, 0)
        self.font = pg.font.SysFont("Perfect DOS VGA 437 Win", 30)
        self.joy = None

        #changes in start screen based on user input
        self.control = "Keys"

        #sets the map keyword
        self.game_map = "town"
        self.change_map = False

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

    def tile_generation(self, map):
        #this function gets the current map and re-adjusts the tiles to create/display
        #called once upon creation and subsequently when player interacts with a "new_map" sprite

        self.block_sprites = pg.sprite.Group()
        self.mask_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.tele_sprites = pg.sprite.Group()
        self.newmap_sprites = pg.sprite.Group()
        self.text_sprites = pg.sprite.Group()

        self.map_tiles = pg.sprite.Group()

        self.snake_spawns = []

        self.tile_map = pytmx.load_pygame(f"sprite_game/tiles/{map}.tmx")
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
                    #pick up items
                    if layer.name == "sprites":
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        it = Item((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, im, obj.name)
                        self.item_sprites.add(it)
                        self.all_sprites.add(it)

                    #walls
                    elif layer.name == "collide":
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE)
                        self.block_sprites.add(w)

                    #signposts (NOT PROGRAMMED)
                    elif "sign" in obj.name:
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    #interactables (NOT PROGRAMMED)
                    elif layer.name == "interact":
                        im = pg.transform.scale(obj.image, (TILE,TILE))
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE, image=im)
                        self.block_sprites.add(w)
                        self.all_sprites.add(w)

                    #sets areas for snakes to potentially spawn
                    elif obj.name == "snake_spawn":
                        self.snake_spawns.append([(obj.x/16)*TILE, (obj.y/16)*TILE, (obj.width/16)*TILE, (obj.height/16)*TILE])

                    #teleports for images and areas
                    elif layer.name == "teleports" or layer.name == "newmaps":
                        if obj.image:
                            im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], image=im)
                            if layer.name =="teleports":
                                self.tele_sprites.add(t)
                            else:
                                self.newmap_sprites.add(t)
                            self.all_sprites.add(t)
                        else:
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], width=(obj.width/16)*TILE, height=(obj.height/16)*TILE)
                            if layer.name =="teleports":
                                self.tele_sprites.add(t)
                            else:
                                self.newmap_sprites.add(t)

    #fix the game not workingnow HAHAHAH

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""
        self.text = False
        self.clear = True

        self.tile_generation(self.game_map)

        #player created seperately from base position
        for layer in self.tile_map.visible_layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    self.player = Player((obj.x/16)*TILE, (obj.y/16)*TILE,self.screen, self.king_right, self.king_left, self.king_up, self)
                    self.all_sprites.add(self.player)
                    self.player_alive = True
        
        #creates a tracker for the player that looks for the closest snake
        self.tracker = Tracker(self.player, self.snake_sprites, self.track_image, self)
        self.tracked = Marker(self.track_image)

        #sets up the text box
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
        print(self.player.inv)

        #spawns snake randomly in the confines of the snake_spawn areas
        if len(self.snake_sprites) < ENEMY_NUMBER - self.player.k_count:
            spawn = rand.randint(0,len(self.snake_spawns)-1)
            x = rand.randrange(int(round(self.snake_spawns[spawn][0])), int(round(self.snake_spawns[spawn][0])) + int(round(self.snake_spawns[spawn][2])))
            y = rand.randrange(int(round(self.snake_spawns[spawn][1])), int(round(self.snake_spawns[spawn][1])) + int(round(self.snake_spawns[spawn][3])))
            s = Snake(x, y, self.screen, self.snake_images_r, self.snake_images_l, self)
            self.snake_sprites.add(s)
            self.all_sprites.add(s)

        #if the player has a bomb, the player's snake tracker is now active and visible. it disapears (but still exists) if the player runs out of bombs
        if self.player.inv["bomb"] > 0:
            self.all_sprites.add(self.tracker)
            self.all_sprites.add(self.tracked)
            if self.player.use == True:
                #if the player uses a bomb, take it from the inventory and start an explosion
                self.player.inv["bomb"] -= 1
                e = Explosion(self.screen, self.exp_list, self)
                # self.explode_sound.play(1)

                #get the amout of time it takes for an explosion versus when the button was pressed. if the explosion is still running, does not start another
                self.e_tick = pg.time.get_ticks()
                self.all_sprites.add(e)
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

        #if text is a string, makes an image based on that text
        if self.text !=False:
            self.text_sprite = TextBox(self.text, self.font, WHITE)
            #(NOT PROGRAMMED) working to split the text for additional sections if the text image is too large for the text box
            if (self.text_sprite.image.get_width() + self.text_sprite.x) >= (self.next_text.rect.x - self.next_text.image.get_width()):
                self.text = self.text.split() #FIX THIS

        #player dead, game over
        if self.player_alive == False:
            self.playing = False

    def draw(self):
        """Fill screen, draw objects, flip."""
     
        self.map_tiles.draw(self.screen)
        for i in self.all_sprites:
            self.screen.blit(i.image, (self.game_viewer.get_view(i)))

        if self.clear == False:
            #draws the textbox and text, bounces the next button
            pg.draw.rect(self.screen, BLACK, (0,HEIGHT-(2.1*TILE), WIDTH, HEIGHT))
            for i in self.text_sprites:
                self.screen.blit(i.image, (i.rect.x, i.rect.y))
            self.screen.blit(self.text_sprite.image, (self.text_sprite.x,self.text_sprite.y))
            self.screen.blit(self.next_text.image, (self.next_text.rect.x, self.next_text.rect.y))
            self.next_text.bounce()

        #displays the hearts (multiple for one sprite) on screen and shifts them from each other
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
                #e for using a bomb, gets the time it was pressed
                if event.key == pg.K_e:
                    self.player.use = True
                    self.bomb_tick = pg.time.get_ticks()

                #i for inventory, assigns the text variable from false to a string with everything in the inventory
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

                #return closes the inventory 
                elif event.key == pg.K_RETURN:
                    self.clear = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_e:
                    self.player.use = False

                elif event.key == pg.K_RETURN:
                    self.text = None

            #connects a controller
            elif event.type == pg.JOYDEVICEADDED:
               self.joy = pg.joystick.Joystick(event.device_index)
            
            #all actions are the same as the keyboard, just to different buttons
            elif event.type == pg.JOYBUTTONDOWN:
                #a button?
                if event.dict["button"] == 0:
                    self.player.use = True
                    self.bomb_tick = pg.time.get_ticks()

                #+ button? x button?
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

                #b button? 
                elif event.dict["button"] ==1 :
                    self.clear = True

    def run(self):
        """Contains main game loop."""
        self.playing = True
        print(self.player.inv)
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            if self.change_map ==True:
                self.tile_generation(self.game_map)
                self.change_map = False

    def start_screen(self):
        """Screen to start game."""
        #displays intro text
        while True:
            self.screen.fill(BLACK)
            self.screen.blit(self.font.render(TEXTS["start"], True, WHITE), (0, HEIGHT//2))
            pg.display.flip()
        
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    #return ends this screen and begins the game
                    if event.key == pg.K_RETURN:
                        return

    def game_over(self):
        """Screen to end game."""
        pass

############################## PLAY ###################################

game = Game()
game.start_screen()

while game.running:
    #sends the base map in
    game.new()
    game.game_over()

pg.quit()