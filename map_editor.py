from curses import KEY_ENTER
from lib2to3.pgen2.token import COLON
import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image
import button
import csv
import easygui


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

#saving and loading
map_name = 'new_map'
save = 0
load = 0
level = 0
font = pygame.font.SysFont('Futura', 30)
font2 = pygame.font.SysFont('Futura', 20)

#grid parameters
ROWS = 50
COLUMNS = 50
TILE_SIZE = 32
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
    obj = pygame.image.load(f'images/objects/o{x}.png')
    obj = pygame.transform.scale(obj, (TILE_SIZE, TILE_SIZE))
    obj_list.append(obj)

save_img = pygame.image.load('images/buttons/save.png')
save_click_img = pygame.image.load('images/buttons/save_click.png')
load_img = pygame.image.load('images/buttons/load.png')
load_click_img = pygame.image.load('images/buttons/load_click.png')


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

save_button = button.Button(WIDTH + (SIDE_MARGIN - save_img.get_width()) // 2, HEIGHT - 120, save_img, 1)
load_button = button.Button(WIDTH + (SIDE_MARGIN - load_img.get_width()) // 2, HEIGHT - 60, load_img, 1)

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

#text on screen
def draw_text(text, font, text_col, x, y ):
    img = font.render(text, True, text_col)
    WIN.blit(img, (x, y))


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

    draw_background()
    draw_grid()
    draw_map()

    #margins for editing panel
    pygame.draw.rect(WIN, GREEN, (WIDTH,0, SIDE_MARGIN, HEIGHT+LOWER_MARGIN))
    pygame.draw.rect(WIN, GREEN, (0,HEIGHT, WIDTH, LOWER_MARGIN))

    draw_text(f'Level: {level}', font, WHITE, 10, HEIGHT + 10)

    #drawing buttons
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(WIN):
            current_tile = button_count
    pygame.draw.rect(WIN, RED, button_list[current_tile], 3)
    #save and load map
    if save_button.draw(WIN):
        save = 1
        pygame.draw.rect(WIN, RED, save_button, 3)

    if load_button.draw(WIN):
        load = 1
        pygame.draw.rect(WIN, RED, load_button, 3)
    
    
                 
    
    load_button.draw(WIN)

    #pygame.display.update()

    #end of drawing


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

    #drawing tiles/objects on map
    if pos[0] < WIDTH and x < COLUMNS and pos[1] < HEIGHT and y < ROWS:
        if pygame.mouse.get_pressed()[0] == 1:
            if current_tile <= 5:
                if tiles[y][x] != current_tile:
                    tiles[y][x] = current_tile
            else:
                if objects[y][x] != current_tile:
                    objects[y][x] = current_tile

    #scrolling
    for event in pygame.event.get():
        if save == 1:
            #pygame.draw.rect(WIN, GREEN, ((WIDTH + SIDE_MARGIN) // 2 - 100, (HEIGHT + LOWER_MARGIN) // 2 - 50, 200, 100))       
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(map_name) > 0:
                        map_name = map_name[:-1]
                elif event.key == pygame.K_RETURN and len(map_name) > 0:
                    save = 0
                    with open(os.path.join('maps', map_name) + '.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter = ';')
                        for row in tiles:
                            writer.writerow(row)
                        for row in objects:
                            writer.writerow(row)
                    #with open(map_name + '_objects.csv', 'w', newline='') as csvfile2:
                    #    writer = csv.writer(csvfile2, delimiter = ',')
                    #    for row in objects:
                    #        writer.writerow(row)
                else:
                    map_name = map_name + pygame.key.name(event.key)  #+= event.unicode
            #draw_text(map_name, font2, WHITE, (WIDTH + SIDE_MARGIN) // 2 - 80, (HEIGHT + LOWER_MARGIN) // 2 - 40)    
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
    
    #saving map
    if save == 1:
        pygame.draw.rect(WIN, GREEN, ((WIDTH + SIDE_MARGIN) // 2 - 100, (HEIGHT + LOWER_MARGIN) // 2 - 50, 200, 100))
        draw_text(map_name, font2, WHITE, (WIDTH + SIDE_MARGIN) // 2 - 80, (HEIGHT + LOWER_MARGIN) // 2 - 40)   

    if load == 1:
        scroll_x = 0
        scroll_y = 0
        path = os.path.join('maps')
        file = easygui.fileopenbox()    
        with open(os.path.join('maps', file), 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ';')   
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    if x < ROWS:
                        tiles[x][y] = int(tile)
                    else:
                        objects[x-COLUMNS][y-ROWS] = int(tile)
        

        load = 0

    pygame.display.update()        
        
pygame.quit()
