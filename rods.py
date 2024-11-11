import pygame
from globals import *

class ControlRod(pygame.sprite.Sprite):

    def __init__(self, x, n):
        super().__init__()
        self.n = n
        self.x = x
        self.distance = 0
        self.image = pygame.Surface((ROD_WIDTH, SCREEN_HEIGHT))
        self.image.fill(ROD_COLOR)

        if self.n % 2:
            self.y = ROD_TOP
        else:
            self.y = -ROD_BOT
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return
    
    def move(self, remove):
        if (self.distance + remove * ROD_VELOCITY) >= 0 and (self.distance + remove * ROD_VELOCITY) <=  MAX_ROD_DIST:
            self.distance += remove * ROD_VELOCITY
        if self.n % 2:
            self.rect = self.image.get_rect(topleft=(self.x, self.y+self.distance))
        else:
            self.rect = self.image.get_rect(topleft=(self.x, self.y-self.distance))
        return
    
class Moderator(pygame.sprite.Sprite):
    def __init__(self, x, width):
        super().__init__()
        self.width = ROD_WIDTH
        self.height = 20*ATOM_DIST + 40*ATOM_RADIUS - 5
        self.x = x
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, ROD_TOP))

        self.draw()

    def draw(self):
        pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, (255, 255, 255), (2, 2, self.width - 5, self.height - 5))