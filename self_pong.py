import sys
import numpy as np
import pygame
from pygame.locals import *
from sklearn.externals import joblib
from game_objects.player import Player
from game_objects.AIPlayers import ElasticNetPlayer, Conv2DPlayer
from game_objects.block import Block
from game_objects.ball import Ball

MODELS_PARAMETERS_DIR = 'pong_data/models_parameters/'
x_mean_dir = MODELS_PARAMETERS_DIR + 'x_mean.pkl'
x_mean = joblib.load(x_mean_dir)

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
    try:
        ai_player = sys.argv[1]
    except:
        ai_player = 'linear'

    SCREEN_REDUCE = 16

    global player
    if ai_player == 'conv':
        player = Conv2DPlayer("player1", screen, SCR_HEI, SCR_WID)
    elif ai_player == 'linear':
        player = ElasticNetPlayer("player1", screen, SCR_HEI, SCR_WID)

    global enemy
    enemy = Player("player2", screen, SCR_HEI, SCR_WID)

    block = Block()
    got.add(block)

    ball = Ball(screen, SCR_HEI, SCR_WID, player, enemy)
    Call.add(ball)

    prev_screen_1 = None
    prev_screen_2 = None
    i = 0
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
        screen_np = (pygame.surfarray.array2d(screen)
                     [SCREEN_REDUCE * 2:SCR_WID - SCREEN_REDUCE, :])
        screen_np = screen_np.flatten().reshape(1, -1) - x_mean
        prev_screen_2 = prev_screen_1
        prev_screen_1 = screen_np

        player.draw()
        enemy.draw()
        if i > 2:

            screen_sequence = np.concatenate([prev_screen_2, prev_screen_1,
                                              screen_np], axis=1)

            player.movement(screen_sequence)

        else:
            player.movement(None)
        enemy.movement()
        ball.movement()
        enemy.scoring()
        player.scoring()
        i += 1
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
