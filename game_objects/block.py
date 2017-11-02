import pygame
from pygame.locals import *


class Block(pygame.sprite.Sprite):
    image = pygame.Surface((20, 20))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 0
