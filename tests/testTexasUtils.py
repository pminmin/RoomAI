#!/bin/python
import unittest
from roomai.texas import Card
from roomai.texas import Utils
from roomai.texas import Action
from roomai.texas import TexasHoldemEnv
from roomai.texas import OptionSpace

class TexasUtilsTester(unittest.TestCase):

    def test_cards1(self):
        handcards1 = [Card(0,0),Card(0,1)]
        handcards2 = [Card(3,1),Card(3,2)]
        keepcards  = [Card(0,2),Card(0,3),Card(2,0),Card(2,1),Card(3,3)]
        pattern = Utils.cards2pattern(handcards2,keepcards)

        self.assertEqual(pattern[0],'3_2')
        self.assertEqual(pattern[1],False)
        self.assertEqual(pattern[2],True)
        self.assertEqual(pattern[3],False)
        self.assertEqual(pattern[4][0], 3)
        self.assertEqual(pattern[4][1], 2)
        for c in pattern[6]:
            print c.toString()
        self.assertEqual(pattern[6][0].point, 3)
        self.assertEqual(pattern[6][1].point, 3)
        self.assertEqual(pattern[6][2].point, 3)
        self.assertEqual(pattern[6][3].point, 2)
        self.assertEqual(pattern[6][4].point, 2)

        self.assertEqual(pattern[6][0].suit, 1)
        self.assertEqual(pattern[6][1].suit, 2)
        self.assertEqual(pattern[6][2].suit, 3)
        self.assertEqual(pattern[6][3].suit, 0)
        self.assertEqual(pattern[6][4].suit, 1)

    def test_cards2(self):
        h1     = [Card(7, 0), Card(7, 1)]
        keep   = [Card(3,1),Card(4,2),Card(5,3),Card(6,0),Card(7,2)]
        pattern = Utils.cards2pattern(h1,keep)
        self.assertEqual(pattern[0],"3_1_1")


    def test_cards(self):
        handcards1 = [Card(0,0),Card(0,1)]
        handcards2 = [Card(3,1),Card(3,2)]
        keepcards  = [Card(0,2),Card(0,3),Card(2,0),Card(2,1),Card(3,3)]
        pattern = Utils.cards2pattern(handcards1, keepcards)
        self.assertEqual(pattern[0],'4_1')
        self.assertEqual(pattern[1],False)
        self.assertEqual(pattern[2],True)
        self.assertEqual(pattern[3],False)
        self.assertEqual(pattern[4][0], 4)
        self.assertEqual(pattern[4][1], 1)
        for c in pattern[6]:
            print c.toString()
        self.assertEqual(pattern[6][0].point, 0)
        self.assertEqual(pattern[6][1].point, 0)
        self.assertEqual(pattern[6][2].point, 0)
        self.assertEqual(pattern[6][3].point, 0)
        self.assertEqual(pattern[6][4].point, 3)

        self.assertEqual(pattern[6][0].suit, 0)
        self.assertEqual(pattern[6][1].suit, 1)
        self.assertEqual(pattern[6][2].suit, 2)
        self.assertEqual(pattern[6][3].suit, 3)
        self.assertEqual(pattern[6][4].suit, 3)

        pattern1 = Utils.cards2pattern(handcards1,keepcards)
        pattern2 = Utils.cards2pattern(handcards2,keepcards)

        diff = Utils.compare_handcards(handcards1,handcards2,keepcards)
        self.assertTrue(diff > 0)


    def test_available_actions(self):
        env = TexasHoldemEnv()
        env.init()
        actions = Utils.available_actions(env.public_state)
        self.assertTrue("allin_1000" in actions)

        env.public_state.raise_account = 200
        actions = Utils.available_actions(env.public_state)
        self.assertTrue("call_10" in actions)
        self.assertTrue("raise_210" in actions)
        self.assertTrue("raise_410" in actions)
        self.assertTrue("raise_410" in actions)
        self.assertTrue("raise_810" in actions)
        self.assertTrue("allin_1000" in actions)
        for key in actions:
            act = actions[key]
            print act.toString()
            self.assertTrue(Utils.is_action_valid(env.public_state, act))
            self.assertTrue(env.is_action_valid(act))


    def test_is_action_valid(self):
        env = TexasHoldemEnv()
        env.init()

        print OptionSpace.AllIn
        action = Action("allin",1000)
        print action.toString()
        self.assertTrue(env.is_action_valid(action))


    def test_compare(self):
        h1 = [Card(7, 0), Card(7, 1)]
        h2 = [Card(2, 0), Card(2, 1)]
        h3 = [Card(2, 2), Card(2, 3)]
        k  = [Card(3,1),Card(4,2),Card(5,3),Card(6,0),Card(7,2)]

        p1 = Utils.cards2pattern(h1,k)
        p2 = Utils.cards2pattern(h2,k)
        p3 = Utils.cards2pattern(h3,k)
        print Utils.compare_patterns(p1,p2)
        print Utils.compare_patterns(p2,p3)
        0/0