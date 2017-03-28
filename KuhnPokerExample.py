#!/bin/python
from roomai.kuhn import *;
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
        idx = int(random.random() * len(self.available_actions))
        return self.available_actions[idx]
    
    #@overide
    def reset(self):
        pass


if __name__ == "__main__":

        players = [KuhnPokerExamplePlayer() for i in xrange(2)]
        env = KuhnPokerEnv()

        isTerminal, _, infos = env.init()

        for i in xrange(len(players)):
            players[i].receiveInfo(infos[i])

        while isTerminal == False:
            turn = infos[-1].public_state.turn
            actions = [roomai.kuhn.ActionSpace.cheat, roomai.kuhn.ActionSpace.bet]
            action = players[turn].takeAction()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receiveInfo(infos[i])

        print scores