import pygame as pg
from settings import *

class Player:
    def __init__(self,x,y,width,height,color,display) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.color = color
        self.display = display
        self.x_velo = 5

        self.y_velo = 5
        self.jumping = False
        self.landed = True

        self.rect = pg.Rect(self.x, self.y,width,height)
        self.status = True
        self.win = False

    def draw(self):
        pg.draw.rect(self.display, self.color, self.rect)

    def update(self, surface_list, doors, monsters):
        x_change = 0
        y_change = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            x_change = -1* self.x_velo
        if keys[pg.K_RIGHT]:
            x_change = self.x_velo

        if keys[pg.K_SPACE] and not self.jumping and self.landed:
            self.jumping = True
            self.landed = False
            self.y_velo = -19

        if not keys[pg.K_SPACE]:
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
            if door.rect.colliderect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height):
                x_change = 0
                self.y_velo = 0
                self.win = True

        for monster in monsters:
            if monster.rect.colliderect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height):
                self.status = False

        # if self.rect.bottom + y_change > HEIGHT - BRICK_HEIGHT:
        #     y_change = 0
        #     self.rect.bottom = HEIGHT - BRICK_HEIGHT
        #     self.landed = True
        
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
    def __init__(self, x, y, width, height, color, display) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.color = color
        self.display = display

        self.rect = pg.Rect(self.x,self.y, width,height)
    
    def draw(self):
        pg.draw.rect(self.display, self.color, self.rect)



class Enemy:
    def __init__(self, x, y, width, height, color, display, velo, confined) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.color = color
        self.display = display
        self.velo = velo
        self.confined = confined

        self.rect = pg.Rect(self.x,self.y,width,height)
    
    def draw(self):
          pg.draw.rect(self.display, self.color, self.rect)

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
    def __init__(self, x, y, width, height, color, display):
        self.self = self
        self. x = x
        self.y = y
        self. color = color
        self.display = display
        self.rect = pg.Rect(self.x, self.y, width, height)

    def draw(self):
        pg.draw.rect(self.display, self.color, self.rect)