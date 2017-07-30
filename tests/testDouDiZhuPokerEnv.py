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
        env.init()

        cards = [0 for i in xrange(15)]
        
        for i in xrange(3):
            for j in xrange(15): 
                cards[j] += env.person_states[i].hand_cards.cards[j]
        for j in range(15):
            c = env.private_state.keep_cards.cards[j]
            cards[j] += c


        for i in xrange(13):
            self.assertEqual(cards[i],4)
        for i in xrange(13,15):
            self.assertEqual(cards[i],1)


    def testFoward(self):
        env = DouDiZhuPokerEnv()
        p = [0,0,0]
        env.init()

        ### init
        for i in xrange(3):
            env.person_states[i].hand_cards.cards = [0 for m in xrange(15)]
            for j in xrange(4*i,4*(i+1)):
                for count in range(4):
                    env.person_states[i].hand_cards.add_cards_str(DouDiZhuActionElement.rank_to_str[j])
            env.person_states[i].hand_cards.add_cards_str(DouDiZhuActionElement.rank_to_str[12])
        env.private_state.keep_cards.add_cards_str("".join([DouDiZhuActionElement.rank_to_str[12],DouDiZhuActionElement.rank_to_str[13], DouDiZhuActionElement.rank_to_str[14]]))
        env.public_state.turn = 0
        
        # landlord 0:4,1:4,2:4,3:4      12:1 
        # peasant1 4:4,5:4,6:4,7:4      12:1
        # peasant2 8:4,9:4,10:4,11:4    12:1
        # remaining 12:1 13:1 14:1

        action = DouDiZhuPokerAction([DouDiZhuActionElement.r], [])
        self.assertFalse(env.is_action_valid(action, env.public_state,env.person_states[env.public_state.turn]))

        action = DouDiZhuPokerAction([1, 2, 3, 4, 5], [12, 2, 3])
        self.assertFalse(env.is_action_valid(action, env.public_state,env.person_states[env.public_state.turn]))

        ##0 turn = 0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.bid], [])
        infos, public_state, person_states, private_state = env.forward(action)

        ##1 turn = 1
        action = DouDiZhuPokerAction([DouDiZhuActionElement.bid], [])
        infos, public_state, person_states, private_state = env.forward(action)
        
        ##2 turn = 2
        self.assertEqual(env.public_state.turn,2)
        action = DouDiZhuPokerAction([DouDiZhuActionElement.bid], [])
        infos, public_state, person_states, private_state = env.forward(action)
        self.assertEqual(public_state.landlord_id,2)
        self.assertEqual(public_state.phase, 1)
        # peasant   0:4, 1:4, 2:4,  3:4  12:1 
        # peasant   4:4, 5:4, 6:4,  7:4  12:1
        # landlord  8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1     
      
        #landlord = 2 
        #########################play phase#################
        ##3 turn = 2 license_id = 2
        self.assertEqual(env.public_state.turn,2)
        self.assertEqual(env.public_state.license_playerid,2)
        action = DouDiZhuPokerAction([8], [])
        infos, public_state, person_states, private_state = env.forward(action)
        # landlord 4:4, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2     

        ## 4 turn = 0 license_id = 2
        self.assertEqual(env.public_state.turn,0)
        action = DouDiZhuPokerAction([0], [])
        self.assertFalse(env.is_action_valid(action,public_state,person_states[public_state.turn]))
        action = DouDiZhuPokerAction([0], [])
        infos, public_state, person_states, private_state = env.forward(action)
        self.assertEqual(public_state.license_playerid,0)
        self.assertEqual(public_state.turn,1)
        action = DouDiZhuPokerAction([8, 8, 8, 8], [9, 10])
        self.assertFalse(env.is_action_valid(action,public_state,person_states[public_state.turn]))
        # landlord 0:3, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1  

        ## 5 turn == 1 license_id =0
        self.assertEqual(env.public_state.epoch,5)
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        infos, public_state, person_states, private_state= env.forward(action)
        # landlord 0:3, 1:4, 2:4,  3:4  12:1 
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1

        ## 6 turn == 2 license_id =0
        self.assertEqual(env.public_state.license_playerid, 0)
        self.assertEqual(env.public_state.turn, 2)
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        infos,public_state,person_states,private_state= env.forward(action)
        # landlord 0:3, 1:4, 2:4,  3:4  12:1
        # peasant1 4:4, 5:4, 6:4,  7:4  12:1
        # peasant2 8:3, 9:4, 10:4, 11:4 12:2 13:1 14:1  

        
        ## 7 turn == 0 license_id = 0
        self.assertEqual(env.public_state.license_playerid, 0)
        self.assertEqual(env.public_state.turn, 0)
        self.assertEqual(env.public_state.is_response, False)
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        self.assertFalse(env.is_action_valid(action,public_state,person_states[public_state.turn]))
        action = DouDiZhuPokerAction([0, 0, 0], [12])
        infos, public_state, person_states, private_state= env.forward(action)
        self.assertEqual(person_states[0].hand_cards.cards[0], 0)
        self.assertEqual(person_states[0].hand_cards.cards[1], 4)
        self.assertEqual(person_states[0].hand_cards.cards[12], 0)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1  

        ## 8 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        ## 9 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2 13:1 14:1  


        #10 turn = 0 license_id = 0
        action = DouDiZhuPokerAction([0, 0, 0], [])
        env.forward(action) 
        ## 11 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        ## 12 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        # landlord 0:0, 1:4, 2:4,  3:4  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2  
        
        # 13 turn =0 license_id = 0
        action = DouDiZhuPokerAction([1, 1, 2, 2, 3, 3], [])
        self.assertTrue(env.is_action_valid(action, public_state, person_states[public_state.turn]))
        env.forward(action)


        ## 14 turn == 1 license_id =0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        ## 15 turn = 2  license_id = 0
        action = DouDiZhuPokerAction([DouDiZhuActionElement.cheat], [])
        env.forward(action)
        # landlord 0:0, 1:2, 2:2,  3:2  12:0 
        # peasant1 4:3, 5:4, 6:4,  7:4  12:1
        # peasant2 8:4, 9:4, 10:4, 11:4 12:2  

        # 16 turn =0 license_id = 0
        action = DouDiZhuPokerAction([1, 1, 2, 2, 3, 3], [])
        self.assertTrue(env.is_action_valid(action,public_state,person_states[public_state.turn ]))
        infos, public_state, person_states, private_state = env.forward(action)
        expected_scores = [1,1,-2]
        scores = public_state.scores
        print public_state.scores
        print public_state.is_terminal
        for i in xrange(len(scores)):
            self.assertEqual(scores[i], expected_scores[i])
        
