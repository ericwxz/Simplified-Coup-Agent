import collections
import time
import random 
import csv
import pandas as pd 

from TwoPlayerCoup import PublicState, TwoSimpCoup
from Player import PolicyPlayer
from OptimalPolicy import optimal_policy


class BasicQPolicy:
    def __init__(self, game):
        self.game = game
        self.qtable = None 

    def selectMove(self,q_table, state):
        """state should not be encoded"""
        valid_moves = self.game.valid_moves(state)
        ep = 0.2
        res = random.randint(0,9)
        if res < ep*10:
            return valid_moves[random.randint(0,len(valid_moves)-1)]
        else:
            return self.bestMove(q_table,state, valid_moves) 

    def bestMove(self,q_table, state, valid_moves):
        encoded_state= tuple(self.game.bin_encoded_state(self.game.encode_full_state(state)))
        best = 0
        currmax = -10
        for i in range(len(valid_moves)):
            if q_table[encoded_state][valid_moves[i]] > currmax:
                best = i
                currmax = q_table[encoded_state][valid_moves[i]]
        return valid_moves[best]

    def train(self, trainingtime, q_table):
        e = 0
        start = time.time()
        learning_rate = 0.1
        time_discount = 1
        p1 = PolicyPlayer(self.game,0,optimal_policy)
        p2 = PolicyPlayer(self.game,1,optimal_policy)
        while time.time() - start < trainingtime:
            #init game
            e += 1
            self.game.setup(p1,p2)
            self.game.new_game()
            currstate = self.game.curr_state
            #playthrough to end
            while currstate.is_terminal() == -1:
                play = self.selectMove(q_table, currstate)
                #evaluate the result and see if it's a win
                newstate = self.game.combined_playbook[play].execute(currstate,self.game.encode_bins,self.game.history)
                res = newstate.is_terminal()
                if res == 0:
                    win = 1
                else:
                    win = 0
                encoded_next = self.game.encode_full_state(newstate)
                #check if need to undo card loss for encoding purposes
                if play == 12 or play==13:
                    self.game.p1cards.append(self.game.p1deadcards.pop())
                    encoded_curr = self.game.encode_full_state(currstate)
                    self.game.p1deadcards.append(self.game.p1cards.pop())
                else:
                    encoded_curr = self.game.encode_full_state(currstate)
                next_play = self.bestMove(q_table,newstate,self.game.valid_moves(newstate))
                q_table[encoded_curr][play] += learning_rate * (win + (time_discount * q_table[encoded_next][next_play] - q_table[encoded_curr][play]) )
                #decr learning rate
                if learning_rate > 0.01:
                    learning_rate -=0.0001
                currstate = newstate


        print("trained using data from " + str(e) + " games")
        return 

    def q_learn(self, trainingtime):
        """Creates a q-table in self.qtable; trains for trainingtime; and returns the policy. the table must be saved"""
        def initLists():
            return [0 for i in range(len(self.game.combined_playbook))]
        q_table = collections.defaultdict(initLists)
        random.seed()
        self.train(trainingtime, q_table)

        self.q_table = q_table
        game = self.game
        def func(state):
            encoded_state= tuple(game.bin_encoded_state(game.encode_full_state(state)))
            best = 0
            currmax = -10
            valid_moves = game.valid_moves(state)
            for i in range(len(valid_moves)):
                if q_table[encoded_state][valid_moves[i]] > currmax:
                    best = i
                    currmax = q_table[encoded_state][valid_moves[i]]
            return valid_moves[best] 

        return func

    def save_table(self, filename = None):
        if self.qtable != None:
            if filename == None:
                filename = "save.csv"
            df = pd.DataFrame(self.qtable)
            df.to_csv(filename,encoding='utf-8', index=False)
        else:
            print("error: no qtable trained or loaded")
         

    def load_table(self, filename):
        df = pd.read_csv(filename)
        self.q_table = df.to_dict()
