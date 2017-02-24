#!/bin/python
import sys
import unittest
sys.path.append("DouDiZhuPoker")

from DouDiZhuPokerEnv   import *

class DouDiZhuPokerEnvTester(unittest.TestCase):
    def testNormal(self):
        env = DouDiZhuPokerEnv()

        p = []
        with self.assertRaises(Exception):
            env.init(p)

        print "a"

        p = [0,0,0]
        env.init(p)

        cards = [0 for i in xrange(15)]
        
        for i in xrange(3):
            for j in xrange(15): 
                cards[j] += env.private_state.hand_cards[i][j]
        for c in env.private_state.additive_cards:
            cards[c] += 1

        for i in xrange(13):
            self.assertEqual(cards[i],4)
        for i in xrange(13,15):
            self.assertEqual(cards[i],1)


    def testFoward(self):
        env = DouDiZhuPokerEnv()
        p = [0,0,0]
        env.init(p)

        ### init
        for i in xrange(3):
            env.private_state.hand_cards[i] = [0 for m in xrange(15)]
            for j in xrange(4*i,4*(i+1) - 1):
                env.private_state.hand_cards[i][j] = 4
            env.private_state.hand_cards[i][12] = 1
        env.private_state.additive_cards = [12, 13, 14]
        env.public_state.turn = 0

        action = Action([ActionSpace.r],[])
        self.assertFalse(env.isActionValid(action))

        print "b"

        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)
        print infos[3].public_state
