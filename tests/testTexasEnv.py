#!/bin/python
import unittest
import logging

from roomai.texas import *
import roomai

class TexasEnvTester(unittest.TestCase):
    def testEnv3players(self):
        roomai.set_level(logging.DEBUG)

        env = TexasHoldemEnv()
        env.num_players   = 3
        env.dealer_id     = 0
        env.chips         = [100,100,100]
        env.big_blind_bet = 20
        players =  [TexasHoldemRandomPlayer() for i in xrange(3)]

        isTerminal, scores, infos = env.init()
        self.assertEqual(infos[0].init_player_id,0)
        env.private_state.hand_cards[0] = [Card(0, 0), Card(0, 1)]
        env.private_state.hand_cards[0] = [Card(2, 0), Card(2, 1)]
        env.private_state.hand_cards[0] = [Card(2, 0), Card(2, 1)]
        env.private_state.keep_cards[0] = [Card(3,0),Card(4,0),Card(5,0),Card(6,0),Card(7,0)]
        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].available_actions),0 )
        self.assertTrue("allin_100" in infos[0].available_actions.keys())
        # dealer_id = 0
        # turn = 0
        # chips:100, 90, 80
        # bets :0,   10,  20
        # state:n,   n,  n

        action = Action("allin",100)
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(env.public_state.turn, 1)
        self.assertNotEqual(len(infos[1].available_actions),0 )
        self.assertTrue("allin_90" in infos[1].available_actions.keys())
        self.assertEqual(env.public_state.turn, 1)
        self.assertEqual(env.chips[0],0)
        self.assertEqual(env.chips[1],90)
        self.assertEqual(env.public_state.stage, StageSpace.firstStage)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  n,  n

        action = Action("fold",0)
        isTerminal, scores, infos = env.forward(action)
        # dealer_id = 0
        # turn = 2
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.public_state.turn, 2)

        action = Action("fold", 0)
        isTerminal, scores, infos = env.forward(action)
        # dealer_id = 0
        # turn = 0
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.public_state.turn, 0)
        print isTerminal
        print env.public_state.bets
        print env.public_state.is_allin
        print env.public_state.is_quit
        print env.public_state.chips
        print scores
        self.assertTrue(isTerminal)
        self.assertEqual(scores[0], 30)
        self.assertEqual(scores[1], -10)
        self.assertEqual(scores[2], -20)



    def testEnv2players(self):
        env = TexasHoldemEnv()
        env.num_players = 2