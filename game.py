import pygame
import qiskit
import os
import numpy as np
#import matplotlib #.pyplot as plt
from PIL import Image

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

NUM_WIRES = 2


SNAKE_POSITION = (300, 300)
SNAKE = np.array([SNAKE_POSITION])

qc = qiskit.QuantumCircuit(NUM_WIRES, NUM_WIRES)
qc.x(range(NUM_WIRES // 2))
qc.h(range(NUM_WIRES))
qc.barrier()



def draw_window():
    WIN.fill(WHITE)
    qc.draw('mpl', filename = os.path.join('images', 'circuit.png'))
    circuit = pygame.image.load(
        os.path.join('images', 'circuit.png'))
    WIN.blit(circuit, (0,HEIGHT-circuit.get_height()))
    pygame.display.update() 

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

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        #if keys_pressed[pygame.K_LEFT]: # move in left


        draw_window()

        
    pygame.quit()

if __name__ == "__main__":
    main()