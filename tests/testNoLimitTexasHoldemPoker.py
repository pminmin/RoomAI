#!/bin/python
import sys
import unittest

#from roomai.texas import *

class NoLimitTexasHoldemPokerTester(unittest.TestCase):

    def testUtil(self):
        '''
        hand_cards    = [Card(2,0),Card(3,0)]
        remaining_cards = [Card(4,0),Card(5,0),Card(6,0),Card(7,0),Card(8,0)]

        pattern = cards2pattern(hand_cards, remaining_cards)
        self.assertEqual(pattern[0], "Straight_SameSuit")
        for i in xrange(len(pattern[6])):
            c = pattern[6][i]
            self.assertEqual(c.suit,0)
            self.assertEqual(c.point, i + 4)
        
        hand_cards = [Card(2,0), Card(4,0)]
        remaining_cards = [Card(6,0), Card(8,0), Card(10,0), Card(12,0), Card(0,0)]
        pattern = cards2pattern(hand_cards, remaining_cards)
        self.assertEqual(pattern[0], "SameSuit")
        for i in xrange(len(pattern[6])):
            c = pattern[6][i]
            self.assertEqual(i * 2 + 4, c.point)
            self.assertEqual(0,c.suit)

        hand_cards = [Card(2,0), Card(3,0)]
        remaining_cards = [Card(1,0), Card(1,1), Card(1,2), Card(1,3), Card(2,1)]
        pattern = cards2pattern(hand_cards, remaining_cards)
        self.assertEqual(pattern[0], "4_1")
        for i in xrange(4):
            self.assertEqual(pattern[6][i].point, 1)
            self.assertEqual(pattern[6][i].suit,i)
        self.assertEqual(pattern[6][4].point,3)
        self.assertEqual(pattern[6][4].suit,0)


        hand_cards = [Card(2,0), Card(2,1)]
        remaining_cards = [Card(4,0), Card(5,1), Card(6,2), Card(7,3), Card(    8,1)] 
        pattern = cards2pattern(hand_cards, remaining_cards)
        self.assertEqual(pattern[0], "2_1_1_1")'''
