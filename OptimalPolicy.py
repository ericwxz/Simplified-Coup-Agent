class OptimalPolicy:
    def __init__(self, game):
        self.game = game

    def choose_move(self, game_state):
        """takes a game state and returns the strategy as defined by the optimal policy"""
        #policy for main actions
            #if you have an assassin:
                #if bins don't indicate other player has contessa:
                    #if you have >3 coins, assassinate 
            #else if opp bin somewhat certain you have a captain or you have a captain:
                #steal
            #else:
                #if you have duke or opp bin somewhat certain you have a duke:
                    #tax
                #elif bins dont indicate other player has duke:
                    #foreign aid
                #else:
                    #income

        #policy for counter actions
        #   counter steal:
            #if you have a captain or opp bins indicate captain:
                #block
        #   counter foreign aid:
            #if you have a duke or opp indicate duke:
                #block
        #   counter assassination:
            #if you have a contessa, always block
            #else, if 

        #policy for challenge
        #   challenge on assassination
            #if you have one card left and no contessa, challenge
            #if you have two cards left and no contessa, challenge
        #   for all else:
            #basic analysis of whether you are sure the opp doesn't have it (bin of 0) and you are very high (bin of 2) on others

        pass