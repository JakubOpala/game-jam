import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image
import easygui
import csv

from map_editor import COLUMNS, ROWS

pygame.init()

#initializing window
win_pos_x = 500 #screen_info.current_w / 2 - WIDTH / 2
win_pos_y = 500 #screen_info.current_h / 2 - HEIGHT / 2
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos_x,win_pos_y)
os.environ['SDL_VIDEO_CENTERED'] = '1'

WIDTH, HEIGHT = 1040,700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sneyq")


WHITE = (255, 255, 255)
GREEN = (160, 180, 100)
FPS = 60    

scroll_x = 0
scroll_y = 0


#hero parameters
hero_width = 30
hero_height = 30
x_cord = 200
y_cord = 200
vel = 5

#loading images
hero_img = pygame.image.load('images/hero.png')
lava_img = pygame.image.load('images/lava.png')


#initial circuit
NUM_WIRES = 2
qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
qc.x(range(NUM_WIRES // 2))
qc.h(range(NUM_WIRES))
qc.barrier()

COLUMNS = 50
ROWS = 50
TILE_SIZE = 40


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

def load_map():
    scroll_x = 0
    scroll_y = 0
    path = os.path.join('maps')
    file = 'new_map1.csv' #easygui.fileopenbox()    
    with open(os.path.join('maps', file), 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter = ';')   
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                if x < ROWS:
                    tiles[x][y] = int(tile)
                else:
                    objects[x-COLUMNS][y-ROWS] = int(tile)

#drawing game
def draw_window():
    WIN.fill(WHITE)
    qc.draw('mpl', filename = os.path.join('images', 'circuit.png'))
    circuit = pygame.image.load(
        os.path.join('images', 'circuit.png'))
    WIN.blit(circuit, (0,HEIGHT-circuit.get_height()))
    #WIN.blit(hero_image)

def draw_background():
    WIN.fill(GREEN)
    bg_width = lava_img.get_width()
    bg_height = lava_img.get_height()
    for x in range(4):
        for y in range(4):
            WIN.blit(lava_img, ((x * bg_width) - scroll_x,(y * bg_height) - scroll_y))

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
def hero_move(keys_pressed):
    if keys_pressed[pygame.K_LEFT] and x_cord > 0 and objects[x_cord // TILE_SIZE - 1, y_cord // TILE_SIZE] == -1: # move in left
        x_cord -= vel
    if keys_pressed[pygame.K_RIGHT] and x_cord + hero_width < TILE_SIZE * COLUMNS and objects[(x_cord+hero_width) // TILE_SIZE + 1, y_cord // TILE_SIZE] == -1: # move in right
        x_cord += vel
    if keys_pressed[pygame.K_UP] and y_cord > 0 and objects[x_cord // TILE_SIZE, y_cord // TILE_SIZE - 1] == -1: # move up
        y_cord -= vel
    if keys_pressed[pygame.K_DOWN] and y_cord + hero_height < TILE_SIZE * ROWS and objects[x_cord // TILE_SIZE, (y_cord+hero_height) // TILE_SIZE + 1] == -1: # move down
        y_cord += vel


def main():
    #hero = pygame.Rect(x_cord, y_cord, hero_width, hero_height)
    load_map()

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        hero_move(keys_pressed)
        

        draw_window()
        draw_background()
        draw_map()
        WIN.blit(hero_img, (x_cord, y_cord))

        pygame.display.update()

        
    pygame.quit()

if __name__ == "__main__":
    main()