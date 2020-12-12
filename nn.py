#import argparse
import csv
import random
import math

from Player import TrainingPlayer, PolicyPlayer, ANNPlayer
from OptimalPolicy import optimal_policy
from TwoPlayerCoup import StateQuality, PublicState

import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

class ANNPolicy:
    def __init__(self,game):
        self.game = game 
        self._model = None

    def save(self, filename):
        if self._model == None:
            print("no model loaded or built")
            return 
        self._model.save(filename) 

    def load(self,filename):
        self._model = keras.models.load_model(filename)
    

    

    def train(self, training_episodes):
        #train a nn with #training_episodes simulated games to gather states to train from; subsequently calling save will save the model for later use

        eps = 0.2
        training_interval = 5
        transfer_interval = 20
        batch_size = 50
        gamma = 0.9
        alpha = 0.1

        def set_optimizer(model, alpha):
            ''' Sets the optimizer for the given model to a SGD optimizer with
                the given learning rate.

                model -- a Keras model
                alpha -- a number between 0.0 and 1.0
            '''
            sgd = keras.optimizers.SGD(lr=alpha, decay=1e-6, momentum=0.8, nesterov=True)
            
            model.compile(loss="mse", optimizer=sgd)

        def make_model(game, alpha):
            ''' Returns a Keras model for approximating Q(s, a) values for
                TwoSimpCoup.  The model will have 43 inputs: 10 for the one-hot
                encoding of the agent's cards, 24 for the public state information,
                and 11 inputs for the one-hot representation of the action. The inputs 
                are deceptively large-- there is a lot of one-hot encoding. The
                model will have a single output giving the estimate of the Q
                value.

                game -- the model of the game
                alpha -- the initial learning rate of the model
            '''
            model = keras.models.Sequential()
            model.add(keras.layers.Dense(25, activation='relu', input_dim = 10 + 24 + len(game.combined_playbook)))
            model.add(keras.layers.Dropout(0.1))
            model.add(keras.layers.Dense(1, activation="linear"))
            set_optimizer(model, alpha)
            return model

        def make_policy(model):
            def policy(state,player):
                if state.state_class != StateQuality.LOSINGCARD:
                    return max(enumerate([q(model, state, player, a) for a in self.game.valid_moves(state)]), key=lambda p: p[1])[0]
                else: 
                    return max(enumerate([q(model, state, player, a) for a in range(len(player.cards))]), key=lambda p: p[1])[0]
            return policy 


        #make initial models

        decay = 0.999
        learning = make_model(self.game, 0.1)
        target = make_model(self.game, 0.1)

        


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
        p1 = TrainingPlayer(self.game,0)
        p2 = PolicyPlayer(self.game,1,optimal_policy)

        def selector(q):
            def choose(state):
                if state.state_class == StateQuality.LOSINGCARD:
                    moves = range(len(p1.cards))
                else:
                    moves = self.game.valid_moves(state)
                if random.random() < eps:
                    return random.randrange(0, len(moves))
                else:
                    return max(enumerate([q(state, a) for a in range(len(moves))]), key=lambda p: p[1])[0]
            return choose

        #define q function
        def encode_action(action):
            """One-hot encoding of an action"""
            return (0 if i != action.index-1 else 1 for i in range(11))

        def q(network, state, player, a):
            if state.is_terminal() != -1:
                return 0
            else:
                encoded_state = state.encode()
                encoded_state.append(player.get_encoding())
                vector = np.matrix(state.encode(), encode_action(a))
                return network(vector)[0][0].numpy()

        select = selector(lambda s, a: q(learning, s, p1, a))
        replay = {(2,2):[], (2,1):[], (1,1):[]}
        for e in range(training_episodes):
            self.game.assign_players(p1,p2)
            self.game.new_game()
            pub_state = self.game.curr_state
            while pub_state.is_terminal() == -1:
                #wait until p1 action: execute play as optimal otherwise
                if pub_state.curr_player != 0:
                    if pub_state.state_class == StateQuality.LOSINGCARD:
                        p2_card_lost = p2.choose_card_to_lose(pub_state)
                        self.game.history.append((-1,1,p2_card_lost))
                        pub_state = PublicState(self.game.encode_bins(), pub_state.p1cards,pub_state.p1coins, pub_state.p2cards-1, pub_state.p2coins,pub_state.turn_counter+1,StateQuality.ACTION, 0, []) 
                    else:
                        pub_state = self.game.combined_playbook[p2.make_move(pub_state)].execute(pub_state,self.game.encode_bins,self.game.history)
                    continue 
                
                if pub_state.state_class != StateQuality.LOSINGCARD:
                    #select an action 
                    action = select(pub_state)
                    next_state = self.game.combined_playbook[action].execute(pub_state, self.game.encode_bins, self.game.history)
                    r = (1.0 if next_state.is_terminal() == 0 else -1.0) if next_state.is_terminal != -1 else 0.0
                    
                    encoded_pub_state = pub_state.encode()
                    encoded_pub_state.append(p1.get_encoding())
                    replay[(pub_state.p1cards, pub_state.p2cards)].append([encoded_pub_state, action, next_state, r])
                    pub_state = next_state
                else:
                    #select a card to lose
                    card_to_lose = select(pub_state)
                    self.game.history.append((-1,0,card_to_lose))
                    next_state = PublicState(self.game.encode_bins(), pub_state.p1cards,pub_state.p1coins, pub_state.p2cards-1, pub_state.p2coins,pub_state.turn_counter+1,StateQuality.ACTION, 0, [])
                    r = (1.0 if next_state.is_terminal() == 0 else -1.0) if next_state.is_terminal != -1 else 0.0
                    encoded_pub_state = pub_state.encode()
                    encoded_pub_state.append(p1.get_encoding())
                    replay[(pub_state.p1cards, pub_state.p2cards)].append([encoded_pub_state, card_to_lose, next_state, r])
                    pub_state = next_state

            #sample from replays to train learning
            if (e+1)%training_interval == 0:
                samples = []
                for partition in replay:
                    samples.extend(random.sample(replay[partition],min(len(replay[partition]), batch_size//3)))
                x_train = [encoded_state + encode_action(action) for encoded_state, action in samples]
                y_train = [[max(-1, min(1, r + gamma * max(q(target, next_state, p1, a) for a in range(12))))] for _, _, next_state, r in samples]

                learning.fit(np.matrix(x_train),np.matrix(y_train),epochs=1,batch_size=10)

                lr = alpha*math.pow(decay, e/training_interval)
                set_optimizer(learning, lr)

            #transfer to target
            if (e+1) % transfer_interval == 0:
                value = 1.0 if self.game.simulate(make_policy(learning), optimal_policy) == 0 else -1.0
                target_value = 1.0 if self.game.simulate(make_policy(target), optimal_policy) == 0 else -1.0
                if value > target_value:
                    target.set_weights(learning.get_weights())
        
        self._model = target
                


    

    def get_policy(self):
        def encode_action(action):
            """One-hot encoding of an action"""
            return (0 if i != action.index-1 else 1 for i in range(11))
        def q(network, state, player, a):
            if state.is_terminal() != -1:
                return 0
            else:
                encoded_state = state.encode()
                encoded_state.append(player.get_encoding())
                vector = np.matrix(state.encode(), encode_action(a))
                return network(vector)[0][0].numpy()
        def policy(state,player):
            if state.state_class != StateQuality.LOSINGCARD:
                return max(enumerate([q(self._model, state, player, a) for a in self.game.valid_moves(state)]), key=lambda p: p[1])[0]
            else: 
                return max(enumerate([q(self._model, state, player, a) for a in range(len(player.cards))]), key=lambda p: p[1])[0]
        return policy 

    """ @classmethod
    def add_arguments(self, argparse):
        parser.add_argument("--epochs", action="store", type=int, default=100, help="number of epochs to train for")
        parser.add_argument("--batch", action="store", type=int, default=10, help="training batch size")
        parser.add_argument("--nodes", action="store", type=int, default=300, help="ANN hidden layer size")
        parser.add_argument("--layers", action="store", type=int, default=1, help="number of ANN hidden layers") """

    
