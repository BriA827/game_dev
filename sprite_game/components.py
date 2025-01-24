import pygame as pg
from settings import *

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
    def __init__(self,x,y, display, right_ani, left_ani, up_ani, game):
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
        self.run = None #-1 = left, none = none, 1 = right, 2 = up

        self.current_frame = 0
        self.delay = 70
        self.last = pg.time.get_ticks()

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

    def collide_wall(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.self.x_change > 0:
                    self.x = hits[0].rect.left - self.rect.width
                elif self.self.x_change < 0:
                    self.x = hits[0].rect.right
                self.self.x_change=0
                self.rect.x = self.x

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.wall_sprites, False)
            if hits:
                if self.self.y_change > 0:
                    self.y = hits[0].rect.top - self.rect.height
                elif self.self.y_change < 0:
                    self.y = hits[0].rect.bottom
                self.self.y_change=0
                self.rect.y = self.y

class Wall(pg.sprite.Sprite):
    def __init__(self, x, y, display, image):
        pg.sprite.Sprite.__init__(self)

        self.self = self
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display

class Snake(pg.sprite.Sprite):
    def __init__(self, x, y, display, image_list, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.self = self
        self.image_list = image_list
        self.image = image_list[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.velo = 3
    
    def update(self):
        self.rect.x -= self.velo
        self.now = pg.time.get_ticks()
        if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.image_list)
                self.image = self.image_list[self.current_frame]
                self.last = self.now
        
        hits = pg.sprite.spritecollide(self, self.game.wall_sprites, False)
        if hits:
            self.velo = self.velo * -1
            self.image
            