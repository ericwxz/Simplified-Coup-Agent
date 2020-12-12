from TwoPlayerCoup import AgentState
from TwoPlayerCoup import TwoSimpCoup
class BasePlayer:
    def __init__(self, game):
        self.game = game

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
    def __init__(self, policy):
        super.__init__()
        self.policy = policy

    def make_move(self,state):
        #return the move dictated by the policy given
        pass 

class RandomPlayer(BasePlayer):
    def __init__(self):
        super.__init__()

    def make_move(self,state):
        pass 

class HumanPlayer(BasePlayer):
    def __init__(self):
        super.__init__()

    def make_move(self,state):
        pass 