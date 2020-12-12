from TwoPlayerCoup import PublicState,TwoSimpCoup
from Player import PolicyPlayer,RandomPlayer
from OptimalPolicy import optimal_policy
def __main__():
    game = TwoSimpCoup()
    p1 = RandomPlayer(game,0)
    p2 = PolicyPlayer(game, 1, optimal_policy)

    game.setup(p1, p2)
    result = game.play()
    print(result)

if __name__ == '__main__':
    __main__()