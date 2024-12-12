import pygame as pg
from settings import *

class Player:
    def __init__(self,x,y,display, right_ani, left_ani):
        self.right_ani = right_ani
        self.left_ani = left_ani
        self.image = self.right_ani[0]
        self.rect = self.image.get_rect()
        self.self = self
        self.rect.x = x
        self.rect.y = y
        self.display = display

        self.x_velo = 5
        self.run = None #false = left, none = none, right = true
        self.y_velo = 5
        self.jumping = False
        self.landed = True

        self.current_frame = 0
        self.delay = 30
        self.last = pg.time.get_ticks()

        self.life = 100
        self.status = True
        self.win = False

    def draw(self):
        self.display.blit(self.image, self.rect)

    def update(self, surface_list, doors, eles, monsters, unlocked):
        x_change = 0
        y_change = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.left_ani)
                self.image = self.left_ani[self.current_frame]
                self.last = self.now
            x_change = -1* self.x_velo
            self.run = False

        elif keys[pg.K_RIGHT]:
            self.now = pg.time.get_ticks()
            if self.now - self.last > self.delay:
                self.current_frame = (self.current_frame + 1) % len(self.right_ani)
                self.image = self.right_ani[self.current_frame]
                self.last = self.now
            x_change = self.x_velo
            self.run = True

        else:
            x_change = 0
            if self.run == False:
                self.image = self.left_ani[0]
            elif self.run == True:
                self.image = self.right_ani[0]
            self.run = None

        if keys[pg.K_UP] and not self.jumping and self.landed:
            self.jumping = True
            self.landed = False
            self.y_velo = -19

        if not keys[pg.K_UP]:
            self.jumping = False

        self.y_velo += GRAVITY
        if self.y_velo > 10:
            self.y_velo = 10
        
        y_change += self.y_velo

        for surface in surface_list:
            if surface.rect.colliderect(self.rect.x, self.rect.y + y_change, self.rect.width, self.rect.height):
                if self.y_velo >= 0:
                    y_change = surface.rect.top - self.rect.bottom
                    self.landed = True
                    self.jumping = False
                    self.y_velo = 0
                elif self.y_velo <0:
                    y_change = surface.rect.bottom - self.rect.top
                    self.y_velo = 0
            if surface.rect.colliderect(self.rect.x + x_change, self.rect.y, self.rect.width, self.rect.height):
                x_change = 0

        for door in doors:
            if door.rect.colliderect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height) and unlocked == True:
                x_change = 0
                self.y_velo = 0
                self.win = True

        for ele in eles:
            if ele.rect.colliderect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.rect.y = ele.rect.y -35
                self.landed
                self.landed = True
                self.jumping = False
                self.y_velo = 0
                if ele.direction == True and keys[pg.K_LEFT] != True and  keys[pg.K_RIGHT] != True:
                    self.rect.x = ele.rect.x

        for monster in monsters:
            if monster.rect.colliderect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.life -= ENEMY_DAMAGE
                if self.life == 0:
                    self.status = False
        
        self.rect.x += x_change
        self.rect.y += y_change

        if self.rect.y >= HEIGHT:
            self.status = False

    def end(self):
        if self.status == False:
            return self.status
        if self.win == True:
            return self.win



class Brick:
    def __init__(self, x, y, width, height, color, display, image=None):
        self.self = self
        if image == None:
            self.rect = pg.Rect(x,y,width,height)
            self.image = image
        else:
            self.image = pg.transform.scale(image, (width, height))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.display = display
    
    def draw(self):
        if self.image == None:
            pg.draw.rect(self.display, self.color, self.rect)
        else:
            self.display.blit(self.image, self.rect)

class Elevator:
    def __init__(self, x, y, width, height, color, display, move=False, image=False, direction=None):
        self.self = self
        if image == None:
            self.rect = pg.Rect(x,y,width,height)
            self.image = image
        else:
            self.image = pg.transform.scale(image, (width, height))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.display = display
        self.move = move
        self.direction = direction
        self.velo = 2

    def draw(self):
        if self.image == None:
            pg.draw.rect(self.display, self.color, self.rect)
        else:
            self.display.blit(self.image, self.rect)
    
    def lift(self, max, player):
        if self.move == True:
            if self.direction == False:
                for m in max:
                    if m.rect.colliderect(self.rect.x, self.rect.y - self.velo, self.rect.width, self.rect.height):
                        self.velo = self.velo * -1
                self.rect.y -= self.velo
            else:
                for m in max:
                    if m.rect.colliderect(self.rect.x - self.velo, self.rect.y, self.rect.width, self.rect.height):
                        self.velo = self.velo * -1
                self.rect.x -= self.velo

class Enemy:
    def __init__(self, x, y, width, height, color, display, velo, confined, image):
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.self = self
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.display = display
        self.velo = velo
        self.confined = confined
    
    def draw(self):
        self.display.blit(self.image, self.rect)

    def moving(self, blocks):
        if self.confined == False:
            if self.rect.x <= BRICK_WIDTH-5:
               self.rect.x = WIDTH + BRICK_WIDTH

        else:
            for b in blocks:
                if b.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
                    self.velo = self.velo * -1

        self.rect.x -= self.velo

class Door:
    def __init__(self, x, y, width, height, color, display, image):
        self.self = self
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.display = display

    def draw(self):
        self.display.blit(self.image, self.rect)


class Crate:
    def __init__(self, x, y, width, height, color, display, image):
        self.image = pg.transform.scale(image, (width*2, height*2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.self = self
        self.color = color
        self.display = display
        self.velo = 5
    
    def moving(self, blocks, on):
        y_change = 0
        if on == True:
            m_pos = pg.mouse.get_pos()
            m = pg.Rect(m_pos[0], m_pos[1], MOUSE_RECT_SIZE, MOUSE_RECT_SIZE)
            if m.colliderect(self.rect.x, self.rect.y,self.rect.width, self.rect.height):
                self.rect.x = m_pos[0] - 15
                self.rect.y = m_pos[1] - 10
        self.rect.y += self.velo
        for b in blocks:
            if b.rect.colliderect(self.rect.x, self.rect.y+self.velo, self.rect.width, self.rect.height):
                self.velo = 0
        self.rect.y += y_change

    def draw(self):
        self.display.blit(self.image, self.rect)

class Key:
    def __init__(self, x, y, width, height, color, display, image):
        self.image = pg.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.self = self
        self.color = color
        self.display = display
        self.collected = False

    def draw(self):
        # if self.collected == False:
        self.display.blit(self.image, self.rect)

    def collect(self, player):
        if player.rect.colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
            self.collected = True
            self.rect.x = player.rect.x
            self.rect.y = player.rect.y - 27
            return True