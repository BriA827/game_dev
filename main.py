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
GREY = (120,120,120)
PLANET = (250, 183, 90)

FPS = 60

#functions
def draw_rect(x, y, color, canvas):
    pg.draw.rect(canvas, color, [x, y, 150,100])

def star(x, y, color, canvas):
    pg.draw.polygon(canvas, color, [[x+30,y-20],[x+40,y],[x+60,y],[x+45,y+15],[x+55,y+35],[x+30,y+25],[x+5,y+35],[x+15,y+15],[x,y],[x+20,y]])

def comet(x, y, color, canvas):
    pg.draw.circle(canvas, color, [x,y], 10,10)
    pg.draw.polygon(canvas, color, [[x,y-10], [x+15,y-35], [x+15,y-25], [x+55, y-60], [x+40,y-30], [x+50, y-30], [x+5, y]])

#setup
pg.init()

width = 1000
height = 700
screen = pg.display.set_mode([width, height])
clock = pg.time.Clock()

playing = True 

#code
title_font = pg.font.SysFont('comicsans', 13)
title_text = 'The Everlasting Lord of Arcane Wisdom, Shouki no Kami, the Prodigal'
title_img = title_font.render(title_text, True, BLACK)

x_list1 = []
y_list1 = []
star_colors = []

x_list2 = []
y_list2 = []
comet_colors = []

for n in range(0, random.randint(10,19)):
    x_list1.append(random.randint(0,width))
    y_list1.append(random.randint(0,height))
    star_colors.append(random.choice([YELLOW, WHITE]))

for n in range(0, random.randint(10,14)):
    x_list2.append(random.randint(0,width))
    y_list2.append(random.randint(0,height))
    comet_colors.append(random.choice([BLUE, ORANGE]))

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
    for n in range(0,len(x_list1)):
        star(x_list1[n], y_list1[n], star_colors[n], screen)

    for n in range(0,len(x_list2)):
        comet(x_list2[n], y_list2[n], comet_colors[n], screen)

    #moon
    pg.draw.arc(screen, WHITE, [850,50, 80,80], 8.5*pi/6, 4*pi/6, 3)
    pg.draw.arc(screen, WHITE, [845,50, 80,80], 8.5*pi/6, 4*pi/6, 5)

    #planet
    pg.draw.arc(screen, ORANGE, [350, 290, 300,40], .5*pi, .49*pi, 6)
    pg.draw.circle(screen, PLANET, [500, 300], 80, 80)
    pg.draw.arc(screen, ORANGE, [350, 290, 300,40], .9*pi, .1*pi, 6)

    #alien
    pg.draw.polygon(screen, GREEN, [[700,650], [720,550],[800,550],[820,650]])
    pg.draw.polygon(screen, GREY, [[670,550], [720,500],[800,500],[850,550]])
    pg.draw.arc(screen, GREY, [720,455,80,90], 0, 1*pi, 3)
    pg.draw.rect(screen,GREEN, [750, 490, 20,10])
    pg.draw.ellipse(screen,GREEN, [750, 460, 20, 30])
    circ_x = 710
    for n in range(0,5):
        pg.draw.circle(screen, YELLOW, [circ_x, 535], 5,5)
        circ_x += 25
    eye_x = 755
    for n in range(0,2):
        pg.draw.circle(screen, BLACK, [eye_x, 475], 3,3)
        eye_x += 10
    
    #update screen
    pg.display.flip()

    #limit to fps
    clock.tick(FPS)

pg.quit()