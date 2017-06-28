#!/bin/python
import roomai.common
import random

class SevenKingFiveTwoThreeRandomPlayer(roomai.common.AbstractPlayer):
    #@override
    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    #@override
    def take_action(self):
        idx = int(random.random() * len(self.available_actions))
        return self.available_actions.values()[idx]

    #@overide
    def reset(self):
        pass