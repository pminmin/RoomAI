#!/bin/python
#coding:utf-8
import random
import roomai.common
import roomai.kuhn.KuhnPokerUtils

class KuhnPokerAlwaysBetPlayer(roomai.common.AbstractPlayer):

           
    def receive_info(self, info):
        pass     

    def take_action(self):
        return roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("bet")

    def reset(self):
        pass


class KuhnPokerRandomPlayer(roomai.common.AbstractPlayer):
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
