#imports
import pygame as pg
from math import pi
import random

#constants
WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
YELLOW = [238, 210, 0]
ORANGE = [255, 69, 0]
GREY = [120,120,120]
PLANET = [230, 163, 80]
RINGS = [201, 112, 48]

FAST_COMET = 6.5
SLOW_COMET = 4

ALIEN_MOVE_SIDE = 5
ALIEN_MOVE_UP = 5

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

def planet(x, y, canvas):
    pg.draw.arc(canvas, RINGS, [x-150, y-10, 300,40], .5*pi, .49*pi, 6)
    pg.draw.circle(canvas, PLANET, [x, y], 80, 80)
    pg.draw.arc(canvas, RINGS, [x-150, y-10, 300,40], .9*pi, .1*pi, 6)

def alien(x, y, canvas):
    pg.draw.polygon(canvas, GREEN, [[x,y], [x+20,y-100],[x+100,y-100],[x+120,y]])
    pg.draw.polygon(canvas, GREY, [[x, y-100], [x+120,y-100], [x+105,y-85], [x+15,y-85]])
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
title_font = pg.font.SysFont('comicsans', 40)
title_text = '0'
title_img = title_font.render(title_text, True, WHITE)

x_list1 = []
y_list1 = []
star_colors = [random.choice([YELLOW, WHITE]) for n in range(0, 70)]

blue_x = []
blue_y = []

orange_x = []
orange_y = []

star_x = [random.randint(0, WIDTH) for x in range( 0, 70)]
star_y = [random.randint(0, WIDTH) for y in range( 0, 70)]

for n in range(0, 7):
    x_list1.append(random.randint(0,WIDTH))
    y_list1.append(random.randint(0,HEIGHT))

for n in range(0, 5):
    blue_x.append(random.randint(0,WIDTH))
    blue_y.append(random.randint(0,HEIGHT))

for n in range(0, 2):
    orange_x.append(random.randint(0,WIDTH))
    orange_y.append(random.randint(0,HEIGHT))

x_loc = 700
y_loc = 650
x_speed = 0
y_speed = 0

frag_cords = [random.randint(50,WIDTH-50), random.randint(50,HEIGHT-50)]

# pg.mouse.set_visible(False)

#main game loop
while playing:

    #event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            playing = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                x_speed = -1 * ALIEN_MOVE_SIDE
            elif event.key == pg.K_RIGHT:
                x_speed = ALIEN_MOVE_SIDE
            elif event.key == pg.K_UP:
                y_speed = -1 * ALIEN_MOVE_UP
            elif event.key == pg.K_DOWN:
                y_speed = ALIEN_MOVE_UP
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                x_speed = 0
            elif event.key == pg.K_UP or event.key == pg.K_DOWN:
                y_speed = 0

    #game logic
    # pos = pg.mouse.get_pos()
    # mx = pos[0]
    # my = pos[1]

    x_loc += x_speed
    y_loc += y_speed

    if x_loc < -140:
        x_loc = WIDTH +30
    elif x_loc > WIDTH + 30:
        x_loc = -140
    
    if y_loc < 15:
        y_loc = HEIGHT +170
    elif y_loc > HEIGHT +170:
        y_loc = 15

    #clear the screen
    screen.fill(BLACK)

    screen.blit(title_img, (WIDTH/2+35,10))

    #draw

    for n in range(0, len(star_x)):
        pg.draw.circle(screen, star_colors[n], [star_x[n], star_y[n]], 3)

    for n in range(0,len(blue_x)):
        comet(blue_x[n], blue_y[n], BLUE, screen)
        blue_y[n] += SLOW_COMET
        blue_x[n] -= SLOW_COMET

        if blue_y[n] > HEIGHT + 50 or blue_x[n] < -40:
            blue_x[n], blue_y[n] = [random.randint(50,WIDTH+400), random.randint(-25,-5)]

    for n in range(0,len(x_list1)):
        star(x_list1[n], y_list1[n], star_colors[n], screen)

    for n in range(0,len(orange_x)):
        comet(orange_x[n], orange_y[n], ORANGE, screen)
        orange_y[n] += FAST_COMET
        orange_x[n] -= FAST_COMET

        if orange_y[n] > HEIGHT + 50 or orange_x[n] < -40:
            orange_x[n], orange_y[n] = [random.randint(50,WIDTH+400), random.randint(-25,-5)]

    #moon
    pg.draw.arc(screen, WHITE, [870,40, 80,80], MOON_BOT_START, MOON_TOP_START, 8)
    pg.draw.arc(screen, WHITE, [865,40, 80,80], MOON_BOT_START, MOON_TOP_START, 8)

    # MOON_BOT_START += MOON_CHANGE
    # if MOON_BOT_START > MOON_BOT_END or MOON_BOT_START < MOON_BOT:
    #     MOON_CHANGE = MOON_CHANGE *-1

    # MOON_TOP_START += MOON_CHANGE

    #planet
    planet(330, 300, screen)

    star(frag_cords[0], frag_cords[1], GREEN, screen)

    #alien
    alien(x_loc, y_loc, screen)

    if (frag_cords[0] >= x_loc and frag_cords[0] <= x_loc + 120) and (frag_cords[1] >= y_loc-100 and frag_cords[1] <= y_loc):
        frag_cords = [random.randint(50,WIDTH-50), random.randint(50,HEIGHT-50)]
        title_text = str(int(title_text) + 1)
        title_img = title_font.render(title_text, True, WHITE)

    #update screen
    pg.display.flip()

    #limit to fps
    clock.tick(FPS)

pg.quit()