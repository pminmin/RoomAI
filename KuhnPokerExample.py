#!/bin/python
from roomai.kuhn import *;
import random

class KuhnPokerExamplePlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        self.available_actions  = None

    #@override
    def receive_info(self, info):
        if info.available_actions is not None:
            self.available_actions = info.available_actions

    #@override
    def take_action(self):
        idx = int(random.random() * len(self.available_actions))
        return self.available_actions[idx]
    
    #@overide
    def reset(self):
        pass


if __name__ == "__main__":

        players = [KuhnPokerExamplePlayer() for i in xrange(2)]
        env = KuhnPokerEnv()

        scores = KuhnPokerEnv.round(env, players)

        print scores