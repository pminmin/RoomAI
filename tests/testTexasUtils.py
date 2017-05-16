#!/bin/python
import unittest

import roomai.abstract
from roomai.texas import TexasHoldemAction
from roomai.texas import TexasHoldemEnv


class TexasUtilsTester(unittest.TestCase):

    def test_pattern(self):

        handcards1 =[roomai.abstract.PokerCard(0,0),roomai.abstract.PokerCard(1,1)]
        keepcards  =[roomai.abstract.PokerCard(2,2),roomai.abstract.PokerCard(3,3),roomai.abstract.PokerCard(4,0),roomai.abstract.PokerCard(5,1),roomai.abstract.PokerCard(6,2)]
        pattern    = TexasHoldemEnv.cards2pattern(handcards1, keepcards)
        print pattern

    
    def test_cards1(self):
        handcards1 = [roomai.abstract.PokerCard(0,0),roomai.abstract.PokerCard(0,1)]
        handcards2 = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(3,2)]
        keepcards  = [roomai.abstract.PokerCard(0,2),roomai.abstract.PokerCard(0,3),roomai.abstract.PokerCard(2,0),roomai.abstract.PokerCard(2,1),roomai.abstract.PokerCard(3,3)]
        pattern = TexasHoldemEnv.cards2pattern(handcards2, keepcards)

        self.assertEqual(pattern[0],'3_2')
        self.assertEqual(pattern[1],False)
        self.assertEqual(pattern[2],True)
        self.assertEqual(pattern[3],False)
        self.assertEqual(pattern[4][0], 3)
        self.assertEqual(pattern[4][1], 2)
        self.assertEqual(pattern[6][0].get_point_rank(), 3)
        self.assertEqual(pattern[6][1].get_point_rank(), 3)
        self.assertEqual(pattern[6][2].get_point_rank(), 3)
        self.assertEqual(pattern[6][3].get_point_rank(), 2)
        self.assertEqual(pattern[6][4].get_point_rank(), 2)

        self.assertEqual(pattern[6][0].get_suit_rank(), 1)
        self.assertEqual(pattern[6][1].get_suit_rank(), 2)
        self.assertEqual(pattern[6][2].get_suit_rank(), 3)
        self.assertEqual(pattern[6][3].get_suit_rank(), 0)
        self.assertEqual(pattern[6][4].get_suit_rank(), 1)

    def test_cards2(self):

        h1     = [roomai.abstract.PokerCard(7, 0), roomai.abstract.PokerCard(7, 1)]
        keep   = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(4,2),roomai.abstract.PokerCard(5,3),roomai.abstract.PokerCard(6,0),roomai.abstract.PokerCard(7,2)]
        pattern = TexasHoldemEnv.cards2pattern(h1, keep)
        self.assertEqual(pattern[0],"3_1_1")


    def test_cards(self):
        handcards1 = [roomai.abstract.PokerCard(0,0),roomai.abstract.PokerCard(0,1)]
        handcards2 = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(3,2)]
        keepcards  = [roomai.abstract.PokerCard(0,2),roomai.abstract.PokerCard(0,3),roomai.abstract.PokerCard(2,0),roomai.abstract.PokerCard(2,1),roomai.abstract.PokerCard(3,3)]
        pattern = TexasHoldemEnv.cards2pattern(handcards1, keepcards)
        self.assertEqual(pattern[0],'4_1')
        self.assertEqual(pattern[1],False)
        self.assertEqual(pattern[2],True)
        self.assertEqual(pattern[3],False)
        self.assertEqual(pattern[4][0], 4)
        self.assertEqual(pattern[4][1], 1)
        self.assertEqual(pattern[6][0].get_point_rank(), 0)
        self.assertEqual(pattern[6][1].get_point_rank(), 0)
        self.assertEqual(pattern[6][2].get_point_rank(), 0)
        self.assertEqual(pattern[6][3].get_point_rank(), 0)
        self.assertEqual(pattern[6][4].get_point_rank(), 3)

        self.assertEqual(pattern[6][0].get_suit_rank(), 0)
        self.assertEqual(pattern[6][1].get_suit_rank(), 1)
        self.assertEqual(pattern[6][2].get_suit_rank(), 2)
        self.assertEqual(pattern[6][3].get_suit_rank(), 3)
        self.assertEqual(pattern[6][4].get_suit_rank(), 3)


        pattern1 = TexasHoldemEnv.cards2pattern(handcards1, keepcards)
        pattern2 = TexasHoldemEnv.cards2pattern(handcards2, keepcards)

        diff = TexasHoldemEnv.compare_handcards(handcards1, handcards2, keepcards)
        self.assertTrue(diff > 0)


    def test_available_actions(self):
        env = TexasHoldemEnv()
        env.init()

        actions = TexasHoldemEnv.available_actions(env.public_state)
        self.assertTrue("allin_1000" in actions)

        env.public_state.raise_account = 200
        actions = TexasHoldemEnv.available_actions(env.public_state)
        self.assertTrue("call_10" in actions)
        self.assertTrue("raise_210" in actions)
        self.assertTrue("raise_410" in actions)
        self.assertTrue("raise_410" in actions)
        self.assertTrue("raise_810" in actions)
        self.assertTrue("allin_1000" in actions)
        for key in actions:
            act = actions[key]
            print act.get_key()
            self.assertTrue(TexasHoldemEnv.is_action_valid(env.public_state, act))



    def test_is_action_valid(self):
        env = TexasHoldemEnv()
        env.init()


        print TexasHoldemAction.AllIn
        action = TexasHoldemAction("allin_1000")
        print action.get_key()
        self.assertTrue(env.is_action_valid(env.public_state,action))


    def test_compare(self):
        h1 = [roomai.abstract.PokerCard(7, 0), roomai.abstract.PokerCard(7, 1)]
        h2 = [roomai.abstract.PokerCard(2, 0), roomai.abstract.PokerCard(2, 1)]
        h3 = [roomai.abstract.PokerCard(2, 2), roomai.abstract.PokerCard(2, 3)]
        k  = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(4,2),roomai.abstract.PokerCard(5,3),roomai.abstract.PokerCard(6,0),roomai.abstract.PokerCard(7,2)]

        p1 = TexasHoldemEnv.cards2pattern(h1, k)
        p2 = TexasHoldemEnv.cards2pattern(h2, k)
        p3 = TexasHoldemEnv.cards2pattern(h3, k)
        print TexasHoldemEnv.compare_patterns(p1, p2)
        print TexasHoldemEnv.compare_patterns(p2, p3)

