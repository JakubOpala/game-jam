from lib2to3.pgen2.token import COLON
import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image
import button

pygame.init()

WIDTH, HEIGHT = 840, 600
SIDE_MARGIN, LOWER_MARGIN = 200, 100
WIN = pygame.display.set_mode((WIDTH+SIDE_MARGIN, HEIGHT+LOWER_MARGIN))
pygame.display.set_caption("Map editor")

win_pos_x = 500 #screen_info.current_w / 2 - WIDTH / 2
win_pos_y = 500 #screen_info.current_h / 2 - HEIGHT / 2
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos_x,win_pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '1'

FPS = 60

#grid parameters
ROWS = 100
COLUMNS = 100
TILE_SIZE = 40
MAP_WIDTH = TILE_SIZE * COLUMNS
MAP_HEIGHT = TILE_SIZE * ROWS

#loading images
lava_img = pygame.image.load('images/lava.png')

TILE_TYPES = 6
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'images/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

OBJECT_TYPES = 2   
obj_list = []
for x in range(OBJECT_TYPES):
    obj = pygame.image.load(f'images/tiles/o{x}.png')
    obj = pygame.transform.scale(obj, (TILE_SIZE, TILE_SIZE))
    obj_list.append(obj)

#colours defining
WHITE = (255, 255, 255)
GREEN = (140, 190, 120)
RED = (220, 25, 25)

#scrolling
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_y = 0
scroll_x = 0
scroll_speed = 5

#buttons
current_tile = 0
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = button.Button(WIDTH + 60 * button_col + 20, 50 + 60 * button_row, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:       
        button_row += 1
        button_col = 0

if button_col != 0:
    button_row += 1
    button_col = 0
for i in range(len(obj_list)):
    tile_button = button.Button(WIDTH + 60 * button_col + 20, 50 + 60 * button_row, obj_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:       
        button_row += 1
        button_col = 0

#map
tiles = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    tiles.append(r)

objects = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    objects.append(r)



def draw_background():
    WIN.fill(GREEN)
    bg_width = lava_img.get_width()
    bg_height = lava_img.get_height()
    for x in range(4):
        for y in range(4):
            WIN.blit(lava_img, ((x * bg_width) - scroll_x,(y * bg_height) - scroll_y))

def draw_grid():
    for c in range(ROWS+1):
        pygame.draw.line(WIN, WHITE, (0, c * TILE_SIZE - scroll_y), (WIDTH + SIDE_MARGIN, c * TILE_SIZE - scroll_y))
    for c in range(COLUMNS+1):
        pygame.draw.line(WIN, WHITE, (c * TILE_SIZE - scroll_x, 0), (c * TILE_SIZE - scroll_x, HEIGHT + LOWER_MARGIN))

def draw_map():
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            if tile >= 0:
                WIN.blit(img_list[tile], (j * TILE_SIZE - scroll_x, i * TILE_SIZE - scroll_y))
    for i, row2 in enumerate(objects):
        for j, tile in enumerate(row2):
            if tile >= 0:
                WIN.blit(obj_list[tile-TILE_TYPES], (j * TILE_SIZE - scroll_x, i * TILE_SIZE - scroll_y))

clock = pygame.time.Clock()
run = True

while run:

    clock.tick(FPS)


    if scroll_left == True and scroll_x>0:
        scroll_x -= 5
    if scroll_right == True and scroll_x<(MAP_WIDTH - WIDTH):
        scroll_x += 5
    if scroll_up == True and scroll_y>0:
        scroll_y -= 5
    if scroll_down == True and scroll_y<(MAP_HEIGHT - HEIGHT):
        scroll_y += 5

    #gettin mouse position
    pos = pygame.mouse.get_pos()    
    x = (pos[0] + scroll_x) // TILE_SIZE
    y = (pos[1] + scroll_y) // TILE_SIZE

    if pos[0] < WIDTH and pos[1] < HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if current_tile <= 5:
                if tiles[y][x] != current_tile:
                    tiles[y][x] = current_tile
            else:
                if objects[y][x] != current_tile:
                    objects[y][x] = current_tile

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False

    draw_background()
    draw_grid()

    #editing panel and buttons
    pygame.draw.rect(WIN, GREEN, (WIDTH,0, SIDE_MARGIN, HEIGHT+LOWER_MARGIN))
    pygame.draw.rect(WIN, GREEN, (0,HEIGHT, WIDTH, LOWER_MARGIN))
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(WIN):
            current_tile = button_count
    pygame.draw.rect(WIN, RED, button_list[current_tile], 3)

    draw_map()

    pygame.display.update()

        

        
pygame.quit()
