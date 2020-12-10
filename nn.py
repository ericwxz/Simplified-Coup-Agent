import argparse
import meta_actions
import csv
import random
import yahtzee

import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

class ANNPolicy:
    def __init__(self,game):
        self.game = game 

    def save(self, filename):
        self._model.save(filename) 

    def load(self,filename):
        self._model = keras.models.load_model(filename)
    

    def train(self, training_episodes, argparse):
        #train a nn with #training_episodes simulated games to gather states to train from

        #make initial models

        #define q function

        #define a function that uses an ANN to return a policy

        #for each episode:
        #   get the history of states from an entire game
        #   for each action made, sparse rewards
        #   put each state into replay database

        #   every so often: train network
        #       get an even distribution from replay database
        #       sample the replays as ANN inputs
        #       compute expected outputs 
        #       traing the ANN
        #       manually decay learning rate
        #   every so often: copy trained to target
        #       if value of simulated game with learning network > value of target network:
        #           set weights of target to the weights of learning

        #def a function that takes a position and returns the a that maximizes the q value using the network
            #ex from glenn's notes: 
            """     def q(network, s, a):
                        if game.game_over(s):
                            # don't need to approximate for terminal positions
                            return 0
                        else:
                            input_vec = np.matrix(encode_state(s) + encode_action(a))
                            return network(input_vec)[0][0].numpy()

                    def make_policy(model):
                        ''' Returns a policy function that uses the given ANN to choose
                            the best action.

                            model -- a Keras model
                        '''
                        def policy(pos):
                            # find a that maximizes Q(s, a)
                            return max(enumerate([q(model, pos, a) for a in range(playbook_size)]), key=lambda p: p[1])[0]
                        return policy """
        #return policy given by the learning model


        pass

    

    def choose_move(self, game_state):
        """takes a game state, feeds it through the NN, and uses the output to select the move as determined by the NN"""

        pass

    @classmethod
    def add_arguments(self, argparse):
        parser.add_argument("--epochs", action="store", type=int, default=100, help="number of epochs to train for")
        parser.add_argument("--batch", action="store", type=int, default=10, help="training batch size")
        parser.add_argument("--nodes", action="store", type=int, default=300, help="ANN hidden layer size")
        parser.add_argument("--layers", action="store", type=int, default=1, help="number of ANN hidden layers")

    
