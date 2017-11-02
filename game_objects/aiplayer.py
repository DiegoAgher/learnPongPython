import pygame
from pygame.locals import *
from sklearn.externals import joblib
from game_objects.player import Player


class AIPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        pygame.sprite.Sprite.__init__(self)
        Player.__init__(self, name, screen, screen_height, screen_width)
        self.predictive_model = joblib.load('ElasticNet.pkl')
        self.y_mean = joblib.load('ymean.pkl')
        self.x_mean = joblib.load('x_mean.pkl')

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

    def movement(self, screen_np, counter):
        if counter < 20:
            self.y = self.y
        else:
            model = self.predictive_model
            centered_data = (screen_np - self.x_mean).reshape(1, -1)
            prediction = model.predict(centered_data)
            print("centered", centered_data.mean())
            self.y = prediction + self.y_mean
            print(self.y)
