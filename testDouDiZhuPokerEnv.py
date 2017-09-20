#!/bin/python
#coding:utf-8
import sys
import unittest
import copy
from roomai.doudizhu   import *
import roomai.common


class Player(roomai.common.AbstractPlayer):
    def reset(self):
        pass
    def receive_info(self, info):
        self.actions = info.person_state.available_actions
    def take_action(self):
        x = int(random.random() * len(self.actions))
        action = self.actions.values()[x]
        #print (action.key)
        return action

if __name__ == "__main__":

    import time
    start = time.time()
    for i in range(100):
        players = [Player() for i in range(3)]
        env = DouDiZhuPokerEnv()
        env.init()
        env.compete(env, players)
    end = time.time()
    print end-start