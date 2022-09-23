from lib2to3.pgen2.token import COLON
import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image

pygame.init()

WIDTH, HEIGHT = 800, 400
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

#colours defining
WHITE = (255, 255, 255)
GREEN = (140, 190, 120)

#grid parameters
ROWS = 100
COLUMNS = 100
TILE_SIZE = 20

def draw_background():
    WIN.fill(GREEN)
    WIN.blit(lava_img, (0,0))

def draw_grid():
    for c in range(ROWS+1):
        pygame.draw.line(WIN, WHITE, (0, c * TILE_SIZE), (WIDTH + SIDE_MARGIN, c * TILE_SIZE))
    for c in range(COLUMNS+1):
        pygame.draw.line(WIN, WHITE, (c * TILE_SIZE, 0), (c * TILE_SIZE, HEIGHT + LOWER_MARGIN))

def main():

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_background()
        draw_grid()
        pygame.display.update()

        

        
    pygame.quit()

if __name__ == "__main__":
    main()