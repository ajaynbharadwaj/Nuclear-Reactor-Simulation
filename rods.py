import pygame
from globals import *

class ControlRod(pygame.sprite.Sprite):

    def __init__(self, x, n):
        super().__init__()
        self.n = n
        self.x = x
        self.image = pygame.Surface((ROD_WIDTH, SCREEN_HEIGHT))
        self.image.fill(ROD_COLOR)

        if self.n % 2:
            self.y = ROD_TOP + 2 * ROD_VELOCITY
        else:
            self.y = -ROD_BOT - 2 * ROD_VELOCITY
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        return
    
    def move(self, remove):
        if self.n % 2:
            if self.y <= (SCREEN_HEIGHT-ROD_BOT - ROD_VELOCITY) and self.y >= ROD_TOP:
                self.y += ROD_VELOCITY * remove
        else:
            if self.y >= -(SCREEN_HEIGHT-ROD_TOP + ROD_VELOCITY) and self.y <= -ROD_BOT:
                self.y -= ROD_VELOCITY * remove


        self.rect = self.image.get_rect(topleft=(self.x, self.y))
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