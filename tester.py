from TwoPlayerCoup import PublicState,TwoSimpCoup
from Player import PolicyPlayer,RandomPlayer
from OptimalPolicy import optimal_policy
from qcoup import BasicQPolicy
def __main__():
    print("\nThe test script should be run in an environment with pickle installed. \nCurrently this test script tests the pre-trained q-table saved in \"picklefinal\". \nI\'m using q-learning to play a simplified version of Coup. \nThe instructions to the full game are here in video format: \nhttps://youtu.be/a8bY3zI9FL4 \n\nThe simplified version removes the Ambassador card and limits the game to two players. All other state transitions and game phases are in play. \n\nMy code implements the game and encodes private state information with the public state information in the form of \"certainty bins\" for each player based on the history of actions played since the start of the game, resetting every time a new game is called. It then uses q-learning to train about one hour (about 13000 games to adequately explore the state space) against a vaguely optimal-policy player. Here are my promising results at just an hour of training:\n")

    print("\n...starting test run")
    game = TwoSimpCoup()
    
    qbuilder = BasicQPolicy(game)
    
    
    qpolicy = qbuilder.q_learn(3600)
    qbuilder.save_table('picklefinal')


    #qpolicy = qbuilder.q_learn(300)
    #qbuilder.save_table('pickletest2')
    
    #qpolicy = qbuilder.q_learn(10000)
    
    #qbuilder.load_table("picklefinal")
    #qpolicy = qbuilder.get_policy()
    


    print("...successfully loaded pre-trained table or trained a table from scratch. Check qcoup.py for information on training a new agent.")


    p1= PolicyPlayer(game,0,qpolicy)
    p2= PolicyPlayer(game,1,optimal_policy)
    p3 = RandomPlayer(game,1)
    num_games = 2000
    p1wins = 0.0
    for i in range(num_games):
        game.setup(p1, p2)
        result = game.play()
        if result == 0:
            p1wins+=1.0

    print("success rate against optimal in 2000 games: " + str(p1wins/num_games))
    p1wins = 0.0
    for i in range(num_games):
        game.setup(p1,p3)
        result = game.play()
        if result==0:
            p1wins+=1.0
    print("success rate against random in 2000 games: " + str(p1wins/num_games)+"\n")

    print("The results currently converge around 0.55 against the optimal policy and 0.58 against the random policy. The rate against the random policy is expected given the challenge mechanic and the likelihood of the agent developing a policy that includes a multitude of strategic bluffs.")
    print("\n For more documentation please refer to info.txt")
if __name__ == '__main__':
    __main__()