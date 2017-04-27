#!/bin/python
import roomai
import random
from roomai.doudizhu.DouDiZhuPokerUtils import *

class DouDiZhuPokerRandomPlayer(roomai.abstract.AbstractPlayer):
    
    def __init__(self):
        self.available_actions  = None
    #@override

    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    #@override
    def take_action(self):
        candidates = self.available_actions.values()
        idx = int(random.random() * len(candidates))
        action = candidates[idx]
        return action

    #@override
    def reset(self, action):
        self.available_actions = None