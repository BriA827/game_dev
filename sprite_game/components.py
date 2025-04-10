import pygame as pg
from settings import *
import math
from pygame.math import Vector2 as vec

class SpriteSheet():
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height, scale_x = None, scale_y = None, color=None):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width,height))
        if scale_x and scale_y:
            image = pg.transform.scale(image, (width*scale_x, height*scale_y))

        if color:
            c = image.get_at([0,0])
            image.set_colorkey(c)
        return image
    
class Player(pg.sprite.Sprite):
    def __init__(self, x, y, display, right_ani, left_ani, up_ani, game):
        pg.sprite.Sprite.__init__(self)
        self.right_ani = right_ani
        self.left_ani = left_ani
        self.up_ani = up_ani

        self.image = self.right_ani[0]
        self.rect = self.image.get_rect()
        self.self = self
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.game = game

        self.velo = 5
        self.run = None #-1 = left, none = none, 1 = right, 2 = up, -2 = down

        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()

        self.inv = {}
        self.use = False

        self.life = 0
        self.k_count  = 0

        self.player_mask = pg.mask.from_surface(self.image)
        self.mask_image = self.player_mask.to_surface()

    def update(self):
        self.x_change = 0
        self.y_change = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left_ani)
                self.image = self.left_ani[self.current_frame]
                self.last = self.now
            self.x_change = -1* self.velo
            self.run = -1

        elif keys[pg.K_RIGHT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.right_ani)
                self.image = self.right_ani[self.current_frame]
                self.last = self.now
            self.x_change = self.velo
            self.run = 1

        elif keys[pg.K_UP]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.up_ani)
                self.image = self.up_ani[self.current_frame]
                self.last = self.now
            self.y_change = -1 * self.velo
            self.run = 2

        elif keys[pg.K_DOWN]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.right_ani)
                self.image = self.right_ani[self.current_frame]
                self.last = self.now
            self.y_change = self.velo
            self.run = -2

        else:
            self.x_change = 0
            if self.run == -1:
                self.image = self.left_ani[0]
            elif self.run == 1 or self.run == -2:
                self.image = self.right_ani[0]
            elif self.run == 2:
                self.image = self.up_ani[0]

            # self.run = None
        self.player_mask = pg.mask.from_surface(self.image)
        self.mask_image = self.player_mask.to_surface()

        self.rect.x += self.x_change
        self.collide_wall('x')

        self.rect.y += self.y_change
        self.collide_wall('y')

        self.collide_snake()
        self.collide_item()
        self.collide_tele()

    def collide_wall(self, dir):
        #collision rectangle
        if pg.sprite.spritecollide(self, self.game.block_sprites, False):
            hits = pg.sprite.spritecollide(self, self.game.block_sprites, False)
            if dir == 'x':
                if self.x_change > 0:
                    self.x = hits[0].rect.left - self.rect.width
                elif self.self.x_change < 0:
                    self.x = hits[0].rect.right
                self.x_change = 0
                self.rect.x = self.x

            elif dir == 'y':
                if self.y_change > 0:
                    self.y = hits[0].rect.top - self.rect.height
                elif self.self.y_change < 0:
                    self.y = hits[0].rect.bottom
                self.y_change=0
                self.rect.y = self.y

        #collision mask
        if pg.sprite.spritecollide(self, self.game.mask_sprites, False):
            hits = pg.sprite.spritecollide(self, self.game.mask_sprites, False, pg.sprite.collide_mask)

            if hits:
                if self.x_change > 0:
                    self.x = hits[0].rect.left - (self.rect.width)
                if self.x_change < 0:
                    self.x = hits[0].rect.right
                if self.y_change > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.y = hits[0].rect.bottom

                self.y_change = 0
                self.x_change = 0
                self.rect.y = self.y
                self.rect.x = self.x

    def collide_snake(self):
        hits = pg.sprite.spritecollide(self, self.game.snake_sprites, False)
        if hits:
            self.life += .5
            if self.life == 10:
                self.game.player_alive = False

    def collide_item(self):
        sp = pg.sprite.Group.sprites(self.game.item_sprites)
        hits = pg.sprite.spritecollide(self, self.game.item_sprites, False)
        for i in sp:
            if i in hits:
                if self.inv[i.id] < PLAYER_INV_MAX:
                    self.inv[i.id] += 1
                    i.kill()
                else:
                    self.game.text = TEXTS["inv_full"].replace("_", i.id+"s")
                    self.game.clear = False
                    hits.remove(i)

    # def collide_door(self):
    #     hits = pg.sprite.spritecollide(self, self.game.door_sprites, False)
    #     if hits:
    #         if self.game.map == OVERWORLD:
    #             return HOUSE
    #         else:
    #             return OVERWORLD

    def collide_tele(self):
        hits = pg.sprite.spritecollide(self, self.game.tele_sprites, False)
        if hits:
            new_name = hits[0].companion
            for i in self.game.tele_sprites:
                if i.name == new_name:
                    new = i
                    break
            if new.displace == "down":
                self.rect.x, self.rect.y = new.rect.x, new.rect.y + (TILE*.8)
            else:
                self.rect.x, self.rect.y = new.rect.x, new.rect.y - (TILE*.8)

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, height, width, image = None, bomb = False, mask = False):
        pg.sprite.Sprite.__init__(self)

        self.self = self
        if image:
            self.image = image
            self.rect = self.image.get_rect()
        else:
            self.rect = pg.Rect(x, y, width, height)
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.bomb = bomb

        if mask == True and image:
            self.wall_mask = pg.mask.from_surface(self.image)
            self.wall_mask_image = self.wall_mask.to_surface()

class Snake(pg.sprite.Sprite):
    def __init__(self, x, y, display, right, left, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.self = self
        self.right = right
        self.left = left
        self.image = right[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.velo = 3

        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
    
    def update(self):
        self.targetx = self.game.player.rect.center[0]
        self.targety = self.game.player.rect.center[1]
        
        self.rect.x += self.velo

        self.now = pg.time.get_ticks()

        if self.velo > 0:
            self.direct = self.right
        elif self.velo < 0:
            self.direct = self.left

        if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.direct)
                self.image = self.direct[self.current_frame]
                self.last = self.now
        
        hits = pg.sprite.spritecollide(self, self.game.block_sprites, False)
        if hits:
            self.velo = self.velo * -1
            # self.velo = 0

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, display, image, name):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.id = name

class Explosion(pg.sprite.Sprite):
    def __init__(self, display, images, game):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.display = display

        self.current_frame = 0
        self.delay = 16
        self.last = pg.time.get_ticks()

        self.game = game
        if self.game.player.run == 1: #right
            self.rect.x = self.game.player.rect.topleft[0]+40
            self.rect.y = self.game.player.rect.topleft[1]-10
        elif self.game.player.run == -1: #left
            self.rect.x = self.game.player.rect.topleft[0]-70
            self.rect.y = self.game.player.rect.topleft[1]-10
        elif self.game.player.run == 2: #up
            self.rect.x = self.game.player.rect.topleft[0]-10
            self.rect.y = self.game.player.rect.topleft[1]-70
        elif self.game.player.run == -2: #down
            self.rect.x = self.game.player.rect.topleft[0]-10
            self.rect.y = self.game.player.rect.topleft[1]+50

    def update(self):
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last = self.now

        if self.image == self.images[-1]:
            self.kill()

        self.collide()

    def collide(self):
        hits = pg.sprite.spritecollide(self, self.game.snake_sprites, False)
        if hits:
            hits[0].kill()
            self.game.player.k_count +=1
            print(self.game.player.k_count)

class Camera():
    def __init__(self, width, height):
        self.self = self
        self.camera = pg.Rect(0,0, width, height)
        self.width = width
        self.height = height

    def get_view(self, sprite_object):
        #all sprite objects will be moved based on camera position
        return sprite_object.rect.move(self.camera.topleft)
    
    def update(self, target):
        #shift map in opp direction
        #add half window size
        x = -target.rect.x + WIDTH//2
        y = -target.rect.y + HEIGHT//2

        #stop scrolling at end
        #if too far left, reset to 0
        x = min(0,x)
        y = min(0,y)

        #too far right, stay half
        x = max(-1 * (self.width - WIDTH), x)
        y = max(-1 * (self.height - HEIGHT), y)
        self.camera = pg.Rect(x, y, self.width, self.height)

class Background(pg.sprite.Sprite):
    def __init__(self, x, y, image):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Marker(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.image = image
        self.rect = self.image.get_rect()

class Tracker(pg.sprite.Sprite):
    def __init__(self, owner, target, image, game):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.game = game

        self.owner = owner
        self.targets = target
        self.target = None

        self.image = image
        self.base_image = image
        self.rect = self.image.get_rect()

        self.radius = (self.owner.rect.width + self.owner.rect.height) / 2
        self.rect.x, self.rect.y = self.owner.rect.center[0] - 5,  self.owner.rect.top - 20

        self.initial_angle = 90

    def closest(self):
        self.target = min([s for s in self.targets], key= lambda s: math.sqrt(((s.rect.center[0] - self.owner.rect.center[0])**2) + ((s.rect.center[1] - self.owner.rect.center[1])**2)))
        if self.target.velo < 0:
            self.game.tracked.rect.x, self.game.tracked.rect.y = self.target.rect.center[0]-15, self.target.rect.top
        else:
            self.game.tracked.rect.x, self.game.tracked.rect.y = self.target.rect.center[0]+1, self.target.rect.top

    def angle_x_y(self):
        rang = math.radians(self.angle)
        self.rect.x = self.radius/math.cos(rang)
        self.rect.y = self.radius/math.sin(rang)
        #FIX THIS!!!!!!!!!!!!!!!!!!!!!!!!

    def rotate(self):
        self.angle = self.initial_angle - math.atan2(self.target.rect.center[1]-self.rect.center[1], self.target.rect.center[0]-self.rect.center[0]) *  (180/math.pi) 
        # self.initial_angle = angle
        self.image = pg.transform.rotate(self.base_image, self.angle)

    def update(self):
        self.closest()
        self.rotate()
        # self.angle_x_y()
        self.rect.x, self.rect.y = self.owner.rect.center[0] - 5,  self.owner.rect.top - 20


class Door(pg.sprite.Sprite):
    def __init__(self, x, y, display, image, game):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.display = display
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

class Teleporter(pg.sprite.Sprite):
    def __init__(self, x, y, name, companion, displace, width=None, height=None, image = None):
        pg.sprite.Sprite.__init__(self)
        if image:
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = pg.rect.Rect(x,y,width,height)
        self.name = name
        self.companion = companion
        self.displace = displace

class TextBox(pg.sprite.Sprite):
    def __init__(self, text, font, color):
        pg.sprite.Sprite.__init__(self)
        self.image = font.render(text, True, color)
        self.x = TILE/2
        self.y = HEIGHT-TILE-(TILE/2)

class Heart(pg.sprite.Sprite):
    def __init__(self, img_list, heart_num):
        pg.sprite.Sprite.__init__(self)
        self.img_list = img_list
        self.self = self
        self.x = 0 - TILE/3
        self.y = TILE/2
        self.heart_values = {}
        self.heart_num = heart_num
        self.hit_goal = 1
        self.life_img = 1
        self.life_index = 0
        for i in range(0, self.heart_num):
            self.heart_values[str(i)] = 0

    def update(self, p_health):
        if p_health == self.hit_goal:
            self.heart_values[str(self.life_index)] = self.life_img
            self.hit_goal+=1
            self.life_img+= 1
            if self.life_img == 3:
                self.life_index+= 1
                self.life_img= 1

class Next(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.start_y = y
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.speed = 2
        self.dir = True

    def bounce(self):
        self.y_change = 0
        if self.dir == True:
            self.y_change -= self.speed
            print(self.y_change)
            if self.rect.y - self.start_y <= 10:
                self.dir = False
        else:
            self.y_change += self.speed
            if self.rect.y - self.start_y >= 10:
                self.dir = True
        self.rect.y += self.y_change
        #FIX THIS LATERRRRRRRR