import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, name, screen, screen_height, screen_width):
        pygame.sprite.Sprite.__init__(self)
        self.SCR_HEI = screen_height
        self.SCR_WID = screen_width
        self.screen = screen
        if name == "player1":
            self.x, self.y = 16, self.SCR_HEI / 2
        elif name == "player2":
            self.x, self.y = self.SCR_WID - 16, self.SCR_HEI / 2
        self.name = name
        self.speed = 6
        self.padWid, self.padHei = 8, 64
        self.score = 0
        self.scoreFont = pygame.font.SysFont("Arial", 32)

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 2:
                print ("player 1 wins!")
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 2:
                print ("Player 2 wins!")
                exit()

    def movement(self):

        keys = pygame.key.get_pressed()
        if self.name == "player1":
            if keys[pygame.K_w]:
                self.y -= self.speed
            elif keys[pygame.K_s]:
                self.y += self.speed
        elif self.name == "player2":
            if keys[pygame.K_UP]:
                self.y -= self.speed
            elif keys[pygame.K_DOWN]:
                self.y += self.speed

        if self.y <= 0:
            self.y = 0
        elif self.y >= self.SCR_HEI - 64:
            self.y = self.SCR_HEI - 64

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.x, self.y, self.padWid, self.padHei))

