import pygame
import numpy as np
from pygame.locals import *
from sklearn.externals import joblib
from keras.models import load_model
from game_objects.player import Player

MODELS_PARAMETERS_DIR = 'pong_data/models_parameters/'
x_mean_dir = MODELS_PARAMETERS_DIR + 'x_mean.pkl'
y_mean_dir = MODELS_PARAMETERS_DIR + 'y_mean.pkl'


class ElasticNetPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)
        try:
            self.predictive_model = joblib.load('ElasticNetSeq.pkl')
            self.y_mean = joblib.load(y_mean_dir)
            self.x_mean = joblib.load(x_mean_dir)
        except Exception as e:
            print Exception
            print "Models or parameters above not found, train the model first"
            print """To train the model use pong2players.py script to gather
                  data and then train the model with one of the training
                  scripts, eg: training/elasticnet.py"""

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 5:
                print ("player 1 wins!")
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 5:
                print ("Player 2 wins!")
                exit()

    def movement(self, screen_np):
        if screen_np is not None:
            model = self.predictive_model
            prediction = model.predict(screen_np)
            self.y = prediction + self.y_mean
            print(self.y)


class Conv2DPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)
        try:
            self.predictive_model = load_model('pong_conv2d.h5')
            self.y_mean = joblib.load(y_mean_dir)
            self.x_mean = joblib.load(x_mean_dir)
        except Exception as e:
            print Exception
            print "Models or parameters above not found, train the model first"
            print """To train the model use pong2players.py script to gather
                  data and then train the model with one of the training
                  scripts, eg: training/elasticnet.py"""

    def movement(self, screen_np):
        if screen_np is not None:
            frame_length = screen_np.shape[1]
            centered_data = np.reshape(screen_np, (1, frame_length / (400 * 3),
                                                   400, 3))
            model = self.predictive_model
            prediction = model.predict(centered_data)
            self.y = prediction + self.y_mean
