
class BasePlayer:
    def __init__(self, agentstate):
        pass 

    def make_move(self,state):
        pass 

class PolicyPlayer(BasePlayer):
    def __init__(self, agentstate, policy):
        super.__init__(agentstate)
        self.policy = policy

    def make_move(self,state):
        #return the move dictated by the policy given
        pass 

class RandomPlayer(BasePlayer):
    def __init__(self, agentstate):
        super.__init__(agentstate)

    def make_move(self,state):
        pass 

class HumanPlayer(BasePlayer):
    def __init__(self, agentstate):
        super.__init__(agentstate)

    def make_move(self,state):
        pass 