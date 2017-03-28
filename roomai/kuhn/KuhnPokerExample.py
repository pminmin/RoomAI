#!/bin/python
import roomai.abstract
import roomai.kuhn.ActionSpace
import random

class KuhnPokerExamplePlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        self.available_actions  = None

    #@override
    def receiveInfo(self, info):
        if info.available_actions is not None:
            self.available_actions = info.available_actions

    #@override
    def takeAction(self):
        idx = int(random.random * len(self.available_actions))
        return self.available_actions[idx]
    
    #@overide
    def reset(self):
        pass
