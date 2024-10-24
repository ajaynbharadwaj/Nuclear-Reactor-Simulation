import numpy as np
import pygame

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

        if self.element:
            self.color = (50,100,200)
        else:
            self.color = (150,150,150)

        self.draw()
        return

    def draw(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        return
    
    def refill(self):
        self.element = True
        self.color = (50,100,200)
        self.draw()
        return

    def hit(self, neutrino):
        if self.element:
            self.color = (150,150,150)
            self.element = False
            neutrino.kill()
            self.draw()
            return True

        else:
            return False

class Neutron(pygame.sprite.Sprite):

    def __init__(self, x, y, radius, angle, velocity):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = radius
        self.angle = angle
        self.velocity = velocity
        self.color = NEUTRON_COLOR

        self.draw()
        return

    def draw(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
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
