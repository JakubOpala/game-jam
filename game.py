import pygame
import qiskit
import os
import numpy as np
import matplotlib

WIDTH, HEIGHT = 900,500
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
    WIN.blit(qc.qiskit.draw('mpl'), (0,300))
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