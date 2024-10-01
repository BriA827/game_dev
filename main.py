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

FAST_COMET = 6
SLOW_COMET = 4

ALIEN_MOVE = 3.3

MOON_TOP_START = pi/3
MOON_BOT_START = pi
MOON_BOT = pi
MOON_BOT_END = 3*pi/2
MOON_CHANGE = .015

FPS = 60

#functions
def draw_rect(x, y, color, canvas):
    pg.draw.rect(canvas, color, [x, y, 150,100])

def star(x, y, color, canvas):
    pg.draw.polygon(canvas, color, [[x+30,y-20],[x+40,y],[x+60,y],[x+45,y+15],[x+55,y+35],[x+30,y+25],[x+5,y+35],[x+15,y+15],[x,y],[x+20,y]])

def comet(x, y, color, canvas):
    pg.draw.circle(canvas, color, [x,y], 10,10)
    pg.draw.polygon(canvas, color, [[x,y-10], [x+15,y-35], [x+15,y-25], [x+55, y-60], [x+40,y-30], [x+50, y-30], [x+5, y]])

def alien(x, y, canvas):
    #700, 650
    pg.draw.polygon(canvas, GREEN, [[x,y], [x+20,y-100],[x+100,y-100],[x+120,y]])
    pg.draw.polygon(canvas, GREY, [[x-30,y-100], [x+20,y-150],[x+100,y-150],[x+150,y-100]])
    pg.draw.arc(canvas, GREY, [x+20,y-195,80,90], 0, 1*pi, 3)
    pg.draw.rect(canvas,GREEN, [x+50, y-160, 20,10])
    pg.draw.ellipse(canvas,GREEN, [x+50, y-190, 20, 30])
    circ_x = x+10
    for n in range(0,5):
        pg.draw.circle(canvas, YELLOW, [circ_x, y-115], 5)
        circ_x += 25
    eye_x = x+55
    for n in range(0,2):
        pg.draw.circle(canvas, BLACK, [eye_x, y-175], 3)
        eye_x += 10

#setup
pg.init()

WIDTH = 1000
HEIGHT = 700
screen = pg.display.set_mode([WIDTH, HEIGHT])
clock = pg.time.Clock()

playing = True 

#code
title_font = pg.font.SysFont('comicsans', 13)
title_text = 'The Everlasting Lord of Arcane Wisdom, Shouki no Kami, the Prodigal'
title_img = title_font.render(title_text, True, BLACK)

x_list1 = []
y_list1 = []
star_colors = [random.choice([YELLOW, WHITE]) for n in range(0, 70)]

blue_x = []
blue_y = []

orange_x = []
orange_y = []

star_x = [random.randint(0, WIDTH) for x in range( 0, 70)]
star_y = [random.randint(0, WIDTH) for y in range( 0, 70)]

for n in range(0, random.randint(10,19)):
    x_list1.append(random.randint(0,WIDTH))
    y_list1.append(random.randint(0,HEIGHT))

for n in range(0, random.randint(10,17)):
    blue_x.append(random.randint(0,WIDTH))
    blue_y.append(random.randint(0,HEIGHT))

for n in range(0, random.randint(10,17)):
    orange_x.append(random.randint(0,WIDTH))
    orange_y.append(random.randint(0,HEIGHT))

alien_cords = [700,650]

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

    for n in range(0, len(star_x)):
        pg.draw.circle(screen, star_colors[n], [star_x[n], star_y[n]], 3)

    for n in range(0,len(blue_x)):
        comet(blue_x[n], blue_y[n], BLUE, screen)
        blue_y[n] += SLOW_COMET
        blue_x[n] -= SLOW_COMET

        if blue_y[n] > HEIGHT + 50 or blue_x[n] < -40:
            blue_x[n], blue_y[n] = [random.randint(100,WIDTH+350), random.randint(-25,-5)]

    for n in range(0,len(x_list1)):
        star(x_list1[n], y_list1[n], star_colors[n], screen)

    for n in range(0,len(orange_x)):
        comet(orange_x[n], orange_y[n], ORANGE, screen)
        orange_y[n] += FAST_COMET
        orange_x[n] -= FAST_COMET

        if orange_y[n] > HEIGHT + 50 or orange_x[n] < -40:
            orange_x[n], orange_y[n] = [random.randint(100,WIDTH+350), random.randint(-25,-5)]

    #moon
    pg.draw.arc(screen, WHITE, [870,40, 80,80], MOON_BOT_START, MOON_TOP_START, 8)
    pg.draw.arc(screen, WHITE, [865,40, 80,80], MOON_BOT_START, MOON_TOP_START, 8)

    MOON_BOT_START += MOON_CHANGE
    if MOON_BOT_START > MOON_BOT_END or MOON_BOT_START < MOON_BOT:
        MOON_CHANGE = MOON_CHANGE *-1

    MOON_TOP_START += MOON_CHANGE

    #planet
    pg.draw.arc(screen, ORANGE, [350, 290, 300,40], .5*pi, .49*pi, 6)
    pg.draw.circle(screen, PLANET, [500, 300], 80, 80)
    pg.draw.arc(screen, ORANGE, [350, 290, 300,40], .9*pi, .1*pi, 6)


    #alien
    alien(alien_cords[0], alien_cords[1], screen)
    alien_cords[1] -= ALIEN_MOVE
    if alien_cords[1] < 500 or alien_cords[1] > HEIGHT - 40:
        ALIEN_MOVE = ALIEN_MOVE * -1

    #update screen
    pg.display.flip()

    #limit to fps
    clock.tick(FPS)

pg.quit()