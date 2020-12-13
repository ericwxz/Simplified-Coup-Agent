import collections
import time
import random 

from TwoPlayerCoup import PublicState, TwoSimpCoup

def selectMove(game,q_table, position):

    pass 

def train(game, trainingtime, q_table):
       
    pass 

def q_learn(game, trainingtime):
    def initLists():
        return [0 for i in range(len(game.combined_playbook))]
    q_table = collections.defaultdict(initLists)
    random.seed()
    train(game, trainingtime, q_table)

    def func(position):
        return #make selection function that gets returned

    return func
