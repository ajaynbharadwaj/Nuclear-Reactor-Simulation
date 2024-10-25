import pygame
from globals import *

class ControlRod(pygame.sprite.Sprite):

    def __init__(self, x, width, screen_height):
        super().__init__()
        self.width = width
        self.height = screen_height
        self.rodY = ROD_Y_MIN
        self.x = x
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((50, 50, 50))
        self.rect = self.image.get_rect(topleft=(x, -self.rodY))
        return
    
    def move(self, direction):

        for i in range(510, 2260, 500):
            if self.x == i:
                return

        if direction and self.rodY < ROD_Y_MAX:
            self.rodY += ROD_VELOCITY
        elif not direction and self.rodY > ROD_Y_MIN:
            self.rodY -= ROD_VELOCITY
        self.rect = self.image.get_rect(topleft=(self.x, -self.rodY))
        return
    
class Moderator(pygame.sprite.Sprite):
    def __init__(self, x, width, screen_height):
        super().__init__()
        self.width = width
        self.height = 20*ATOM_DIST + 40*ATOM_RADIUS
        self.x = x
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, 205))

        self.draw()

    def draw(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, (255, 255, 255), (2, 2, self.width - 6, self.height - 6))