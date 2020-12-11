import random
class StateQuality:
        ACTION = 0
        CHALLENGEACTION = 1
        COUNTER = 2
        CHALLENGECOUNTER = 3
        LOSINGCARD = 4

class TwoSimpCoup:

    #1) set up players and call assign_players
    #2) set up new game state 
    #3) assign the agent states to each player
    #4) play
    #5) if new game with same player types, simply call new_game and reassign states 
        #if new player types, start from step 1

    def __init__(self):
        self.cardtypes = {0:"Duke", 1:"Assassin", 2:"Captain", 3:"Contessa"}
        self.cardactions = {0: [self.TaxMove()], 1:[self.AssassinateMove()], 2:[self.StealMove()], 3:[self.IncomeMove(), self.ForeignAidMove(),self.CoupMove()]}
        self.cardcounters = {"Duke":[self.CounterForeignAidMove()], "Captain":[self.CounterStealMove()],"Contessa":[self.CounterAssassinMove()],"All":[]}
        self.associations = {1:None, 2:None, 3:None, 4:0, 5:1, 6:2, 7:3, 8:2, 9:3, 10:None, 11:None}
        self.counter_playbook_size = 3
        self.main_playbook_size = 6
        self.num_cards = 4
        self.card_dupes = 3
        self.history = [] #history of (action, player)

    def assign_players(self, p1obj, p2obj):
        self.p1 = p1obj 
        self.p2 = p2obj

    def encode_action(self,  action):
        """One-hot encoding of an action"""
        return (0 if i != action.index else 1 for i in range(self.counter_playbook_size + self.main_playbook_size + 1))

    def encode_card(self, card_index):
        return (0 if i != card_index else 1 for i in range(self.num_cards))

    def encode_bins(self):
        if len(self.history) < 3:
            return ((0,0,0,0),(0,0,0,0))
        p1_bins = [0 for i in range(self.num_cards)]
        p2_bins = [0 for i in range (self.num_cards)]
        for action_player in self.history:
            if self.associations[action_player[0].index] != None:
                if action_player[1] == 0:
                    p1_bins[action_player[0].index] += 1
                else:
                    p2_bins[action_player[0].index] += 1
        
        #calculate certainty: 0 for unlikely, 0.5 for unclear, 1 for likely
        p1_total = sum(p1_bins)
        p2_total = sum(p2_bins)
        for i in range(self.num_cards):
            if p1_bins[i] > p1_total//3:
                p1_bins[i] = 1
            elif p1_bins[i] < p1_total//6:
                p1_bins[i] = 0
            else:
                p1_bins[i] = 0.5 

            if p2_bins[i] > p2_total//3:
                p2_bins[i] = 1
            elif p2_bins[i] < p1_total//6:
                p2_bins[i] = 0
            else:
                p2_bins[i] = 0.5 
        return (tuple(p1_bins), tuple(p2_bins))
        


        #return (p1(certainty bins),p2(certainty))

    #for testing against random/optimal
    def simulate_play(self, policy1, policy2):
        """starts a new game and returns 1 if policy1 wins and 2 if policy2 wins"""
        pass

    def simple_opponent(self, state):
        """returns the move as an integer made by an opponent after simulating perfect-information optimal play """
        #config new set of possible opponent moves and possible curr moves based on bins
        #run minimax on new, very limited set of actions/states
            # no bins, just num cards and num coins in state: much smaller space

        pass

    def valid_moves(self, state, player):
        """"""
        if state.turn_counter %2 != player: 
            return [] 
        
        if state.state_class == StateQuality.ACTION:
            return range(self.main_playbook_size)
        
        if state.state_class == StateQuality.CHALLENGEACTION:
            return [10,11]
        
        if state.state_class == StateQuality.COUNTER:
            return range(self.counter_playbook_size)
        
        if state.state_class == StateQuality.CHALLENGECOUNTER:
            return [10,11]

        return None


    def new_game(self):
        """returns the initial public state and randomly selected private states; resets history"""
        deck = [0,0,0,1,1,1,2,2,2,3,3,3]
        p1deck = []
        p2deck = []
        p1deck.append(deck.pop(random.randrange(len(deck))))
        p1deck.append(deck.pop(random.randrange(len(deck))))
        p2deck.append(deck.pop(random.randrange(len(deck))))
        p2deck.append(deck.pop(random.randrange(len(deck))))
        ret_vals = [PublicState([],2,2,2,2,0,StateQuality.ACTION, 0, [])] #public state, p1state, p2state
        ret_vals.append(AgentState(self.encode_card(p1deck[0]), self.encode_card(p1deck[1])))
        ret_vals.append(AgentState(self.encode_card(p2deck[0]), self.encode_card(p2deck[1])))
        return ret_vals
        

    def play_human(self, policy):
        """simulates a game between a human player and an AI player according to a given policy"""
        pass


    


    #interface for move classes
    class BaseMove:
        def __init__(self, game):
            pass 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state):
            pass

    class TaxMove:
        def __init__(self):
            self.index =4
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins+3,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(),(player+1)%0,[self])
            else:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+3,curr_state.turn_counter, curr_state.next_quality(),(player+1)%0,[self])

    class AssassinateMove:
        def __init__(self):
            self.index = 5 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self,player))
            if player== 0:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(), (player+1)%0,[self]) 

    class StealMove:
        def __init__(self):
            self.index = 6 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self.index,player))
            if player == 0:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins+2,curr_state.p2cards,curr_state.p2coins-2,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self])
            else:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins-2,curr_state.p2cards,curr_state.p2coins+2,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self]) 

    class IncomeMove:
        def __init__(self):
            self.index = 1
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins+1,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, StateQuality.ACTION,(player+1)%0,[self])
            else:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+1,curr_state.turn_counter, StateQuality.ACTION,(player+1)%0,[self])

    class ForeignAidMove:
        def __init__(self):
            self.index = 2
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins+2,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, StateQuality.COUNTER,(player+1)%0,[self])
            else:
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+2,curr_state.turn_counter, StateQuality.COUNTER,(player+1)%0,[self]) 

    class CoupMove:
        def __init__(self):
            self.index = 3
        
        def assign_players(self,p1obj,p2obj):
            self.p1 = p1obj 
            self.p2 = p2obj

        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.turn_counter%2
            history.append((self,player))
            if player == 0:
                newcards = self.p2.choose_card_to_lose(curr_state)
                self.p2.cards = newcards
                return PublicState(bin_encoder(history),curr_state.p1cards,curr_state.p1coins-7,curr_state.p2cards-1,curr_state.p2coins,curr_state.turn_counter, StateQuality.ACTION,(player+1)%0,[self])
            else:
                newcards = self.p1.choose_card_to_lose(curr_state)
                self.p1.cards = newcards 
                return PublicState(bin_encoder(history),curr_state.p1cards-1,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins-7,curr_state.turn_counter, StateQuality.ACTION,(player+1)%0,[self]) 
    
    class CounterForeignAidMove:
        def __init__(self):
            self.index = 7
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            pass 

    class CounterStealMove:
        def __init__(self):
            self.index = 8
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            pass  

    class CounterAssassinMove:
        def __init__(self):
            self.index = 9
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            pass  

    class ChallengeMove:
        def __init__(self):
            self.index = 10
        
        def execute(self,curr_state, private_state):
            pass

    class AllowMove:
        def __init__(self):
            self.index = 11 

        def execute(self,curr_state, private_state):
            pass

    
class PublicState:
    #contains info about history bins, number of cards on the table, number of coins, and current turn
    def __init__(self, bins, p1cards, p1coins, p2cards, p2coins, turn_counter, state_class, curr_player, movestack):
        self.bins = bins
        self.p1cards = p1cards 
        self.p1coins = p1coins 
        self.p2cards = p2cards
        self.p2coins = p2coins 
        self.turn_counter = turn_counter
        self.state_class = state_class
        self.movestack = movestack

    def is_terminal(self,state):
        """returns -1 if not terminal, 0 if current player wins, 1 if other player wins"""
        pass 

    def next_quality(self):
        """return 0, 1, 2, 3 to represent whether the next game state is 
            either before any main actions (0), open to challenge immediately after (1),
            before an applicable counteraction (2), open to challenge after a counteraction (3)"""
        return (self.state_class + 1) % 4

    def encode(self):
        """returns an array of """
        pass 

class AgentState:
    #the private state of the agent: what cards the agent has
    def __init__(self, encoded_card_1, encoded_card_2):
        self.encoded_1 = encoded_card_1
        self.encoded_2 = encoded_card_2
    


    

    
        

        
    
    