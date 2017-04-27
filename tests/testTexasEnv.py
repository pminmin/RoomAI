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
        self.assertEqual(infos[0].person_state.id,0)
        env.private_state.hand_cards[0] = [Card(0, 0), Card(0, 1)]
        env.private_state.hand_cards[0] = [Card(2, 0), Card(2, 1)]
        env.private_state.hand_cards[0] = [Card(2, 0), Card(2, 1)]
        env.private_state.keep_cards    = [Card(3,0),  Card(4,0),Card(5,0),Card(6,0),Card(7,0)]
        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].person_state.available_actions),0 )
        self.assertTrue("allin_100" in infos[0].person_state.available_actions.keys())
        # dealer_id = 0
        # turn = 0
        # chips:100, 90, 80
        # bets :0,   10,  20
        # state:n,   n,  n

        action = Action_Texas("allin",100)
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(env.public_state.turn, 1)
        self.assertNotEqual(len(infos[1].person_state.available_actions),0 )
        self.assertTrue("allin_90" in infos[1].person_state.available_actions.keys())
        self.assertEqual(env.public_state.turn, 1)
        self.assertEqual(env.chips[0],0)
        self.assertEqual(env.chips[1],90)
        self.assertEqual(env.public_state.stage, StageSpace.firstStage)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  n,  n

        action = Action_Texas("fold",0)
        isTerminal, scores, infos = env.forward(action)
        # dealer_id = 0
        # turn = 2
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.public_state.turn, 2)

        action = Action_Texas("fold", 0)
        isTerminal, scores, infos = env.forward(action)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        print isTerminal
        print env.public_state.bets
        print env.public_state.is_allin
        print env.public_state.is_quit
        print env.public_state.chips
        print scores
        print env.public_state.turn
        self.assertEqual(env.public_state.turn, -1)
        self.assertTrue(isTerminal)
        self.assertEqual(scores[0], 30)
        self.assertEqual(scores[1], -10)
        self.assertEqual(scores[2], -20)

    def testEnv3Players2(self):
        roomai.set_level(logging.DEBUG)

        env = TexasHoldemEnv()
        env.num_players   = 3
        env.dealer_id     = 0
        env.chips         = [100, 500,1000]
        env.big_blind_bet = 20
        players =  [TexasHoldemRandomPlayer() for i in xrange(3)]

        isTerminal, scores, infos = env.init()
        self.assertEqual(infos[0].person_state.id,0)
        env.private_state.hand_cards[0] = [Card(7, 0), Card(7, 1)]
        env.private_state.hand_cards[1] = [Card(2, 0), Card(2, 1)]
        env.private_state.hand_cards[2] = [Card(2, 2), Card(2, 3)]
        env.private_state.keep_cards    = [Card(3,1),Card(4,2),Card(5,3),Card(6,0),Card(7,3)]
        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].person_state.available_actions),0 )
        self.assertTrue("raise_60" in infos[0].person_state.available_actions.keys())
        self.assertEqual(env.public_state.raise_account, 20)
        # dealer_id = 0
        # turn = 0
        # chips:100, 490, 980
        # bets :0,   10,  20
        # state:n,   n,  n
        # flag_next:0
        # raise_account: 20

        action = Action_Texas("raise", 60)
        isTerminal, scores, infos = env.forward(action)
        print env.public_state.num_expected_to_action, env.public_state.is_expected_to_action
        self.assertEqual(env.public_state.turn, 1)
        self.assertTrue("raise_60" not in infos[1].person_state.available_actions)
        self.assertTrue("raise_80" not in infos[1].person_state.available_actions)
        self.assertEqual(env.public_state.raise_account, 40)
        action = Action_Texas("call", 40)
        self.assertRaises(ValueError, env.forward, action)
        # dealer_id = 0
        # turn  = 1
        # stage = 1
        # chips:40,   490, 980
        # bets :60,   10,  20
        # state:n,   n,  n
        # raise_account: 40


        action = Action_Texas("call", 50)
        isTerminal, scores, infos = env.forward(action)
        print env.public_state.num_expected_to_action, env.public_state.is_expected_to_action
        # dealer_id = 0
        # turn  = 2
        # stage = 1
        # chips:40,   450, 980
        # bets :60,   50,  20
        # state:n,   n,  n
        # raise_account: 40
        # expected:f,f,t

        action = Action_Texas("call", 40)
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(infos[0].public_state.stage,StageSpace.secondStage)
        self.assertEqual(env.public_state.chips[1],440)
        self.assertEqual(env.public_state.turn, 1)
        # dealer_id = 0
        # turn  = 1
        # stage = 2
        # chips:40,   440, 940
        # bets :60,   60,  60
        # state:n,   n,  n
        # raise_account: 40

        action = Action_Texas("call",0)
        isTerminal, scores, infos = env.forward(action)
        isTerminal, scores, infos = env.forward(action)
        isTerminal, scores, infos = env.forward(action)
        self.assertEqual(env.public_state.stage,3)
        self.assertEqual(len(env.public_state.public_cards),4)
        p = 0
        tmp = [Card(3,1),Card(4,2),Card(5,3),Card(6,0)]
        for c in env.public_state.public_cards:
            self.assertEqual(c.toString(), tmp[p].toString())
            p += 1
        self.assertEqual(env.public_state.raise_account, 40)
        self.assertEqual(env.public_state.stage, 3)
        self.assertEqual(env.public_state.turn, 1)
        print "1",infos[1].person_state.available_actions.keys()
        # dealer_id = 0
        # turn  = 1
        # stage = 3
        # chips:40,  440, 940
        # bets :60,   60,  60
        # state:n,   n,  n
        # raise_account: 40

        action = Action_Texas("allin",440)
        isTerminal, score, infos = env.forward(action)
        self.assertEqual(infos[0].public_state.max_bet, 500)
        print "2", infos[2].person_state.available_actions.keys()
        self.assertEqual(env.public_state.is_allin[1],True)
        self.assertEqual(infos[0].public_state.stage, 3)
        # dealer_id = 0
        # turn  = 2
        # stage = 3
        # chips:40,   0, 940
        # bets :60,   500,  60
        # state:n,   n,  n
        # raise_account: 40

        action = Action_Texas("call",440)
        isTerminal, scores, infos = env.forward(action)
        action = Action_Texas("allin",40)
        isTerminal, scores, infos = env.forward(action)
        # dealer_id = 0
        # chips:0,     0,    500
        # bets :100,   500,  500
        # 0 > 1 = 2
        self.assertEqual(scores[0],200)
        self.assertEqual(scores[1],-100)
        self.assertEqual(scores[2],-100)



    def testEnv2players(self):
        env = TexasHoldemEnv()
        env.num_players = 2