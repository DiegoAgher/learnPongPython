import pygame
import numpy as np
from pygame.locals import *
from game_objects.player import Player
from game_objects.training_player import TrainPlayer
from game_objects.ball import Ball
from game_objects.block import Block

SCR_WID, SCR_HEI = 400, 400
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 30
pygame.init()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GOLD = (201, 168, 168)
Call = pygame.sprite.Group(())
got = pygame.sprite.Group(())
backg = pygame.Surface((SCR_WID, SCR_HEI))


def main():
    backgscale = pygame.transform.scale(backg, (SCR_WID, SCR_HEI))

    global player
    player = TrainPlayer("player1", screen, SCR_HEI, SCR_WID)

    global enemy
    enemy = TrainPlayer("player2", screen, SCR_HEI, SCR_WID)

    block = Block()
    got.add(block)

    ball = Ball(screen, SCR_HEI, SCR_WID, player, enemy)
    Call.add(ball)

    screen_data = []
    while True:

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            print("Game exited by user")
                            exit()

            screen.blit(backg, (0, 0))
            got.update()
            Call.update()
            backgscale = pygame.transform.scale(backg, (SCR_WID, SCR_HEI))
            got.draw(screen)
            Call.draw(screen)
            player.movement()
            enemy.movement()
            ball.movement()

            player.draw()
            screen_np = pygame.surfarray.array2d(screen).flatten()                                                                                                           
            screen_np = np.append(screen_np, player.y)                                                                                                                       
            screen_data.append(screen_np)
            player.scoring(screen_data)

            enemy.draw()
            screen_np = pygame.surfarray.array2d(screen).flatten()                                                                                                           
            screen_np = np.append(screen_np, player.y)                                                                                                                       
            screen_data.append(screen_np)
            enemy.scoring(screen_data)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
