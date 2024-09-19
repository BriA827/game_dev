#imports
import pygame as pg
from math import pi
import random

#constants
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (238, 210, 2)
ORANGE = (255, 69, 0)

PLANET = (207, 193, 171)

FPS = 60

#functions
def draw_rect(x, y, color, canvas):
    pg.draw.rect(canvas, color, [x, y, 150,100])

def star(x, y, color, canvas):
    pg.draw.polygon(canvas, color, [[x+30,y-25],[x+40,y],[x+60,y],[x+45,y+15],[x+55,y+35],[x+30,y+25],[x+5,y+35],[x+15,y+15],[x,y],[x+20,y]])
#setup
pg.init()

screen = pg.display.set_mode([600, 400])
clock = pg.time.Clock()

playing = True 

#code
title_font = pg.font.SysFont('comicsans', 13)
title_text = 'The Everlasting Lord of Arcane Wisdom, Shouki no Kami, the Prodigal'
title_img = title_font.render(title_text, True, BLACK)

x_list = []
y_list = []
colors = []
for n in range(0, random.randint(7,19)):
    x_list.append(random.randint(0,500))
    y_list.append(random.randint(50,300))
    colors.append(random.choice([YELLOW, ORANGE, WHITE]))

#main game loop
while playing:

    #event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False

    #game logic

    #clear the screen
    screen.fill(BLACK)

    #blit
    #problem 4
    # screen.blit(title_img, (10,10))

    #draw
    for n in range(0,len(x_list)):
        star(x_list[n], y_list[n], colors[n], screen)

    pg.draw.arc(screen, WHITE, [480,30, 70,70], 8.5*pi/6, 4*pi/6, 3)
    pg.draw.arc(screen, WHITE, [475,30, 70,70], 8.5*pi/6, 4*pi/6, 5)

    pg.draw.circle(screen, PLANET, [300, 200], 50, 50)
    
    #update screen
    pg.display.flip()

    #limit to fps
    clock.tick(FPS)

pg.quit()