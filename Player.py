
import random 
class BasePlayer:
    def __init__(self, game, index):
        self.game = game
        self.index = index

    def get_cards(self, cards):
        self.cards = cards
        self.dead_cards = []

    def make_move(self,state):
        pass 

    def choose_card_to_lose(self, state):
        pass
    
    def get_encoding(self):
        state = []
        for card in self.cards:
            cardinfo = list(self.game.encode_card(card))
            cardinfo.append(1)
            state.append(cardinfo)
        for card in self.dead_cards:
            cardinfo = list(self.game.encode_card(card))
            cardinfo.append(0)
            state.append(cardinfo)
        return state

class PolicyPlayer(BasePlayer):
    def __init__(self, game, index, policy):
        super().__init__(game,index)
        self.policy = policy

    def make_move(self,state):
        #return the move dictated by the policy given
        return self.policy(state, self.cards, self.index, False)

    def choose_card_to_lose(self, state):
        card_to_lose = self.policy(state, self.cards, self.index, True) 
        
        self.dead_cards.append(self.cards[card_to_lose])
        self.cards.pop(card_to_lose)
        return card_to_lose

class RandomPlayer(BasePlayer):
    def __init__(self,game,index):
        super().__init__(game,index)

    def make_move(self,state):
        moves = self.game.valid_moves(state)
        if moves !=  None and len(moves) != 0:
            return moves[random.randrange(len(moves))]
        return None

    def choose_card_to_lose(self, state):
        card_to_lose = random.randrange(len(self.cards))
        self.dead_cards.append(self.cards[card_to_lose])
        self.cards.pop(card_to_lose)
        return card_to_lose

class HumanPlayer(BasePlayer):
    def __init__(self,game,index):
        super().__init__(game,index)

    def make_move(self,state):
        pass 

class TrainingPlayer(BasePlayer):
    def __init__(self,game,index):
        super().__init__(game,index)

class ANNPlayer(BasePlayer):
    def __init__(self,game,index):
        super().__init__(game,index)
        self.policy=None
    
    def set_nn_policy(self, policy):
        self.policy = policy

    def make_move(self, state):
        #takes encoded state (encoded public state and card encoding combined) to make a decision
        if self.policy == None:
            return None 
        return self.policy(state,self)

    def choose_card_to_lose(self, state):
        if self.policy == None:
            return None
        return self.policy(state,self)
