
class BasePlayer:
    def __init__(self):
        pass 

    def get_cards(self, agentstate):
        self.cards = agentstate

    def make_move(self,state):
        pass 

    def choose_card_to_lose(self, state):
        pass

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