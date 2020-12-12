from TwoPlayerCoup import PublicState,TwoSimpCoup
from Player import PolicyPlayer,RandomPlayer
from OptimalPolicy import optimal_policy
from nn import ANNPolicy
def __main__():
    game = TwoSimpCoup()
    nnp = ANNPolicy(game)
    nnp.train(100)
    nnp.save("model")
    nnpolicy = nnp.get_policy()

    p1= PolicyPlayer(game,0,nnpolicy)
    p2= PolicyPlayer(game,1,optimal_policy)
    p1wins = 0.0
    for i in range(100):
        game.setup(p1, p2)
        result = game.play()
        if result == 0:
            p1wins+=1.0

    print(p1wins/100.0)

if __name__ == '__main__':
    __main__()