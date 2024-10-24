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