from TwoPlayerCoup import PublicState,TwoSimpCoup
from Player import PolicyPlayer,RandomPlayer
from OptimalPolicy import optimal_policy

game = TwoSimpCoup()
p1= PolicyPlayer(game,0,optimal_policy)
p2= PolicyPlayer(game,1,optimal_policy)
game.setup(p1, p2)
print(game.curr_state.encode())