import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image
import easygui
import csv

from sympy import Abs

from map_editor import COLUMNS, ROWS

pygame.init()


WIDTH, HEIGHT = 1040,700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sneyq")

#initializing window
#win_pos_x = 500 #screen_info.current_w / 2 - WIDTH / 2
#win_pos_y = 500 #screen_info.current_h / 2 - HEIGHT / 2
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos_x,win_pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '1'

WHITE = (255, 255, 255)
GREEN = (160, 180, 100)
FPS = 60    

scroll_x = 0
scroll_y = 0

COLUMNS = 50
ROWS = 50
TILE_SIZE = 32


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

tiles = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    tiles.append(r)

objects = []
for row in range(ROWS):
    r = [-1] * COLUMNS
    objects.append(r)

#loading images
hero_down = pygame.image.load('images/hero/hero_down.png')
hero_right = pygame.image.load('images/hero/hero_right.png')
hero_left = pygame.image.load('images/hero/hero_left.png')
hero_up = pygame.image.load('images/hero/hero_up.png')
bgd_img = pygame.image.load('images/space.png')

#hero
class character:
    def __init__(self,x, y, height, width, vel, image):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = 5
        self.img = image

hero = character(5, 15, 2, 1, 5, hero_down)

#initial circuit
NUM_WIRES = 2
qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
qc.x(range(NUM_WIRES // 2))
qc.h(range(NUM_WIRES))
qc.barrier()



def load_map():
    scroll_x = 0
    scroll_y = 0
    path = os.path.join('maps')
    file = 'testowa.csv' #easygui.fileopenbox()    
    with open(os.path.join('maps', file), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')   
        for y, row in enumerate(reader):
            for x, tile in enumerate(row):
                if y < ROWS:
                    tiles[y][x] = int(tile)
                else:
                    objects[y-ROWS][x] = int(tile)

#drawing game
#def draw_window():
    #WIN.fill(WHITE)
    #qc.draw('mpl', filename = os.path.join('images', 'circuit.png'))
    #circuit = pygame.image.load(
    #    os.path.join('images', 'circuit.png'))
    #WIN.blit(circuit, (0,HEIGHT-circuit.get_height()))
    #WIN.blit(hero_image)   

def draw_background():
    WIN.fill(GREEN)
    bg_width = bgd_img.get_width()
    bg_height = bgd_img.get_height()
    for x in range(4):
        for y in range(4):
            WIN.blit(bgd_img, ((x * bg_width) - scroll_x,(y * bg_height) - scroll_y))

def draw_map():
    for i, row in enumerate(tiles):
        for j, tile in enumerate(row):
            if tile >= 0:
                WIN.blit(img_list[tile], (j * TILE_SIZE - scroll_x, i * TILE_SIZE - scroll_y))
    for i, row2 in enumerate(objects):
        for j, tile in enumerate(row2):
            if tile >= 0:
                WIN.blit(obj_list[tile-TILE_TYPES], (j * TILE_SIZE - scroll_x, i * TILE_SIZE - scroll_y))

#applying quantum gates on circuit
def apply_gate(gate, wires):
    # print(gate, wires)
    if gate == "H":
        qc.h(wires[0])
    elif gate == "X":
        qc.x(wires[0])
    elif gate == "Y":
        qc.y(wires[0])
    elif gate == "Z":
        qc.z(wires[0])
    elif gate == "S":
        qc.s(wires[0])
    elif gate == "T":
        qc.t(wires[0])
    elif gate == "CX":
        qc.cnot(wires[1], wires[0])
    elif gate == "CCX":
        qc.toffoli(wires[2], wires[1], wires[0])



#handling hero's movement
def hero_move(keys_pressed, hero):
    if keys_pressed[pygame.K_LEFT] and hero.x > 0:
        if objects[hero.y + 1][hero.x - 1] == -1: # move in left
            hero.x -= 1 #hero.vel
            hero.img = hero_left
    if keys_pressed[pygame.K_RIGHT] and (hero.x + hero.width < COLUMNS -1):
        if objects[hero.y + 1][hero.x + hero.width] == -1: # move in right
            hero.x += 1 #hero.vel
            hero.img = hero_right
    if keys_pressed[pygame.K_UP] and (hero.y > 0):
        if (objects[hero.y][hero.x] == -1): # move up
            hero.y -= 1 #hero.vel
            hero.img = hero_up
    if keys_pressed[pygame.K_DOWN] and (hero.y + hero.height < ROWS - 1):
        if (objects[hero.y + hero.height][hero.x] == -1): # move down
            hero.y += 1 #hero.vel
            hero.img = hero_down


def main():
    #hero = pygame.Rect(x_cord, y_cord, hero_width, hero_height)
    load_map()

    clock = pygame.time.Clock()
    time = 0
    run = True

    while run:
        clock.tick(FPS)
        time = (time + 1) % FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        if time % 10 == 0:
            hero_move(keys_pressed, hero)
        

        #draw_window()
        draw_background()
        draw_map()
        WIN.blit(hero.img, (hero.x * TILE_SIZE, hero.y * TILE_SIZE))

        pygame.display.update()

        
    pygame.quit()

if __name__ == "__main__":
    main()