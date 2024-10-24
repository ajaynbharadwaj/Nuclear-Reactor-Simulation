import numpy as np
import pygame
import sys
from particles import *
import ctypes
import math
import random
ctypes.windll.user32.SetProcessDPIAware()

SCREEN_WIDTH, SCREEN_HEIGHT = 2560, 1440
FPS = 144
BACKGROUND_COLOR = (220, 220, 220)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

ATOM_GRID_SIZE, ATOM_DIST, ATOM_RADIUS = (20,40), 20, 15
NEUTRINO_RADIUS = 5


def atom_init(ATOM_GRID_SIZE):
    grid_width = ATOM_GRID_SIZE[1] * (2 * ATOM_RADIUS + ATOM_DIST) - ATOM_DIST
    grid_height = ATOM_GRID_SIZE[0] * (2 * ATOM_RADIUS + ATOM_DIST) - ATOM_DIST
    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    atoms = []

    for row in range(ATOM_GRID_SIZE[0]):
        for col in range(ATOM_GRID_SIZE[1]):
            x = start_x + col * (2 * ATOM_RADIUS + ATOM_DIST)
            y = start_y + row * (2 * ATOM_RADIUS + ATOM_DIST)
            atoms.append(atom(x,y, ATOM_RADIUS, False))

    return atoms

def atomUpdate(atoms):
    for atom in atoms:
        pygame.draw.circle(screen, atom.color, (atom.x, atom.y), atom.radius)
    return

def neutrino_init():
    neutrinos = []
    NUM_NEUTRINOS = 10
    for _ in range(NUM_NEUTRINOS):
        # Random position within screen bounds
        x = random.randint(0 + NEUTRINO_RADIUS, SCREEN_WIDTH - NEUTRINO_RADIUS)
        y = random.randint(0 + NEUTRINO_RADIUS, SCREEN_HEIGHT - NEUTRINO_RADIUS)

        # Random angle between 0 and 360 degrees
        angle = random.uniform(0, 360)

        # Create a new neutrino and add it to the list
        neutrinos.append(neutrino(x, y, NEUTRINO_RADIUS, angle, 2))
    return neutrinos

def neutrinoUpdate(neutrinos):
    for neutrino in neutrinos:
        neutrino.posUpdate()
        pygame.draw.circle(screen, neutrino.color, (neutrino.x, neutrino.y), neutrino.radius)
    return

def check_collision(neutrino, atom):
    # Calculate the distance between the centers of the neutrino and atom
    distance = math.sqrt((neutrino.x - atom.x) ** 2 + (neutrino.y - atom.y) ** 2)
    #distance = np.linalg.norm(np.array((neutrino.x, neutrino.y)) - np.array((atom.x, atom.y)))    
    # If the distance is less than or equal to the sum of their radii, a collision occurs
    if distance <= (neutrino.radius + atom.radius):
        return True
    return False

def handle_collisions(neutrinos, atoms):
    for neutrino in neutrinos:
        for atom in atoms:
            if check_collision(neutrino, atom):
                atom.color = (255, 0, 0)  # Change color to red to indicate collision
                # You can add more behavior here, like removing the atom or bouncing


def main():
    running = True

    atoms = atom_init(ATOM_GRID_SIZE)
    neutrinos = neutrino_init()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)
        


    
        atomUpdate(atoms)
        neutrinoUpdate(neutrinos)
        handle_collisions(neutrinos, atoms)




        current_fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {current_fps}", True, (255, 0, 0))  # Red color for FPS text
        screen.blit(fps_text, (10, 10))  # Display FPS at position (10, 10)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()