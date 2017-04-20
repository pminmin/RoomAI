#!/bin/python

import sys
import unittest
from roomai.doudizhu import *

class DouDiZhuPokerUtilTester(unittest.TestCase):

    
    def testAction2Patterns(self):
        
        a = Action([1,1,1],[2])
        self.assertEqual(a.pattern[0], "p_3_1_0_1_0")

        a = Action([1,1,1,2,3,3],[])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([1,1,1,1],[2])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([1,1,1,1,1],[2])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([ActionSpace.cheat],[2])
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([ActionSpace.cheat],[])
        self.assertEqual(a.pattern[0], "i_cheat")
        
        a = Action([ActionSpace.R, ActionSpace.r],[])
        self.assertEqual(a.pattern[0], "x_rocket")
        

    def testAllPatterns(self):
        for k in AllPatterns:
            p = AllPatterns[k]
            self.assertEqual(k,p[0])
            self.assertEqual(len(p),7)
            if "p" in p[0]:
                self.assertEqual("p_%d_%d_%d_%d_%d"%(p[1],p[2],p[3],p[4],p[5]), p[0])

    def testRemoveCards(self):
        cards = [ActionSpace.key_to_str[1],ActionSpace.key_to_str[2],ActionSpace.key_to_str[3]]
        hand_cards = HandCards(cards)
        print hand_cards.cards

        cards1 = HandCards("4")
        print cards1.cards
        hand_cards.remove_cards(cards1)
        self.assertEqual(hand_cards.cards[1],0)
        self.assertEqual(hand_cards.count2num[1],2)
        self.assertEqual(hand_cards.num_cards,2)
        ##[2,3]
        
        cards2 = HandCards("55")
        hand_cards.add_cards(cards2)
        self.assertEqual(hand_cards.cards[2],3)
        self.assertEqual(hand_cards.count2num[1],1)
        self.assertEqual(hand_cards.count2num[3],1)
        self.assertEqual(hand_cards.num_cards,4)
        ##[2,2,2,3]
    
    def test_extractMaster(self):
        cards = []
        for i in xrange(13):
            for j in xrange(4):
                cards.append(ActionSpace.key_to_str[i])
        cards.append(ActionSpace.key_to_str[13])
        cards.append(ActionSpace.key_to_str[14])

        hand_cards = HandCards(cards)

        ## extract straight
        ss = Utils.extractMasterCards(hand_cards, 5, 3, Action([0,0,0,1,1,1,2,2,2],[]).pattern)


        ## extract slave
        ss = Utils.extractSlaveCards(hand_cards, 5, [1,1,1,1], Action([1,1,1,1],[]).pattern)
        for s in ss:
            for i in s:
                self.assertTrue(i!=1)
        

    def testCandidateAction(self):
        env = DouDiZhuPokerEnv();
        env.init()
        env.public_state.is_response = False
        env.public_state.phase = PhaseSpace.play
        
        #hand_cards1 = HandCards([1,2,3,4,5,6,6,13,14])
        tmp = [1,1,1,2,2,3,3,4,4,5,6,8,8,8,8,9,9,10,10,10,10,13,14]
        for i in xrange(len(tmp)):
            tmp[i] = ActionSpace.key_to_str[tmp[i]]
        hand_cards1 = HandCards(tmp)
        #self.assertEqual(hand_cards1.num_cards,32)

         
        actions = Utils.candidate_actions(hand_cards1, env.public_state)
        for key in actions:
            a = actions[key]
            flag = Utils.is_action_from_handcards(hand_cards1,a)
            self.assertTrue(flag)     
            self.assertTrue(a.pattern[0] != "i_invalid") 
        
    
    def testCandidatesAction1(self):

        env = DouDiZhuPokerEnv();
        env.init()
        env.public_state.is_response = False
        env.public_state.phase = PhaseSpace.play

        hand_cards2 = []
        for i in xrange(13):
            for j in xrange(4):
                hand_cards2.append(ActionSpace.key_to_str[i])
        hand_cards2.append(ActionSpace.key_to_str[13])
        hand_cards2.append(ActionSpace.key_to_str[14])
        env.public_state.is_response = True
        env.public_state.license_action = Action([1,1],[])
        actions = Utils.candidate_actions(HandCards(hand_cards2), env.public_state)
        for key in actions:
            a = actions[key]
            print key, a.masterCards, a.slaveCards
        self.assertEqual(len(actions),26)

        
        env.public_state.is_response = True
        env.public_state.license_action = Action([1,1,1,1],[0,0])
        actions = Utils.candidate_actions(HandCards(hand_cards2), env.public_state)
        for key in actions:
            a = actions[key]

        env.public_state.is_response = False
        env.public_state.license_action = Action([1,1],[])
        actions = Utils.candidate_actions(HandCards(hand_cards2), env.public_state)
        for key in actions:
            a = actions[key]

    
    def testHandCards(self):
        a = ["3","3","3","4"]
        hand_cards = HandCards(a);
        hand_cards.remove_cards(HandCards("3"))
        self.assertEqual(hand_cards.cards[0], 2)
        print hand_cards.cards
        hand_cards.add_cards(HandCards("45"))
        print hand_cards.cards
        self.assertEqual(hand_cards.cards[1], 2)
        hand_cards.remove_cards_str("5")
        self.assertEqual(hand_cards.cards[2], 0)

    def testHandCards1(self):
        h = HandCards("45")
        self.assertEqual(h.cards[1],1)
        self.assertEqual(h.cards[2],1)

