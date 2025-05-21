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
        self.menu_music = pg.mixer.Sound("sprite_game/sounds/menu.wav")
        self.town_music = pg.mixer.Sound("sprite_game/sounds/TownTheme.mp3")

        self.font = pg.font.Font("sprite_game/Perfect DOS VGA 437.ttf", 30)
        self.joy = None

        #changes in start screen based on user input
        self.control = None

        #sets the map keyword
        self.game_map = "town"
        self.change_map = False

        #saves important data across maps
        self.persistant = {"npcs":{}}
        self.names = ["Liz", "Lulu", "Irene", "Carol", "Lewis"]
        self.sprite_code = 0

    def load_images(self):
        """Load and get images."""

        self.floor_images = []
        for i in range(4):
            wood = SpriteSheet(f"sprite_game/sprites/spr_wood_texture_{i}.png")
            img = wood.get_image(0,0,16,16, 4,4)
            img.set_alpha(150)
            self.floor_images.append(img)

        chars_sheet = SpriteSheet("sprite_game/sprites/new_chars.png")
        self.king_still = chars_sheet.get_image(17,10*18-1, 32,46,True)

        self.king_right = []
        self.king_left = []
        self.king_up = []

        self.green_right = []
        self.green_left = []
        self.green_up = []

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

        for i in range(10):
            if i <= 5:
                green_r = chars_sheet.get_image(780+(TILE*i),13.5*18-3, 39,48,1.1,1.1)
                green_r.set_colorkey(NEW_CHARS)
                self.green_right.append(green_r)
                green_l = pg.transform.flip(green_r, True, False)
                self.green_left.append(green_l)
            else:
                green_up = chars_sheet.get_image(780+(TILE*i),13.5*18-3, 39,48,1.1,1.1)
                green_up.set_colorkey(NEW_CHARS)
                self.green_up.append(green_up)

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

        self.speaking = {}
        speaking_sheet = SpriteSheet("sprite_game/sprites/speaking.png")
        self.thinking = {}

        thinking_sheet = SpriteSheet("sprite_game/sprites/thinking.png")

        count = 0
        for y in range(0,6):
            for x in range(0,5):
                image = speaking_sheet.get_image(x*16,y*16,16,16,1.5,1.5)
                image.set_colorkey(BLACK)
                self.speaking[BUBBLES[count]] = image
                count += 1
        count = 0
        for y in range(0,6):
            for x in range(0,5):
                image = thinking_sheet.get_image(x*17-3,y*17-1,16,16,1.5,1.5)
                image.set_colorkey(BLACK)
                self.thinking[BUBBLES[count]] = image
                count += 1

    def tile_generation(self, map):
        #this function gets the current map and re-adjusts the tiles to create/display
        #called once upon creation and subsequently when player interacts with a "newmap" sprite

        self.block_sprites = pg.sprite.Group()
        self.npc_sprites = pg.sprite.Group()
        self.npc_block_sprites = pg.sprite.Group()
        self.mask_sprites = pg.sprite.Group()
        self.snake_sprites = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.tele_sprites = pg.sprite.Group()
        self.newmap_sprites = pg.sprite.Group()
        self.text_sprites = pg.sprite.Group()
        self.response_sprites = pg.sprite.Group()
        self.bubble_sprites = pg.sprite.Group()

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
                    #pick-up items
                    if layer.name == "sprites":
                        im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                        it = Item((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, im, obj.name, self.sprite_code)
                        self.item_sprites.add(it)
                        self.all_sprites.add(it)
                        self.sprite_code +=1

                    #walls
                    elif layer.name == "collide":
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE)
                        self.block_sprites.add(w)

                    #walls for npc to prevent getting stuck -- doesnt affect player
                    elif layer.name == "npc_collide":
                        w = Wall((obj.x/16)*TILE, (obj.y/16)*TILE, self.screen, (obj.height/16)*TILE, (obj.width/16)*TILE)
                        self.npc_block_sprites.add(w)

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
                    elif layer.name == "teleports":
                        if obj.image:
                            im = pg.transform.scale(obj.image, (TILE/2,TILE/2))
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], image=im)
                            self.tele_sprites.add(t)
                            self.all_sprites.add(t)
                        else:
                            t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], width=(obj.width/16)*TILE, height=(obj.height/16)*TILE)
                            self.tele_sprites.add(t)

                    elif layer.name == "newmaps":
                        t = Teleporter((obj.x/16)*TILE, (obj.y/16)*TILE, obj.name.split("_")[0], obj.name.split("_")[1], obj.name.split("_")[-1], loc=obj.name.split("_")[2], width=(obj.width/16)*TILE, height=(obj.height/16)*TILE)
                        self.newmap_sprites.add(t)

                    elif obj.name == "npc_move":
                        n = Npc((obj.x/16)*TILE, (obj.y/16)*TILE,self.screen, self.green_right, self.green_left, self.green_up, self)
                        self.all_sprites.add(n)
                        self.npc_sprites.add(n)

                    #player
                    elif obj.name == "player":
                        self.player = Player((obj.x/16)*TILE, (obj.y/16)*TILE,self.screen, self.green_right, self.green_left, self.green_up, self)
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

        for y in range(2):
            for x in range(3):
                im = Background(WIDTH -(TILE) - (TILE*x), HEIGHT-(3.5*TILE) - (TILE*y), self.floor_images[1])
                self.response_sprites.add(im)

    def new(self):
        """Create all game objects, sprites, and groups. Call run() method"""
        self.text = None
        self.clear = True
        self.menu_music.stop()
        self.town_music.play(-1)

        self.tile_generation(self.game_map)

        self.heart_sprites = Heart(self.hearts, PLAYER_HEARTS)

        self.game_viewer = Camera(self.tile_map.width*TILE, self.tile_map.height*TILE)

        self.selected_index = -1
        if self.joy:
            self.last_joy = pg.time.get_ticks()

        self.run()

    def update(self):
        """Run all updates."""
        try:
            print(self.prompt, self.player_response, self.player.current_npc.quest)
        except:
            pass
        #for each npc, sees which are talking and which are thinking
        #if either are true, creates a speech/thought bubble for them
        for i in self.npc_sprites:
            if i.talk == True:
                speech = self.speaking
            elif i.think == True:
                speech = self.thinking
            if i.emotion:
                b = Speech(i, speech, i.emotion, self.screen, self)
                i.bubble = b
                self.all_sprites.add(b)
                self.bubble_sprites.add(b)

        #if the npc is no longer speaking/thinking or has changed emotions, kills the old 
        for i in self.bubble_sprites:
            if i.owner.bubble != i.self or i.owner.emotion != i.emotion:
                i.kill()

        #spawns snake randomly in the confines of the snake_spawn areas
        if len(self.snake_sprites) < ENEMY_NUMBER - self.player.k_count:
            spawn = rand.randint(0,len(self.snake_spawns)-1)
            x = rand.randrange(int(round(self.snake_spawns[spawn][0])), int(round(self.snake_spawns[spawn][0])) + int(round(self.snake_spawns[spawn][2])))
            y = rand.randrange(int(round(self.snake_spawns[spawn][1])), int(round(self.snake_spawns[spawn][1])) + int(round(self.snake_spawns[spawn][3])))
            s = Snake(x, y, self.screen, self.snake_images_r, self.snake_images_l, self)
            self.snake_sprites.add(s)
            self.all_sprites.add(s)

        #if the player has a bomb, the player's snake tracker is now active and visible. it disapears (but still exists) if the player runs out of bombs
        if "bomb" in self.player.inv:
            self.all_sprites.add(self.tracker)
            self.all_sprites.add(self.tracked)
            if self.player.use == True and self.player.inv["bomb"] > 0:
                #if the player uses a bomb, take it from the inventory and start an explosion
                self.player.inv["bomb"] -= 1
                e = Explosion(self.screen, self.exp_list, self)
                self.explode_sound.play()

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
        self.npc_block_sprites.update()
        self.game_viewer.update(self.player)

        self.heart_sprites.update(self.player.life)
        self.heart_sprites.bounce()

        if self.clear == False:
            try:
                if TEXTS["inv_full"][:-3] in self.text:
                    self.prompt = "inv_full"
                    self.player.velo = PLAYER_VELO/PLAYER_VELO
                else:
                    self.player.velo = 0
            except:
                pass

        #if text is a string, makes an image based on that text
        if self.text:
            if "Inventory:" not in self.text and "npc" in self.prompt and self.player.current_npc.name not in self.text:
                self.text = self.player.current_npc.name+ ": " + self.text
            self.text_sprite = TextBox(self.text, self.font, WHITE)
            if "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                self.choices = []
                for i in TEXTS[self.prompt]["response"]:
                    self.choices.append(TextBox(i, self.font, WHITE))

                if self.selected_index == -1:
                    self.selected_index = len(self.choices)-1
                elif self.selected_index == len(self.choices):
                    self.selected_index = 0

                self.selected_choice = {"x": WIDTH-(TILE), "y":HEIGHT-(3.23*TILE) - (TILE*self.selected_index), "response": self.choices[self.selected_index]}

            #(NOT PROGRAMMED) working to split the text for additional sections if the text image is too large for the text box
            if (self.text_sprite.image.get_width() + self.text_sprite.x) >= (self.next_text.rect.x - self.next_text.image.get_width()):
                pass
            #if this happens, put into a list. the lsit shoudl then do "inventory: x, x, x, 1/x" "invenory: x, x, x, 2/x"
            #enter should push page forward, back should push backward

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

            #if dialogue options are present, it adds the box for those to appear as well
            if "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                pg.draw.rect(self.screen, BLACK, (WIDTH-(TILE*3.1),HEIGHT-(4.6*TILE), 3.3*TILE, 2.2*TILE))
                for i in self.response_sprites:
                    self.screen.blit(i.image, (i.rect.x, i.rect.y))
                for i in range(len(self.choices)):
                    self.screen.blit(self.choices[i].image, ((WIDTH-(TILE*2.8), HEIGHT-(3.3*TILE) - (TILE*i))))
                self.screen.blit(self.next_text.image, (self.selected_choice["x"], self.selected_choice["y"]))

            else:
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
                self.running = False
                self.playing = False
                break

            elif event.type == pg.KEYDOWN:
                #this section helps move the selector icon for dialogue options
                if event.key == pg.K_DOWN:
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.selected_index += 1

                elif event.key == pg.K_UP:
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.selected_index -= 1

                #e for using a bomb, gets the time it was pressed
                elif event.key == pg.K_e:
                    self.player.use = True
                    self.bomb_tick = pg.time.get_ticks()

                #i for inventory, turns the text variable from none to a string with everything in the inventory
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

                #when hitting t, checks for which npc to start talking and says player is now talking with npc
                elif event.key == pg.K_t:
                    for i in self.npc_sprites:
                        if i.talk == True:
                            self.player.talking = True
                            self.prompt = "npc_talk_default"
                            self.text = TEXTS["npc_talk_default"]["say"]
                            self.clear = False

                #checks to see if there's more text, otherwise closes dialgoue box (including inventory)
                elif event.key == pg.K_RETURN:
                    #this sections checks if the text is more than one line
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.player_response = TEXTS[self.prompt]["response"][self.selected_index]
                        #if it is and the player continues the dialogue, move onto the quest
                        #the quest is an item and the amount
                        if self.player_response == "Quest":
                            if self.player.current_npc.quest == None:
                                self.prompt = "npc_want"
                                self.quest = rand.choice(QUESTS)
                                self.text = TEXTS[self.prompt]["say"]
                                self.text = self.text.replace("-", str(self.quest["n"]))
                                if self.quest["n"] > 1:
                                    self.text = self.text.replace("_", self.quest["item"]+"s")
                                else:
                                    self.text = self.text.replace("_", self.quest["item"])

                            elif self.player.current_npc.quest != None and self.player.current_npc.quest != "Done":
                                #if the quest can be completed, prompt to complete
                                if self.player.current_npc.quest["item"] in self.player.inv.keys() and self.player.inv[self.player.current_npc.quest["item"]] == self.player.current_npc.quest["n"]:
                                    self.prompt = "quest_prompt"
                                    self.text = TEXTS[self.prompt]["say"]

                                #if not, say the quest again
                                else:
                                    self.prompt = "npc_have_quest"
                                    text = TEXTS[self.prompt]
                                    self.text = text.replace("-", str(self.player.current_npc.quest["n"]))
                                    if self.player.current_npc.quest["n"] > 1:
                                        self.text = self.text.replace("_", self.player.current_npc.quest["item"]+"s")
                                    else:
                                        self.text = self.text.replace("_", self.player.current_npc.quest["item"])

                        elif self.player_response == "Accept":
                            self.player.current_npc.quest = self.quest
                            self.quest = None
                            self.text = None
                            self.clear = True
                            self.player.velo = PLAYER_VELO
                            if self.player.talking == True:
                                self.player.talking = False
                            self.selected_index = -1
                            self.prompt=None
                        
                        #if the player says "bye", ends the dialogue like normal
                        elif self.player_response == "Bye" or self.player_response == "No":
                            self.clear = True
                            self.text = None
                            self.player.velo = PLAYER_VELO
                            if self.player.talking == True:
                                self.player.talking = False
                            self.selected_index = -1
                            self.prompt=None

                        elif self.player_response == "Yes" and self.prompt != "removed":
                            self.prompt = "removed"
                            self.text = TEXTS[self.prompt]
                            self.text = self.text.replace("-", str(self.player.current_npc.quest["n"]))
                            if self.player.current_npc.quest["n"] > 1:
                                self.text = self.text.replace("_", self.player.current_npc.quest["item"]+"s")
                            else:
                                self.text = self.text.replace("_", self.player.current_npc.quest["item"])
                            self.player.inv[self.player.current_npc.quest["item"]] -= self.player.current_npc.quest["n"]
                            self.player.current_npc.quest = "Done"

                        elif self.player_response == "Yes" and self.player.current_npc.quest == "Done":
                            self.prompt == "npc_finish_quest"
                            self.text = TEXTS[self.prompt]

                    else: 
                        self.clear = True
                        self.text = None
                        self.player.velo = PLAYER_VELO
                        if self.player.talking == True:
                            self.player.talking = False
                        self.selected_index = -1
                        self.prompt=None

            elif event.type == pg.KEYUP:
                if event.key == pg.K_e:
                    self.player.use = False
            
            #all actions are the same as the keyboard, just to different buttons ########################################## controller
            elif event.type == pg.JOYBUTTONDOWN:

                #x button
                if event.dict["button"] == 2:
                    actions = []
                    #checks for talking, if true, a initiates dialogue
                    for i in self.npc_sprites:
                        if i.talk == True:
                            self.player.talking = True
                            self.prompt = "npc_talk_default"
                            self.text = TEXTS["npc_talk_default"]["say"]
                            self.clear = False
                            actions.append(True)

                    #otherwise, uses bomb
                    if True not in actions:
                        self.player.use = True
                        self.bomb_tick = pg.time.get_ticks()
                #a
                elif event.dict["button"] == 0:
                    #this sections checks if the text is more than one line
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.player_response = TEXTS[self.prompt]["response"][self.selected_index]
                        #if it is and the player continues the dialogue, move onto the quest
                        #the quest is an item and the amount
                        if self.player_response == "Quest":
                            if self.player.current_npc.quest == None:
                                self.prompt = "npc_want"
                                self.quest = rand.choice(QUESTS)
                                self.text = TEXTS[self.prompt]["say"]
                                self.text = self.text.replace("-", str(self.quest["n"]))
                                if self.quest["n"] > 1:
                                    self.text = self.text.replace("_", self.quest["item"]+"s")
                                else:
                                    self.text = self.text.replace("_", self.quest["item"])

                            else:
                                self.prompt = "npc_have_quest"
                                text = TEXTS[self.prompt]
                                self.text = text.replace("-", str(self.player.current_npc.quest["n"]))
                                if self.player.current_npc.quest["n"] > 1:
                                    self.text = self.text.replace("_", self.player.current_npc.quest["item"]+"s")
                                else:
                                    self.text = self.text.replace("_", self.player.current_npc.quest["item"])

                        elif self.player_response == "Accept":
                            self.clear = True
                            self.player.velo = PLAYER_VELO
                            if self.player.talking == True:
                                self.player.talking = False
                        
                        #if the player says "bye", ends the dialogue like normal
                        elif self.player_response == "Bye":
                            self.clear = True
                            self.player.velo = PLAYER_VELO
                            if self.player.talking == True:
                                self.player.talking = False

                    else:
                        self.joy_tick = pg.time.get_ticks()
                        if self.joy_tick - self.last_joy > JOY_DELAY:
                            if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                                pass
                            else: 
                                self.clear = True
                                self.player.velo = PLAYER_VELO
                                if self.player.talking == True:
                                    self.player.talking = False
                                

                #+ button
                elif event.dict["button"] == 6:
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

            if self.joy.get_axis(1) < 0 - JOY_MINIMUM:
                self.joy_tick = pg.time.get_ticks()
                if self.joy_tick - self.last_joy > JOY_DELAY:
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.selected_index += 1
                        self.last_joy = self.joy_tick

            elif self.joy.get_axis(1) > JOY_MINIMUM:
                self.joy_tick = pg.time.get_ticks()
                if self.joy_tick - self.last_joy > JOY_DELAY:
                    if self.clear == False and "Inventory:" not in self.text and type(TEXTS[self.prompt]) == dict:
                        self.selected_index -= 1
                        self.last_joy = self.joy_tick

    def run(self):
        """Contains main game loop."""
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            if self.change_map ==True:
                for i in self.npc_sprites:
                    self.persistant["npcs"][i.name] = {"name":i.name, "quest":i.quest, "map":i.map}
                self.sprite_code = 0
                #checks to see if the player is changing the map area. first, changes the map and hten updates the players persistant data
                self.tile_generation(self.game_map)
                self.change_map = False
                self.player.newmap_spawn()
                self.player.inv = self.persistant["player"]["inv"]
                self.player.inv_codes = self.persistant["player"]["codes"]
                self.player.k_count = self.persistant["player"]["kills"]
                self.player.life = self.persistant["player"]["life"]

                for i in range(0, len(list(self.npc_sprites))-1):
                    if self.game_map == list(self.npc_sprites)[i].map:
                        list(self.npc_sprites)[i].name = self.persistant["npcs"][list(self.persistant["npcs"])[i]]["name"]
                        list(self.npc_sprites)[i].quest = self.persistant["npcs"][list(self.persistant["npcs"])[i]]["quest"]
                        list(self.npc_sprites)[i].map = self.persistant["npcs"][list(self.persistant["npcs"])[i]]["map"]

                #sprite codes (when paired with sprite ids) identify and remove sprites from the map if they are already in the player's inventory
                #(ie "bomb" 1 is in inv so take it off map, but dont remove "mush" 1)
                for i in self.item_sprites:
                    if i.id in self.player.inv and i.code in self.player.inv_codes:
                        i.kill()

    def start_screen(self):
        """Screen to start game."""
        #displays intro text
        start = True

        self.selected = "Keys"
        control_error = False
        self.last_joy = pg.time.get_ticks()

        while start:
            self.town_music.stop()
            self.menu_music.play(-1)
            self.screen.fill(TIES)

            if self.selected == "Keys":
                t = TEXTS["start"]
                t = t.replace("_", "Enter")
                shift = 70
            else:
                t = TEXTS["start"]
                t = t.replace("_", "A")
                shift = 100

            #text section for keyboard
            self.screen.blit(self.font.render("Keyboard", True, WHITE), (WIDTH//4 + 20, HEIGHT//4))
            pg.draw.ellipse(self.screen, WHITE, (WIDTH//3 - 20, HEIGHT//3-10, 45,45), 3)

            #text section for controller
            self.screen.blit(self.font.render("Controller", True, WHITE), (WIDTH//2+ 30, HEIGHT//4))
            pg.draw.ellipse(self.screen, WHITE, (2*WIDTH//3 - 70, HEIGHT//3-10, 45,45), 3)

            self.screen.blit(self.font.render(t, True, WHITE), (WIDTH//4+ shift, HEIGHT//2))

            #draw a circle around whichever one is currently selected
            if self.selected == "Keys":
                k = Next(WIDTH//3 - 10, HEIGHT//3, self.screen, self.next_image)
                self.screen.blit(k.image, (k.rect.x, k.rect.y))
            else:
                j = Next(2*WIDTH//3 - 60, HEIGHT//3, self.screen, self.next_image)
                self.screen.blit(j.image, (j.rect.x, j.rect.y))

            #display error text
            if control_error:
                self.screen.blit(self.font.render("No controller connected!", True, WHITE), (WIDTH//4+ 25, HEIGHT//1.5))

            pg.display.flip()
        
            for event in pg.event.get():

                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    start = False

                #connects a controller, checks if joy is the selected type
                elif event.type == pg.JOYDEVICEADDED:
                    self.joy = pg.joystick.Joystick(event.device_index)
                    if self.selected == "Joy":
                        control_error = False

                elif event.type == pg.KEYDOWN:
                    #return ends this screen and begins the game
                    #sets the game input as either keys or controller ----(ALLOW THIS TO BE CHANGED IN PAUSE MENU IF IMPLEMENTED)
                    if event.key == pg.K_RETURN:
                        #if controller is selected but there is none, raise an error
                        if self.selected == "Joy" and self.joy == None:
                            control_error = True
                        else:
                            self.control = self.selected
                            return
                    
                    #changes selected based on player input
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        if self.selected == "Keys":
                            self.selected = "Joy"
                        else:
                            self.selected = "Keys"

                elif self.joy.get_axis(0) < 0 - JOY_MINIMUM or self.joy.get_axis(0) > JOY_MINIMUM:
                    self.joy_tick = pg.time.get_ticks()
                    if self.joy_tick - self.last_joy > JOY_DELAY:
                        if self.selected == "Keys":
                            self.selected = "Joy"
                        else:
                            self.selected = "Keys"
                        self.last_joy = self.joy_tick

                elif event.type == pg.JOYBUTTONDOWN:
                    #a
                    if event.dict["button"] == 0:
                        if self.selected == "Joy" and self.joy == None:
                            control_error = True
                        else:
                            self.control = self.selected
                            return

    def game_over(self):
        """Screen to end game."""
        #displays text
        end = True

        self.selected = "Restart"
        self.last_joy = pg.time.get_ticks()

        while end:
            self.town_music.stop()
            self.menu_music.play(-1)
            self.screen.fill(TIES)

            #text section for restarting
            self.screen.blit(self.font.render("Restart", True, WHITE), (WIDTH//4 + 20, HEIGHT//4))
            pg.draw.ellipse(self.screen, WHITE, (WIDTH//3 - 20, HEIGHT//3-10, 45,45), 3)

            #text section for quitting
            self.screen.blit(self.font.render("Quit", True, WHITE), (WIDTH//2+ 80, HEIGHT//4))
            pg.draw.ellipse(self.screen, WHITE, (2*WIDTH//3 - 70, HEIGHT//3-10, 45,45), 3)

            #draw a circle around whichever one is currently selected
            if self.selected == "Restart":
                k = Next(WIDTH//3 - 10, HEIGHT//3, self.screen, self.next_image)
                self.screen.blit(k.image, (k.rect.x, k.rect.y))
            else:
                j = Next(2*WIDTH//3 - 60, HEIGHT//3, self.screen, self.next_image)
                self.screen.blit(j.image, (j.rect.x, j.rect.y))

            pg.display.flip()
        
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.running = False
                    end = False

                elif event.type == pg.KEYDOWN:
                    #return ends this screen and either begins the game or quits
                    if event.key == pg.K_RETURN:
                        if self.selected == "Restart":
                            end = False
                        else:
                            end = False
                            self.running = False
                            # path = "sprite_game/data.txt"
                            # data = open(path, 'a')
                            # data.write(f"{self.player.k_count}\n")
                            break
                    
                    #changes selected based on player input
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        if self.selected == "Restart":
                            self.selected = "Quit"
                        else:
                            self.selected = "Restart"

                elif self.joy.get_axis(0) < 0 - JOY_MINIMUM or self.joy.get_axis(0) > JOY_MINIMUM:
                    self.joy_tick = pg.time.get_ticks()
                    if self.joy_tick - self.last_joy > JOY_DELAY:
                        if self.selected == "Restart":
                            self.selected = "Quit"
                        else:
                            self.selected = "Restart"
                        self.last_joy = self.joy_tick

                elif event.type == pg.JOYBUTTONDOWN:
                    #a
                    if event.dict["button"] == 0:
                        if self.selected == "Restart":
                            end = False
                        else:
                            end = False
                            self.running = False
                            # path = "sprite_game/data.txt"
                            # data = open(path, 'a')
                            # data.write(f"{self.player.k_count}\n")
                            break

############################## PLAY ###################################

game = Game()
game.start_screen()

while game.running:
    #sends the base map in
    game.new()
    game.game_over()

pg.quit()