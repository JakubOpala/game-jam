from lib2to3.pgen2.token import COLON
import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image

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

#loading images
lava_img = pygame.image.load('images/lava.png')
TILE_TYPES = 12
img_list = []
#for x in range(TILE_TYPES):


#colours defining
WHITE = (255, 255, 255)
GREEN = (140, 190, 120)

#grid parameters
ROWS = 100
COLUMNS = 100
TILE_SIZE = 40

#scrolling
scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False
scroll_y = 0
scroll_x = 0
scroll_speed = 5


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



clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
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
