
from TwoPlayerCoup import StateQuality

def optimal_policy(game_state, cards, player, is_lose):
    cardtypes = {0:"Duke", 1:"Assassin", 2:"Captain", 3:"Contessa"}
    movetype = {1: "self.IncomeMove()", 2: "self.ForeignAidMove()", 3: "self.CoupMove()", 4: "self.TaxMove()", 5: "self.AssassinateMove()", 6: "self.StealMove()", 7: "self.CounterForeignAidMove()", 8: "self.CounterStealMove()", 9: "self.CounterAssassinMove()", 10: "self.ChallengeMove(self.associations)", 11: "self.AllowMove()"}
    associations = {1:None, 2:None, 3:None, 4:0, 5:1, 6:2, 7:3, 8:2, 9:3, 10:None, 11:None}
    """takes a game state and returns the strategy as defined by the optimal policy"""
    
    if is_lose:
        if game_state.bins[(player + 1)%2][1] < 0.5 and 3 in cards:
            return cards.index(3)
        elif 2 in cards:
            return cards.index(2) 
        elif 3 in cards: 
            return cards.index(3)
        elif 1 in cards:
            return cards.index(1) 
        else:
            if len(cards) == 1:
                return 0
            return cards.index(0)
            
    
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

    num_cards = len(cards)
    if player == 0:
        personal_coins = game_state.p1coins 
    else:
        personal_coins = game_state.p2coins
    
    if personal_coins >= 10:
        return 3

    if game_state.state_class== StateQuality.ACTION:
        if 1 in cards:
            if game_state.bins[(player+1)%2][3] < 1 and personal_coins > 3:
                return 5
        elif (game_state.bins[player][2] > 0 or 2 in cards) and game_state.bins[(player+1)%2][2] < 1:
            return 6
        else: 
            if 0 in cards or game_state.bins[player][0] > 0.4:
                return 4
            elif game_state.bins[(player+1)%2][0] < 0.2:
                return 2
            else:
                return 1


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
    elif game_state.state_class == StateQuality.COUNTER:
        last_move = game_state.movestack[len(game_state.movestack)-1]
        if last_move[0] == 6:
            if 2 in cards or game_state.bins[player][2] > 0.4:
                return 8
            else:
                return 11 
        if last_move[0] == 2:
            if 0 in cards or game_state.bins[player][0] > 0.4:
                return 7
            else:
                return 11 
        if last_move[0] == 5:
            if 3 in cards or game_state.bins[player][3] > 0.9:
                return 9
            elif game_state.bins[player][3] > 0.4 and num_cards == 1: 
                return 9
            else:
                return 11
    #policy for challenge
    #   challenge on assassination
        #if you have one card left and no contessa, challenge
        #if you have two cards left and no contessa, challenge
    #   for all else:
        #basic analysis of whether you are sure the opp doesn't have it (bin of 0) and you are very high (bin of 1) on others
    elif game_state.state_class == StateQuality.CHALLENGEACTION or game_state.state_class == StateQuality.CHALLENGECOUNTER:
        if len(game_state.movestack) == 0:
            return 11
        last_move = game_state.movestack[len(game_state.movestack)-1]
        if last_move[0] ==5:
            if len(cards) == 1 and 3 not in cards:
                return 10 
            else: 
                return 11 
        else:
            num_certain_cards = 0
            for i in game_state.bins[(player+1)%2]:
                if i > 0.9:
                    num_certain_cards +=1
            if associations[last_move[0]] == None:
                return 11
            if game_state.bins[(player+1)%2][associations[last_move[0]]] == 0 and 3 >= num_certain_cards > 1:
                return 10 
            else: 
                return 11
    else: 
        if game_state.bins[(player + 1)%2][1] < 0.5 and 3 in cards:
            if cards.index(3) == 0:
                return 12
            else:
                return 13
        elif 2 in cards:
            if cards.index(2) == 0:
                return 12
            else:
                return 13
        elif 3 in cards: 
            if cards.index(3) == 0:
                return 12
            else:
                return 13
        elif 1 in cards:
            if cards.index(1) == 0:
                return 12
            else:
                return 13 
        else:
            if len(cards) == 1:
                return 12
            return 12
    
