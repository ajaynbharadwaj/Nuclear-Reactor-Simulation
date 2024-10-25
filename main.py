import numpy as np
import pygame
import sys
import ctypes
import random

from particles import Atom, Neutron, Water
from rods import ControlRod, Moderator
from globals import *

pygame.init()
ctypes.windll.user32.SetProcessDPIAware()
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reactor Simulation")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

def controlRodInit():
    controlRods = pygame.sprite.Group()
    for i in range(ROD_NUMBER): 
        x = 510 + i * (10 * ATOM_RADIUS + 5 * ATOM_DIST) 
        controlRods.add(ControlRod(x, ROD_WIDTH, SCREEN_HEIGHT))
    return controlRods

def modderatorInit():
    moderators = pygame.sprite.Group()
    for i in range(MODERATOR_NUMBER): 
        x = 360 + i * (10 * ATOM_RADIUS + 5 * ATOM_DIST) 
        moderators.add(Moderator(x, ROD_WIDTH, SCREEN_HEIGHT))
    return moderators

def atomWaterInit(ATOM_GRID_SIZE):
    grid_width = ATOM_GRID_SIZE[1] * (2 * ATOM_RADIUS + ATOM_DIST) - ATOM_DIST
    grid_height = ATOM_GRID_SIZE[0] * (2 * ATOM_RADIUS + ATOM_DIST) - ATOM_DIST
    start_x = (SCREEN_WIDTH - grid_width) // 2
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    atoms = pygame.sprite.Group()
    water = pygame.sprite.Group()

    for row in range(ATOM_GRID_SIZE[0]):
        for col in range(ATOM_GRID_SIZE[1]):
            x = start_x + col * (2 * ATOM_RADIUS + ATOM_DIST)
            y = start_y + row * (2 * ATOM_RADIUS + ATOM_DIST)
            atoms.add(Atom(x,y, ATOM_RADIUS, False))

            water.add(Water(x, y, ATOM_RADIUS))

    return atoms, water

def neutronInit():
    neutrons = pygame.sprite.Group()
    return neutrons

def neutronUpdate():
    for neutron in neutrons:
        neutron.posUpdate()

        screen.blit(neutron.image, neutron.rect.topleft)
    return

def controlRodUpdate():
    for controlRod in controlRods:
        if len(neutrons) < (DESIRED_NEUTRONS + NEUTRON_TH):
            controlRod.move(True)
        elif len(neutrons) > (DESIRED_NEUTRONS + NEUTRON_TH):
            controlRod.move(False)
        screen.blit(controlRod.image, controlRod.rect)
    return        

def moderatorUpdate():
    for moderator in moderators:
        screen.blit(moderator.image, moderator.rect)
    return

def atomUpdate():
    for atom in atoms:

        if atom.element == False:
            if random.random() < P_DECAY:
                createNeutrons(atom.x, atom.y, 1, 1)

            if random.random() < P_URANIUM and atom.element == 0:
                atom.refill()

        screen.blit(atom.image, atom.rect.topleft)
    return

def waterUpdate():
    for block in water:
        block.tempUpdate()
    water.draw(screen)    
    return

def atomNeutronCollisions():
    collided_neutrons = pygame.sprite.groupcollide(neutrons, atoms, False, False)
    for neutron, atom_list in collided_neutrons.items():
        for atom in atom_list:
            if atom.hit(neutron) == 1:
                createNeutrons(atom.x, atom.y, 3, 0)

def waterNeutronCollisions():
    for block in water:
        collided_neutrons = pygame.sprite.spritecollide(block, neutrons, False)
        if collided_neutrons:
            block.temp += TEMP_RAISE
            if block.temp <= TEMP_STEAM:
                for neutron in collided_neutrons:
                    if random.random() < P_WATERABSORB:
                        neutron.kill()
        elif block.temp != 0:
            block.temp -= TEMP_REDUCTION
    return

def rodNeutronCollisions():
    for neutron in neutrons:
        collided_rods = pygame.sprite.spritecollide(neutron, controlRods, False)
        if collided_rods:
            neutron.kill()

def createNeutrons(x,y,n, thermal):
    for _ in range(n):
        neutrons.add(Neutron(x, y, NEUTRON_RADIUS, random.uniform(0,360), NEUTRON_VELOCITY, thermal))

atoms, water = atomWaterInit(ATOM_GRID_SIZE)
neutrons = neutronInit()
controlRods = controlRodInit()
moderators = modderatorInit()

def main():
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(BACKGROUND_COLOR)
        


        waterUpdate()
        atomUpdate()
        neutronUpdate()
        controlRodUpdate()
        moderatorUpdate()
        atomNeutronCollisions()
        waterNeutronCollisions()
        rodNeutronCollisions()



        current_fps = int(clock.get_fps())
        fps_text = font.render(f"FPS: {current_fps}", True, (0, 0, 0))
        screen.blit(fps_text, (10, 10))

        neutrino_count = len(neutrons)
        count_text = font.render(f"Neutrons: {neutrino_count}", True, (0, 0, 0))
        text_rect = count_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(count_text, text_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()