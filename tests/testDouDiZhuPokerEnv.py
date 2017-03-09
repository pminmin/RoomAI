#!/bin/python
#coding:utf-8
import sys
import unittest
import copy
from roomai.doudizhu   import *


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
                cards[j] += env.private_state.hand_cards[i].cards[j]
        for c in env.private_state.keep_cards:
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
        hand_cards = [[],[],[]]
        for i in xrange(3):
            for j in xrange(4*i,4*(i+1)):
                for k in xrange(4):
                    hand_cards[i].append(j)
            hand_cards[i].append(12)
            env.private_state.hand_cards[i] = HandCards(hand_cards[i])
        env.private_state.keep_cards = [12, 13, 14]
        env.public_state.turn = 0
        
        # landlord 0:4,1:4,2:4,3:4      12:1 
        # peasant1 4:4,5:4,6:4,7:4      12:1
        # peasant2 8:4,9:4,10:4,11:4    12:1
        # remaining 12:1 13:1 14:1

        action = Action([ActionSpace.r],[])
        self.assertFalse(env.isActionValid(action))

        action = Action([1,2,3,4,5],[12,2,3])
        self.assertFalse(env.isActionValid(action))

        ##0 turn = 0
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)

        ##1 turn = 1
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)
        
        ##2 turn = 2
        self.assertEqual(env.public_state.turn,2)
        action = Action([ActionSpace.bid],[])
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(infos[3].public_state.landlord_id,2)
        self.assertEqual(infos[3].public_state.phase, 1)
        # peasant   0:4, 1:4, 2:4,  3:4  12:1 
        # peasant   4:4, 5:4, 6:4,  7:4  12:1
        # landlord  8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1     
      
        #landlord = 2 
        #########################play phase#################
        ##3 turn = 2 license_id = 2
        self.assertEqual(env.public_state.turn,2)
        self.assertEqual(env.public_state.license_playerid,2)
        action = Action([8],[])
        isTerminal, scores, infos = env.forward(action)
        # landlord 4:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2     

        ## 4 turn = 0 license_id = 2
        self.assertEqual(env.public_state.turn,0)
        action = Action([0],[])
        self.assertFalse(env.isActionValid(action))
        action = Action([0],[])
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(infos[3].public_state.license_playerid,0)
        self.assertEqual(infos[3].public_state.turn,1)        
        action = Action([8,8,8,8],[9,10])
        self.assertFalse(env.isActionValid(action)) 
        # landlord 0:3, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1  

        ## 5 turn == 1 license_id =0
        self.assertEqual(env.public_state.epoch,5)
        action = Action([ActionSpace.cheat],[])
        isTerminal, scores, infos = env.forward(action)
        # landlord 0:3, 1:4, 2:4,  3:4  12:1 
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1

        ## 6 turn == 2 license_id =0
        self.assertEqual(env.public_state.license_playerid, 0)
        self.assertEqual(env.public_state.turn, 2)
        action = Action([ActionSpace.cheat],[])
        isTerminal, scores, infos = env.forward(action)         
        # landlord 0:3, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1  
        
        ## 7 turn == 0 license_id = 0
        self.assertEqual(env.public_state.license_playerid, 0)
        self.assertEqual(env.public_state.turn, 0)
        action = Action([ActionSpace.cheat],[])
        self.assertFalse(env.isActionValid(action))
        action = Action([0,0,0],[12])
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(infos[3].private_state.hand_cards[0].cards[0], 0)
        self.assertEqual(infos[3].private_state.hand_cards[0].cards[1], 4)
        self.assertEqual(infos[3].private_state.hand_cards[0].cards[12], 0)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1  

        ## 8 turn == 1 license_id =0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        ## 9 turn = 2  license_id = 0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1  


        #10 turn = 0 license_id = 0
        action = Action([0,0,0],[])
        env.forward(action) 
        ## 11 turn == 1 license_id =0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        ## 12 turn = 2  license_id = 0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2  
        
        # 13 turn =0 license_id = 0
        action = Action([1,1,2,2,3,3],[])
        self.assertTrue(env.isActionValid(action))
        env.forward(action)


        ## 14 turn == 1 license_id =0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        ## 15 turn = 2  license_id = 0
        action = Action([ActionSpace.cheat],[])
        env.forward(action)
        # landlord 0:0, 1:2, 2:2,  3:2  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2  

        # 16 turn =0 license_id = 0
        action = Action([1,1,2,2,3,3],[])
        self.assertTrue(env.isActionValid(action))
        isTerminal, scores, infos = env.forward(action)
        expected_scores = [1,1,-2]
        for i in xrange(len(scores)):
            self.assertEqual(scores[i], expected_scores[i])
        
