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

    def draw(self):
        pg.draw.rect(self.display, self.color, self.rect)

    def update(self, surface_list):
        x_change = 0
        y_change = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] and self.rect.x > BRICK_WIDTH:
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
                pass
        # if self.rect.bottom + y_change > HEIGHT - BRICK_HEIGHT:
        #     y_change = 0
        #     self.rect.bottom = HEIGHT - BRICK_HEIGHT
        #     self.landed = True
        
        self.rect.x += x_change
        self.rect.y += y_change



class Brick:
    def __init__(self, x, y, width, height, color, display) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.color = color
        self.display = display

        self.rect = pg.Rect(self.x,self.y, self.width,self.height)
    
    def draw(self):
        pg.draw.rect(self.display, self.color, self.rect)



class Enemy:
    def __init__(self, x, y, width, height, color, display, velo) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.color = color
        self.display = display
        self.velo = velo
    
    def draw(self):
          pg.draw.rect(self.display, self.color, [self.x,self.y, self.width,self.height])

    def move(self):
        self.x -= self.velo
        
    def stopped(self):
        if self.x <= BRICK_WIDTH-5:
            self.x = WIDTH + BRICK_WIDTH