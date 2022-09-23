import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image

pygame.init()

#initializing window
#screen_info = pygame.display.Info()
win_pos_x = 500 #screen_info.current_w / 2 - WIDTH / 2
win_pos_y = 500 #screen_info.current_h / 2 - HEIGHT / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_pos_x,win_pos_y)
#os.environ['SDL_VIDEO_CENTERED'] = '1'
WIDTH, HEIGHT = 1300,1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("sneyq")

WHITE = (255, 255, 255)
FPS = 60    



#hero parameters
hero_width = 30
hero_height = 30
x_cord = 200
y_cord = 200
vel = 5

#loading images
hero_image = pygame.image.load(
    os.path.join('images', 'hero.png'))

#initial circuit
NUM_WIRES = 2
qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
qc.x(range(NUM_WIRES // 2))
qc.h(range(NUM_WIRES))
qc.barrier()

#drawing game
def draw_window():
    WIN.fill(WHITE)
    qc.draw('mpl', filename = os.path.join('images', 'circuit.png'))
    circuit = pygame.image.load(
        os.path.join('images', 'circuit.png'))
    WIN.blit(circuit, (0,HEIGHT-circuit.get_height()))
    WIN.blit(hero_image)
    pygame.display.update() 

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
    if keys_pressed[pygame.K_LEFT]: # move in left
        x_cord -= vel
    if keys_pressed[pygame.K_RIGHT]: # move in right
        x_cord += vel
    if keys_pressed[pygame.K_UP]: # move up
        y_cord -= vel
    if keys_pressed[pygame.K_DOWN]: # move down
        y_cord += vel


def main():
    hero = pygame.Rect(x_cord, y_cord, hero_width, hero_height)

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

        
    pygame.quit()

if __name__ == "__main__":
    main()