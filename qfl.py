import collections
import time
import random 


def superpos(position):
    remaining_yards = position[0]
    downs_left = position[1]
    yards_to_reset = position[2]
    ticks_left = position[3]
    s1 = -1
    s2 = -1
    if ticks_left == 0:
        s1 = float('inf')
    else:
        s1 = 0.5 * round(remaining_yards/ticks_left/0.5)
    if downs_left == 0:
        s2 = float('inf')
    else:
        s2 = 0.5 * round(yards_to_reset/downs_left/0.5)

    return (s1 , s2)

def selectMove(model,q_table,position):
    sup = superpos(position)
    ep = 0.2
    res = random.randint(0,9)
    if res < ep*10:
        return random.randint(0,model.offensive_playbook_size()-1)
    else:
        return bestSupMove(model,q_table,sup)
    

def train(model, trainingtime, q_table):
    start = time.time()
    learning_rate = 0.1
    time_discount = 1
    while time.time()-start < trainingtime - 0.005:
        #playthrough to end
        currpos = model.initial_position()
        while not model.game_over(currpos):
            #select a move
            play = selectMove(model,q_table,currpos)
            #evaluate the result and check if win
            newpos, outcome = model.result(currpos, play)
            if model.game_over(newpos) == True and model.win(newpos) == True:
                win = 1
            else:
                win = 0
            #update q_table with linear approximator or direct q-value eqn
            sup_curr = superpos(currpos)
            sup_next = superpos(newpos)
            next_play= bestSupMove(model, q_table, sup_next)
            q_table[sup_curr][play] += learning_rate * (win +(time_discount * q_table[sup_next][next_play]) - q_table[sup_curr][play])
            #decr the learning rate
            if learning_rate > 0.01:
                learning_rate -= 0.001
            currpos = newpos
            
        


def bestSupMove(model,q_table,suppos):
    best = 0
    currmax = -10
    for i in range(model.offensive_playbook_size()):
        if q_table[suppos][i] > currmax:
            best = i 
            currmax = q_table[suppos][i]
    return best

def initLists(model):
    return [0 for i in range(model.offensive_playbook_size())]


def q_learn(model, trainingtime):
    def initLists():
        return [0 for i in range(model.offensive_playbook_size())]
    q_table = collections.defaultdict(initLists)
    random.seed()
    train(model, trainingtime, q_table)

    def func(position):
        return bestSupMove(model,q_table,superpos(position))

    return func