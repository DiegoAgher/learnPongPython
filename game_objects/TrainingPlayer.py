import numpy as np
import h5py
import pygame
from pygame.locals import *
from datetime import datetime
from game_objects.player import Player


class TrainPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)

    def scoring(self, screen_data):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 5:
                print ("player 1 wins!")
                training_id = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
                training_id = training_id.strip().replace(" ", "")
                data_file = (h5py.File("pong_data/training_data/{}.h5".
                                       format(training_id)))
                dataset = (data_file.
                           create_dataset(
                            'train_{}'.format(training_id),
                            (len(screen_data), screen_data[0].shape[0]),
                            dtype='f'))
                for index, vector in enumerate(screen_data):
                    dataset[index] = vector

                data_file.close()
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 5:
                print ("Player 2 wins!")
                training_id = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
                training_id = training_id.strip().replace(" ", "")
                data_file = (h5py.File("pong_data/training_data/{}.h5".
                                       format(training_id)))
                dataset = (data_file.
                           create_dataset(
                            'train_{}'.format(training_id),
                            (len(screen_data), screen_data[0].shape[0]),
                            dtype='f'))
                for index, vector in enumerate(screen_data):
                    dataset[index] = vector

                data_file.close()
                exit()
