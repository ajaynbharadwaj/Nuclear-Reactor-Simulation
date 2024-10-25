import numpy as np
import pygame
import random

from globals import *

class Atom(pygame.sprite.Sprite):
    
    def __init__(self, x, y, radius, element):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.element = element
        self.x = x
        self.y = y
        self.source = (x,y)

        if self.element == 0:
            self.color = (150,150,150)
        elif self.element == 1:
            self.color = (50,100,200)
        elif self.element == 2:
            self.color = (50,50,50)

        self.draw()
        return

    def draw(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        return
    
    def refill(self):
        self.element = 1
        self.color = (50,100,200)
        self.draw()
        return

    def hit(self, neutrino):
        if self.element == 1:
            if random.random() < P_XENON:
                self.element = 2
                self.color = (50,50,50)
            else:
                self.element = 0
                self.color = (150,150,150)
            neutrino.kill()
            self.draw()
            return True
        elif self.element == 2 and neutrino.source != self.source:
            self.color = (150,150,150)
            self.element = 0
            neutrino.kill()
            self.draw()
            return False
        else:
            return False

class Neutron(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, angle, velocity, thermal):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.angle = angle
        self.color = NEUTRON_COLOR
        self.source = (x,y)
        self.thermal = thermal
        if self.thermal:
            self.velocity = velocity
        else:
            self.velocity = velocity * NEUTRON_VELOCITY_NONTHERMAL

        self.draw()
        return

    def draw(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        if self.thermal == 0:
            pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius - 3)
        return

    def posUpdate(self):
        self.rect.x += self.velocity * np.cos(np.deg2rad(self.angle))
        self.rect.y += self.velocity * np.sin(np.deg2rad(self.angle))

        if self.rect.x < (-self.radius*2 + KILL_BUFFER) or self.rect.x > (SCREEN_WIDTH + self.radius*2 - KILL_BUFFER):
            self.kill()
        if self.rect.y < (-self.radius*2 + KILL_BUFFER) or self.rect.y > (SCREEN_HEIGHT + self.radius*2 - KILL_BUFFER):
            self.kill()
        return

class Water(pygame.sprite.Sprite):

    def __init__(self, x, y, radius):
        super().__init__()
        self.size = 3 * radius
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill((150, 180, 200))
        self.rect = self.image.get_rect(center=(x, y))
        self.temp = int(0)
        return

    def tempUpdate(self):
        if self.temp <= TEMP_STEAM:
            self.image.fill((150+min(self.temp*TEMP_COLORFACTOR, 255-150),180-self.temp*TEMP_COLORFACTOR,200-self.temp*TEMP_COLORFACTOR))
        else:
            self.image.fill(BACKGROUND_COLOR)
        return
