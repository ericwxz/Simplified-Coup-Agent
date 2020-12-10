

class TwoSimpCoup:

    #game architecture:
    #each game state

    def __init__(self):
        self.cardtypes = {(0,0,0,1):"Duke", (0,0,1,0):"Assassin", (0,1,0,0):"Captain", (1,0,0,0):"Contessa"}
        self.cardmoves = {"Duke": [], "Assassin":[], "Captain":[]}
        self.cardcounters = {"Duke":[], "Captain":[],"Contessa":[]}
        self.counter_playbook_size = 3
        self.main_playbook_size = 6
        self.history = [] #history of (action, player)

    def encode_action(self,  action):
        """One-hot encoding of an action"""

    #for testing against random/optimal
    def play(self, policy1, policy2):
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
        pass

    def new_game(self):
        """returns the initial public state and randomly selected private states"""
        pass 

    



    class BaseMove:
        #moves change the current state of the game
        def __init__(self):
            pass 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state):
            pass 

    class TaxMove:

    class AssassinateMove:

    class StealMove:
    
    class CounterForeignAidMove:

    class CounterStealMove:

    class CounterAssassinMove:

    class ChallengeMove:
        def __init__(self):
            pass 
        
        def execute(self,curr_state, private_state):
            pass

    
    class PublicState:
        #contains info about history bins, number of cards on the table, number of coins, is_current_turn
        def __init__(self, info):
            pass

        def is_terminal(self,state):
            """returns -1 if not terminal, 0 if current player wins, 1 if other player wins"""
            pass 

        def next_quality(self,state):
            """return 0, 1, 2, 3 to represent whether the next game state is 
                either before any main actions (0), open to challenge immediately after (1),
                before an applicable counteraction (2), open to challenge after a counteraction (3)"""
            return (self.state_quality + 1) % 4

        def encode(self):
            """returns an array of """
            pass 

    class AgentState:
        def __init__(self, encoded_cards):
            self.state = encoded_cards 
    


    

    
        

        
    
    