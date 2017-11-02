import pygame
from pygame.locals import *
from game_objects.player import Player
from game_objects.aiplayer import AIPlayer
from game_objects.block import Block
from game_objects.ball import Ball

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
    backgscale = pygame.transform.scale(backg,(SCR_WID, SCR_HEI))

    global player
    player = AIPlayer("player1", screen, SCR_HEI, SCR_WID)

    global enemy
    enemy = Player("player2", screen, SCR_HEI, SCR_WID)

    block = Block()
    got.add(block)

    ball = Ball(screen, SCR_HEI, SCR_WID, player, enemy)
    Call.add(ball)

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
            screen_np = pygame.surfarray.array2d(screen).flatten()
            player.movement(screen_np, i)
            enemy.movement()
            ball.movement()
            player.draw()
            enemy.draw()
            enemy.scoring()
            player.scoring()

            pygame.display.flip()
            clock.tick(FPS)
            i += 1

if __name__ == "__main__":
    main()
