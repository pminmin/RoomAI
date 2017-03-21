#!/bin/python

import sys
import unittest
from roomai.doudizhu import *

class DouDiZhuPokerUtilTester(unittest.TestCase):

    
    def testCandidatesAction1(self):

        env = DouDiZhuPokerEnv();
        env.init()
        env.public_state.is_response = False
        env.public_state.phase = PhaseSpace.play

        hand_cards2 = []
        for i in xrange(3):
            for j in xrange(2):
                hand_cards2.append(i)
        for i in xrange(3,3+3):
            for j in xrange(4):
                hand_cards2.append(i)
        hand_cards2.append(13)
        hand_cards2.append(14)
        env.public_state.is_response = True
        env.public_state.license_action = Action([1,1],[])
        actions = Utils.candidate_actions(HandCards(hand_cards2), env.public_state)
        for key in actions:
            a = actions[key]

    
