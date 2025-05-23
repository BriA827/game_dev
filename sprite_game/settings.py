import pygame as pg

WHITE = [255,255,255]
BLACK = [0,0,0]
RED = [255,0,0]
GREEN = [0,255,0]
BUE = [0,0,255]
YEOW = [238, 210, 0]
ORANGE = [255, 69, 0]
GREY = [120,120,120]
NEW_CHARS = [160, 160, 160]
TIES = [63, 38, 49]
DARK_GREEN = [30,57,22]

FPS = 60

TILE = 64

#size of the pygame WINDOW
WIDTH = 15*TILE
HEIGHT = 10*TILE

ENEMY_NUMBER = 3
ENEMY_RESPAWN = False
SNAKE_DMG = .25

#max of each item
PLAYER_INV_MAX = 3
PLAYER_HEARTS = 5
PLAYER_VELO = 4

#controller has slight drift, adjusts for that
JOY_MINIMUM = 0.004
JOY_DELAY = 300

TICK_OFFSET = 10

TEXTS = {"start": "Press _ to start", "inv_full": "You can't hold any more _!", "npc_talk_default":{"say":"Hello. Lovely weather we're having.", "response":["Bye", "Quest"]}, "npc_want": {"say": "I want - _, please.", "response":["Bye", "Accept"]}, "npc_have_quest": "I asked for - _.", "npc_finish_quest":"Oh, thank you! Here, take this.", "gained": "Gained - _ in your inventory.", "removed": "Removed - _ from your inventory.", "quest_prompt":{"say":"Complete quest?", "response":["No", "Yes"]}, "npc_happy":"Great to see you!", "won":"You killed all the snakes!"}
QUESTS = [{"item": "mush", "n":3}, {"item": "log", "n":2}, {"item": "log", "n":2}, {"item": "bag", "n":1}, {"item": "key", "n":1}]
BUBBLES = ["swirl", 'music', 'sad', 'sweat1', 'blue', 'sparkle', 'laugh', 'happy', 'dot3', 'money', 'star', 'idea', 'empty', 'dot2', 'lines', 'z2', 'heart2', 'exclaim2', 'dot1', 'angry', 'z1', 'broken', 'exclaim1', 'no', 'shine', 'question', 'heart1', 'sweat2', 'cloud', 'evil']