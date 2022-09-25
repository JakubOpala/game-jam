from lib2to3.pgen2.token import COLON
import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image
import button

pygame.init()

WIDTH, HEIGHT = 1000, 600
SIDE_MARGIN, LOWER_MARGIN = 100, 100
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

#loading images
lava_img = pygame.image.load('images/lava.png')
tile1 = pygame.image.load('images/tiles/1.png')
TILE_TYPES = 8
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load('images/tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


#colours defining
WHITE = (255, 255, 255)
GREEN = (140, 190, 120)

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
    tile_button = button.Button(WIDTH + 50 * button_col + 50, 50 + 30 * button_row, img_list[i], 1)
    button_list.apend(tile_button)
    button_col += 1
    if button_col == 3:       
        button_row += 1
        button_col = 0




def draw_background():
    WIN.fill(GREEN)
    bg_width = lava_img.get_width()
    bg_height = lava_img.get_height()
    for x in range(4):
        for y in range(4):
            WIN.blit(lava_img, ((x * bg_width) - scroll_x,(y * bg_height) - scroll_y))
    for x in range(20):
        WIN.blit(tile1, (0 - scroll_x,x * tile1.get_height() - scroll_y))

def draw_grid():
    for c in range(ROWS+1):
        pygame.draw.line(WIN, WHITE, (0, c * TILE_SIZE - scroll_y), (WIDTH + SIDE_MARGIN, c * TILE_SIZE - scroll_y))
    for c in range(COLUMNS+1):
        pygame.draw.line(WIN, WHITE, (c * TILE_SIZE - scroll_x, 0), (c * TILE_SIZE - scroll_x, HEIGHT + LOWER_MARGIN))



clock = pygame.time.Clock()
run = True

while run:

    clock.tick(FPS)

    #editing panel and buttons
    pygame.draw.rect(WIN, GREEN, (WIDTH,0, SIDE_MARGIN, HEIGHT))
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(WIN):
            current_tile = button_count

    if scroll_left == True and scroll_x>0:
        scroll_x -= 5
    if scroll_right == True:
        scroll_x += 5
    if scroll_up == True and scroll_y>0:
        scroll_y -= 5
    if scroll_down == True:
        scroll_y += 5

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
    pygame.display.update()

        

        
pygame.quit()
