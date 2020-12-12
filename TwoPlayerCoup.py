import random
from Player import PolicyPlayer
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
        self.cardactions = {0: [self.TaxMove()], 1:[self.AssassinateMove()], 2:[self.StealMove()], -1:[self.IncomeMove(), self.ForeignAidMove(),self.CoupMove()]}
        self.cardcounters = {"Duke":[self.CounterForeignAidMove()], "Captain":[self.CounterStealMove()],"Contessa":[self.CounterAssassinMove()],"All":[]}
        self.associations = {1:None, 2:None, 3:None, 4:0, 5:1, 6:2, 7:3, 8:2, 9:3, 10:None, 11:None}
        self.counter_playbook_size = 3
        self.main_playbook_size = 6
        self.combined_playbook = {1: self.IncomeMove(), 2: self.ForeignAidMove(), 3: self.CoupMove(), 4: self.TaxMove(), 5: self.AssassinateMove(), 6: self.StealMove(), 7: self.CounterForeignAidMove(), 8: self.CounterStealMove(), 9: self.CounterAssassinMove(), 10: self.ChallengeMove(self.associations), 11: self.AllowMove()}
        self.num_cards = 4
        self.card_dupes = 3
        self.history = [] #history of (action, player) or (-1, player, card index) for losing cards
        self.p1 = None 
        self.p2 = None
        self.curr_state = None

    def assign_players(self, p1obj, p2obj):
        self.p1 = p1obj 
        self.p2 = p2obj

    def encode_action(self,  action):
        """One-hot encoding of an action"""
        return (0 if i != action.index-1 else 1 for i in range(len(self.combined_playbook)))

    def encode_card(self, card_index):
        return (0 if i != card_index else 1 for i in range(self.num_cards))

    def encode_bins(self):
        if len(self.history) < 3:
            return ((0,0,0,0),(0,0,0,0))
        p1_bins = [0 for i in range(self.num_cards)]
        p2_bins = [0 for i in range (self.num_cards)]
        for action_player in self.history:
            if len(action_player) > 2:
                #check card index and subtract 5
                if action_player[1] == 0:
                    p1_bins[action_player[2]] -= 5
                else:
                    p2_bins[action_player[2]] -= 5
            elif self.associations[action_player[0].index] != None:
                if action_player[1] == 0:
                    p1_bins[self.associations[action_player[0].index]] += 1
                else:
                    p2_bins[self.associations[action_player[0].index]] += 1
        
        #calculate certainty: 0 for unlikely, 0.5 for unclear, 1 for likely
        p1_total = sum(p1_bins)
        p2_total = sum(p2_bins)
        for i in range(self.num_cards):
            if p1_bins[i] > p1_total//2:
                p1_bins[i] = 1
            elif p1_bins[i] < p1_total//5:
                p1_bins[i] = 0
            else:
                p1_bins[i] = 0.5 

            if p2_bins[i] > p2_total//2:
                p2_bins[i] = 1
            elif p2_bins[i] < p1_total//5:
                p2_bins[i] = 0
            else:
                p2_bins[i] = 0.5 
        return (tuple(p1_bins), tuple(p2_bins))

        #return (p1(certainty bins),p2(certainty))

    def valid_moves(self, state):
        """"""
        if state.curr_player == 0:
            playercoins = state.p1coins 
        else:
            playercoins = state.p2coins 

        moves = []
        
        if state.state_class == StateQuality.ACTION:
            moves.extend([1,2,4,6])
            if playercoins >= 10:
                return [3]
            if playercoins >= 3:
                moves.append(5)
            if playercoins >= 7:
                moves.append(3)
            return moves

        elif state.state_class == StateQuality.CHALLENGEACTION or state.state_class == StateQuality.CHALLENGECOUNTER:
            lastindex = state.movestack[len(state.movestack)-1].index 
            if lastindex != 3 and lastindex < 10:
                #main action or counter 
                return [10,11]
            else:
                return []
        elif state.state_class == StateQuality.COUNTER:
            lastmove = state.movestack[len(state.movestack)-1]
            moves = []
            if lastmove.index == 5:
                moves.append(9)
            if lastmove.index == 2:
                moves.append(7)
            if lastmove.index == 6:
                moves.append(8)
            moves.append(11)
            return moves
        elif state.state_class == StateQuality.LOSINGCARD:
            moves.append(-1)
            return moves
        
        return None


    def new_game(self):
        """returns the initial public state and randomly selected private states (encoded for NN); resets history; resets cards in each player's hand"""
        deck = [0,0,0,1,1,1,2,2,2,3,3,3]
        p1deck = []
        p2deck = []
        p1deck.append(deck.pop(random.randrange(len(deck))))
        p1deck.append(deck.pop(random.randrange(len(deck))))
        p2deck.append(deck.pop(random.randrange(len(deck))))
        p2deck.append(deck.pop(random.randrange(len(deck))))
        self.p1.get_cards(p1deck)
        self.p2.get_cards(p2deck)
        start_state = PublicState([],2,2,2,2,0,StateQuality.ACTION, 0, [])
        self.curr_state = start_state
        ret_vals = [start_state] #public state, p1state, p2state
        ret_vals.append([self.encode_card(p1deck[0]),self.encode_card(p1deck[1])])
        ret_vals.append([self.encode_card(p2deck[0]),self.encode_card(p2deck[1])])
        return ret_vals
        

    def setup(self, p1obj, p2obj):
        """Takes care of assigning players and starting new game"""
        self.assign_players(p1obj, p2obj)
        start_state_and_encoded_hands = self.new_game()
        self.combined_playbook[10].assign_players(self.p1,self.p2)

        return start_state_and_encoded_hands

    def play(self):
        if self.p1 == None or self.p2 == None:
            print("Agents not specified. Aborting")
            return 
        while self.curr_state.is_terminal() == -1:
            if self.curr_state.state_class == StateQuality.LOSINGCARD:
                if self.curr_state.curr_player == 0:
                    card_lost = self.p1.choose_card_to_lose(self.curr_state)
                    self.history.append((-1, 0, card_lost))
                    self.curr_state = PublicState(self.encode_bins(), self.curr_state.p1cards-1,self.curr_state.p1coins, self.curr_state.p2cards, self.curr_state.p2coins,self.curr_state.turn_counter+1,StateQuality.ACTION, 1, []) 

                else:
                    card_lost = self.p2.choose_card_to_lose(self.curr_state)
                    self.history.append((-1, 1, card_lost))
                    self.curr_state = PublicState(self.encode_bins(), self.curr_state.p1cards,self.curr_state.p1coins, self.curr_state.p2cards-1, self.curr_state.p2coins,self.curr_state.turn_counter+1,StateQuality.ACTION, 0, []) 

            else:
                if self.curr_state.curr_player == 0:
                    move = self.p1.make_move(self.curr_state)
                    if move == None:
                        self.curr_state = PublicState(self.curr_state.bins, self.curr_state.p1cards, self.curr_state.p1coins, self.curr_state.p2cards, self.curr_state.p2coins, self.curr_state.turn_counter, self.curr_state.next_quality(),self.curr_state.curr_player,self.curr_state.movestack)
                    else:
                        self.curr_state = self.combined_playbook[move].execute(self.curr_state,self.encode_bins,self.history)
                else:
                    move = self.p2.make_move(self.curr_state)
                    if move == None:
                        self.curr_state = PublicState(self.curr_state.bins, self.curr_state.p1cards, self.curr_state.p1coins, self.curr_state.p2cards, self.curr_state.p2coins, self.curr_state.turn_counter, self.curr_state.next_quality(),self.curr_state.curr_player,self.curr_state.movestack)
                    else:
                        self.curr_state = self.combined_playbook[move].execute(self.curr_state,self.encode_bins,self.history)

            
        return self.curr_state.is_terminal() 

    def simulate(self, policy1, policy2):
        old_players = [self.p1, self.p2]
        newp1 = PolicyPlayer(self,0,policy1)
        newp2 = PolicyPlayer(self,1,policy2)
        self.setup(newp1,newp2)
        result = self.play()
        self.setup(old_players[0],old_players[1])
        return result

    
        



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
            player = curr_state.curr_player
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins+3,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self])
            else:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+3,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self])

    class AssassinateMove:
        def __init__(self):
            self.index = 5 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            #delay card loss after other stages; only calculate coin loss
            if player== 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins-3,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(), (player+1)%2,[self])
            else:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins-3,curr_state.turn_counter, curr_state.next_quality(), (player+1)%2,[self])   

    class StealMove:
        def __init__(self):
            self.index = 6 
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            stolen_amount = 2
            if player == 0:
                if curr_state.p2coins < 2:
                    stolen_amount = curr_state.p2coins
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins+stolen_amount,curr_state.p2cards,curr_state.p2coins-stolen_amount,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self])
            else:
                if curr_state.p1coins < 2:
                    stolen_amount = curr_state.p1coins
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins-stolen_amount,curr_state.p2cards,curr_state.p2coins+stolen_amount,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,[self]) 

    class IncomeMove:
        def __init__(self):
            self.index = 1
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins+1,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, StateQuality.ACTION,(player+1)%2,[self])
            else:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+1,curr_state.turn_counter, StateQuality.ACTION,(player+1)%2,[self])

    class ForeignAidMove:
        def __init__(self):
            self.index = 2
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins+2,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, StateQuality.COUNTER,(player+1)%2,[self])
            else:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins+2,curr_state.turn_counter, StateQuality.COUNTER,(player+1)%2,[self]) 

    class CoupMove:
        def __init__(self):
            self.index = 3
        
        def assign_players(self,p1obj,p2obj):
            self.p1 = p1obj 
            self.p2 = p2obj

        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins-7,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, StateQuality.LOSINGCARD,(player+1)%2,[self])
            else:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins-7,curr_state.turn_counter, StateQuality.LOSINGCARD,(player+1)%2,[self]) 
    
    class CounterForeignAidMove:
        def __init__(self):
            self.index = 7
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            curr_state.movestack.append(self)
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins-2,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)
            else: 
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins-2,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)  

    class CounterStealMove:
        def __init__(self):
            self.index = 8
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            curr_state.movestack.append(self)
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins+2,curr_state.p2cards,curr_state.p2coins-2,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)
            else: 
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins-2,curr_state.p2cards,curr_state.p2coins+2,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)  
  

    class CounterAssassinMove:
        def __init__(self):
            self.index = 9
        
        #returns the new state of the game after execuing the action
        #updates self.history and reevaluates bins on each move
        def execute(self, curr_state, bin_encoder, history):
            player = curr_state.curr_player
            history.append((self,player))
            curr_state.movestack.append(self)
            if player == 0:
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins ,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)
            else: 
                return PublicState(bin_encoder(),curr_state.p1cards,curr_state.p1coins,curr_state.p2cards,curr_state.p2coins,curr_state.turn_counter, curr_state.next_quality(),(player+1)%2,curr_state.movestack)  
  

    class ChallengeMove:
        def __init__(self,associationtable):
            self.index = 10
            self.associations = associationtable
        def assign_players(self,p1obj,p2obj):
            self.p1 = p1obj 
            self.p2 = p2obj
        def execute(self,curr_state,bin_encoder,history):
            last_action = curr_state.movestack.pop() 
            card_challenge = self.associations[last_action.index]
            curr_state.movestack.append(self)
            if curr_state.curr_player == 0:
                if card_challenge not in self.p2.cards:
                    #successful challenge
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins, curr_state.turn_counter,StateQuality.LOSINGCARD, (curr_state.curr_player+1)%2,curr_state.movestack)
                else:
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins, curr_state.turn_counter,StateQuality.LOSINGCARD, curr_state.curr_player,curr_state.movestack)
            else: 
                if card_challenge not in self.p1.cards:
                    #successful challenge
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins, curr_state.turn_counter,StateQuality.LOSINGCARD, (curr_state.curr_player+1)%2,curr_state.movestack)
                else:
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins, curr_state.turn_counter,StateQuality.LOSINGCARD, curr_state.curr_player,curr_state.movestack)

    class AllowMove:
        def __init__(self):
            self.index = 11 

        def execute(self,curr_state,bin_encoder,history):
            next_counter = curr_state.turn_counter
            next_player = curr_state.curr_player
            curr_state.movestack.append(self)
            if curr_state.next_quality() == StateQuality.ACTION:
                next_counter += 1
                next_player = (next_player + 1)%2

            #allowing at some point in the assasination route
            if curr_state.movestack[0].index == 5:
                last_move = curr_state.movestack[len(curr_state.movestack)-1]
                if last_move.index == 9:
                    #last move was a contessa, and allowing contessa to block: no changes 
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins,next_counter,curr_state.next_quality(),next_player,curr_state.movestack)
                elif last_move.index == 11:
                    #last move was an opportunity to block with contessa but chose to let assassin go through: advance to LOSINGCARD
                    return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins,next_counter,StateQuality.LOSINGCARD,next_player,curr_state.movestack)
            
            return PublicState(curr_state.bins, curr_state.p1cards, curr_state.p1coins, curr_state.p2cards, curr_state.p2coins,next_counter,curr_state.next_quality(),next_player,curr_state.movestack)

            
            

    
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
        self.curr_player = curr_player

    def is_terminal(self):
        """returns -1 if not terminal, 0 if p1 wins, 1 if p2 wins"""
        if self.p1cards == 0:
            return 1
        elif self.p2cards == 0:
            return 0
        else:
            return -1

    def next_quality(self):
        """return 0, 1, 2, 3 to represent whether the next game state is 
            either before any main actions (0), open to challenge immediately after (1),
            before an applicable counteraction (2), open to challenge after a counteraction (3)"""
        return (self.state_class + 1) % 4

    def encode_action(self,  action):
        """One-hot encoding of an action"""
        return (0 if i != action.index-1 else 1 for i in range(12))

    def encode(self):
        """returns all relevant information in the public state, encoded in a list of length 24"""
        encoded = list(self.bins[0]) #4 
        encoded.extend(list(self.bins[1])) #4
        if len(self.movestack) < 3:
            last_move = self.movestack[0].index 
        else:
            last_move = self.movestack[len(self.movestack)-1].index
        encoded.extend([self.p1cards,self.p1coins,self.p2cards,self.p2coins,self.state_class]) #5
        encoded.extend(list(self.encode_action(last_move))) #11
        return encoded

    







    

    
        

        
    
    