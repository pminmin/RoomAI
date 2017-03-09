#!/bin/python

import sys
import unittest
from roomai.doudizhu import *

class DouDiZhuPokerUtilTester(unittest.TestCase):
    def testAction2Patterns(self):
        
        a = Action([1,1,1],[2])
        self.assertEqual(a.pattern[0], "p_3_1_0_1_1")

        a = Action([1,1,1,2,3,3],[])
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
        cards = [1,2,3]
        hand_cards = HandCards(cards)

        cards1 =[1]
        hand_cards.remove_cards(cards1)
        self.assertEqual(hand_cards.cards[1],0)
        self.assertEqual(hand_cards.count2num[1],2)
        self.assertEqual(hand_cards.num_cards,2)
        ##[2,3]
        
        cards2 = [2,2]
        hand_cards.add_cards(cards2)
        self.assertEqual(hand_cards.cards[2],3)
        self.assertEqual(hand_cards.count2num[1],1)
        self.assertEqual(hand_cards.count2num[3],1)
        self.assertEqual(hand_cards.num_cards,4)
        ##[2,2,2,3]
