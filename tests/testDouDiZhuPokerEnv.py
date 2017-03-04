#!/bin/python
#coding:utf-8
import sys
import unittest
import copy
sys.path.append("DouDiZhuPoker")

from DouDiZhuPokerEnv   import *


class DouDiZhuPokerEnvTester(unittest.TestCase):
    def testNormal(self):
        env = DouDiZhuPokerEnv()

        p = []
        with self.assertRaises(Exception):
            env.init(p)


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
            for j in xrange(4*i,4*(i+1)):
                env.private_state.hand_cards[i][j] = 4
            env.private_state.hand_cards[i][12] = 1
        env.private_state.additive_cards = [12, 13, 14]
        env.public_state.turn = 0
        
        # landlord 0:4,1:4,2:4,3:4 12:1 
        # peasant1 4:4,5:4,6:4,7:4 12:1
        # peasant2 8:4,9:4,10:4,11:4      
        # remaining 12:1 13:1 14:1

        action = Action([ActionSpace.r],[])
        self.assertFalse(env.isActionValid(action))

        action = Action([1,2,3,4,5],[12,2,3])
        self.assertFalse(env.isActionValid(action))

        ##1 turn = 0
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)

        ##2 turn = 1
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)
        
        ##3 turn = 2
        self.assertEqual(env.public_state.turn,2)
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(infos[3].public_state.landlord_id,2)
        self.assertEqual(infos[3].public_state.phase, 1)
        # landlord 0:4, 1:4, 2:4,  3:4  12:2 13:1 14:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4      
        
        #########################play phase#################
        ##4 turn = 2
        self.assertEqual(env.public_state.turn,2)
        action = Action([0],[])
        isTerminal, scores, infos = env.forward(action)
        # landlord 0:3, 1:4, 2:4,  3:4  12:2 13:1 14:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4      

        ## 5 turn = 0 
        self.assertEqual(env.public_state.turn,0)
        action = Action([0],[])
        self.assertFalse(env.isActionValid(action))
        action = Action([4],[])
        isTerminal, scores, infos = env.forward(action)
        # landlord 0:3, 1:4, 2:4,  3:4  12:2 13:1 14:1
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4   
        self.assertEqual(infos[3].public_state.license_playerid,0)
        self.assertEqual(infos[3].public_state.turn,1)

        
        action = Action([8,8,8,8],[9,10])
        self.assertFalse(env.isActionValid(action)) 
