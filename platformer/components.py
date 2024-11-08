import pygame as pg

class Player:
    def __init__(self,x,y,width,height,color,display) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.color = color
        self.display = display
        self.velo = 5
        self.x_velo = 0

        self.y_velo = 5
        self.jumping = False
        self.falling = False
        self.y_counter = 0
        self.jump_height = self.height/1.5

    def move(self):
        self.x += self.x_velo

        if self.jumping:
            self.y_counter +=1
            self.y -= self.y_velo

            if self.y_counter >= self.jump_height:
                self.jumping = False
                self.falling = True

        if self.falling:
            self.y_counter-= 1
            self.y += self.y_velo
            if self.y_counter == 0:
                self.falling = False

    def keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.x_velo = -1 * self.velo
        elif keys[pg.K_RIGHT]:
            self.x_velo = self.velo
        elif keys[pg.K_SPACE] and self.jumping is False and self.falling is False:
            self.jumping = True
            self.y_counter = 0
        else:
            self.x_velo = 0
    
    def draw(self):
        pg.draw.rect(self.display,self.color, [self.x,self.y, self.width, self.height])

class Brick:
    def __init__(self, x, y, width, height, color, display) -> None:
        self.self = self
        self.x = x
        self.y = y
        self.width = width 
        self.height = height
        self.color = color
        self.display = display
    
    def draw(self):
        pg.draw.rect(self.display, self.color, [self.x,self.y, self.width,self.height])

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
        
    def stopped(self, blocked, screen_width):
        if self.x <= blocked-5:
            self.x = screen_width + blocked