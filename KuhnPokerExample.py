#!/bin/python
from roomai.kuhn import *;
import random

class KuhnPokerExamplePlayer(roomai.abstract.AbstractPlayer):
    #@override
    def receive_info(self, info):
        if info.person_state.available_actions is not None:
            self.available_actions = info.person_state.available_actions

    #@override
    def take_action(self):
        idx = int(random.random() * len(self.available_actions))
        return self.available_actions.values()[idx]
    
    #@overide
    def reset(self):
        pass

def main():
        players = [KuhnPokerExamplePlayer() for i in xrange(2)]
        env = KuhnPokerEnv()
        scores = KuhnPokerEnv.compete(env, players)
        print scores

if __name__ == "__main__":
    main()
