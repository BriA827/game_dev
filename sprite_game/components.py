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
        self.hit_rect = pg.Rect(0,0,32,32)
        self.rot_speed = 200
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0)
        self.rot = 0
        self.pos = vec(x,y) *TILE
        self.self = self
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.game = game

        self.velo = 5
        self.run = None #-1 = left, none = none, 1 = right, 2 = up

        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()

        self.inv = []
        self.use = False

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
            self.run = 1

        else:
            self.x_change = 0
            if self.run == -1:
                self.image = self.left_ani[0]
            elif self.run == 1:
                self.image = self.right_ani[0]
            elif self.run == 2:
                self.image = self.up_ani[0]

            self.run = None

        self.rect.x += self.x_change
        self.collide_wall('x')

        self.rect.y += self.y_change
        self.collide_wall('y')

        self.collide_snake()
        self.collide_item()
        self.collide_door()

    def collide_wall(self, dir):
        if dir == 'x':
            self.hits = pg.sprite.spritecollide(self, self.game.block_sprites, False)
            if self.hits:
                if self.x_change > 0:
                    self.x = self.hits[0].rect.left - self.rect.width
                elif self.self.x_change < 0:
                    self.x = self.hits[0].rect.right
                self.x_change = 0
                self.rect.x = self.x

        if dir == 'y':
            self.hits = pg.sprite.spritecollide(self, self.game.block_sprites, False)
            if self.hits:
                if self.y_change > 0:
                    self.y = self.hits[0].rect.top - self.rect.height
                elif self.self.y_change < 0:
                    self.y = self.hits[0].rect.bottom
                self.y_change=0
                self.rect.y = self.y

    def collide_snake(self):
        pg.sprite.spritecollide(self, self.game.snake_sprites, True)

    def collide_item(self):
        sp = pg.sprite.Group.sprites(self.game.item_sprites)
        hits = pg.sprite.spritecollide(self, self.game.item_sprites, True)
        for i in sp:
            if "Bomb" in str(type(i)) and i in hits:
                self.inv.append("Bomb")

    def collide_door(self):
        hits = pg.sprite.spritecollide(self, self.game.door_sprites, False)
        if hits:
            if self.game.map == OVERWORLD:
                return HOUSE
            else:
                return OVERWORLD

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image, bomb =False):
        pg.sprite.Sprite.__init__(self)

        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.bomb = bomb

class Snake(pg.sprite.Sprite):
    def __init__(self, x, y, display, right, left, game, d):
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
        self.velo = 3 * d

        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()
    
    def update(self):
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
        
        hits = pg.sprite.spritecollide(self, self.game.wall_sprites, False)
        if hits:
            self.velo = self.velo * -1

class Bomb(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y, display, images):
        pg.sprite.Sprite.__init__(self)
        self.self = self
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

        self.current_frame = 0
        self.delay = 16
        self.last = pg.time.get_ticks()

    def update(self):
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.image = self.images[self.current_frame]
            self.last = self.now

        if self.image == self.images[-1]:
            self.kill()

    def draw(self):
        self.display.blit(self.image, (self.rect.x, self.rect.y))

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
        self.image = image
        self.rect = self.image.get_rect()
        self.owner = owner
        self.targets = target
        self.target = None
        self.angle = (180+90)/2

    def update(self):
        if self.game.map == OVERWORLD:
            self.target = min([s for s in self.targets], key= lambda s: math.sqrt(((s.rect.center[0] - self.owner.rect.center[0])**2) + ((s.rect.center[1] - self.owner.rect.center[1])**2)))
            self.rect.x, self.rect.y = self.owner.rect.center[0] - 5,  self.owner.rect.top - 20
            if self.target.velo < 0:
                self.game.tracked.rect.x, self.game.tracked.rect.y = self.target.rect.center[0]-15, self.target.rect.top
            else:
                self.game.tracked.rect.x, self.game.tracked.rect.y = self.target.rect.center[0]+1, self.target.rect.top

            angle = (math.atan(self.target.rect.center[1]/self.target.rect.center[0])) * (180/math.pi)
            # self.angle = self.angle + angle
            # self.image = pg.transform.rotate(self.image, self.angle)

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