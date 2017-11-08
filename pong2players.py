import pygame
import numpy as np
from pygame.locals import *
from game_objects.TrainingPlayer import TrainPlayer
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
    i = 0
    SCREEN_REDUCE = 16
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Game exited by user")
                exit()

        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #    pressed = 'up'
        # elif keys[pygame.K_s]:
        #    pressed = 'down'
        screen.blit(backg, (0, 0))
        got.update()
        Call.update()
        backgscale = pygame.transform.scale(backg, (SCR_WID, SCR_HEI))
        got.draw(screen)
        Call.draw(screen)
        #print "ball x, y: ", ball.rect.x, ball.rect.y
        player.draw()
        enemy.draw()
        if ball.rect.x <= 200:
            screen_np = (pygame.surfarray.array2d(screen)
                         [SCREEN_REDUCE*2:SCR_WID - SCREEN_REDUCE, :])
            screen_np = np.append(screen_np.flatten(), player.y)
            screen_data.append(screen_np)
        player.movement()
        enemy.movement()
        ball.movement()
        player.scoring(screen_data)
        enemy.scoring(screen_data)

        pygame.display.flip()
        clock.tick(FPS)
        i += 1

if __name__ == "__main__":
    main()
