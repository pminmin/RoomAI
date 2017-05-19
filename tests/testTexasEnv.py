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


        infos,public_state, person_states, private_state  = env.init()
        self.assertEqual(infos[0].person_state.id,0)
        env.private_state.hand_cards[0] = [roomai.abstract.PokerCard(0, 0), roomai.abstract.PokerCard(0, 1)]
        env.private_state.hand_cards[0] = [roomai.abstract.PokerCard(2, 0), roomai.abstract.PokerCard(2, 1)]
        env.private_state.hand_cards[0] = [roomai.abstract.PokerCard(2, 0), roomai.abstract.PokerCard(2, 1)]
        env.private_state.keep_cards    = [roomai.abstract.PokerCard(3,0),  roomai.abstract.PokerCard(4,0),roomai.abstract.PokerCard(5,0),roomai.abstract.PokerCard(6,0),roomai.abstract.PokerCard(7,0)]

        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].person_state.available_actions),0 )
        self.assertTrue("allin_100" in infos[0].person_state.available_actions.keys())
        # dealer_id = 0
        # turn = 0
        # chips:100, 90, 80
        # bets :0,   10,  20
        # state:n,   n,  n


        action = TexasHoldemAction("allin_100")
        infos,public_state, person_states, private_state  = env.forward(action)
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


        action = TexasHoldemAction("fold_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # turn = 2
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.public_state.turn, 2)


        action = TexasHoldemAction("fold_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        print env.public_state.bets
        print env.public_state.is_allin
        print env.public_state.is_quit
        print env.public_state.chips
        print env.public_state.turn
        self.assertEqual(env.public_state.turn, -1)
        self.assertTrue(public_state.is_terminal)
        self.assertEqual(public_state.scores[0], 30)
        self.assertEqual(public_state.scores[1], -10)
        self.assertEqual(public_state.scores[2], -20)

    def testEnv3Players2(self):
        roomai.set_level(logging.DEBUG)

        env = TexasHoldemEnv()
        env.num_players   = 3
        env.dealer_id     = 0
        env.chips         = [100, 500,1000]
        env.big_blind_bet = 20
        players =  [TexasHoldemRandomPlayer() for i in xrange(3)]


        infos,public_state, person_states, private_state = env.init()
        self.assertEqual(infos[0].person_state.id,0)
        env.private_state.hand_cards[0] = [roomai.abstract.PokerCard(7, 0), roomai.abstract.PokerCard(7, 1)]
        env.private_state.hand_cards[1] = [roomai.abstract.PokerCard(2, 0), roomai.abstract.PokerCard(2, 1)]
        env.private_state.hand_cards[2] = [roomai.abstract.PokerCard(2, 2), roomai.abstract.PokerCard(2, 3)]
        env.private_state.keep_cards    = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(4,2),roomai.abstract.PokerCard(5,3),roomai.abstract.PokerCard(6,0),roomai.abstract.PokerCard(7,3)]
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


        action = TexasHoldemAction("raise_60")
        infos,public_state, person_states, private_state  = env.forward(action)
        print env.public_state.num_needed_to_action, env.public_state.is_needed_to_action
        self.assertEqual(env.public_state.turn, 1)
        self.assertTrue("raise_60" not in infos[1].person_state.available_actions)
        self.assertTrue("raise_80" not in infos[1].person_state.available_actions)
        self.assertEqual(env.public_state.raise_account, 40)
        action = TexasHoldemAction("call_40")
        self.assertRaises(ValueError, env.forward, action)
        # dealer_id = 0
        # turn  = 1
        # stage = 1
        # chips:40,   490, 980
        # bets :60,   10,  20
        # state:n,   n,  n
        # raise_account: 40



        action = TexasHoldemAction("call_50")
        infos,public_state, person_states, private_state  = env.forward(action)
        assert(public_state.stage, StageSpace.firstStage)
        print env.public_state.num_needed_to_action, env.public_state.is_needed_to_action
        print public_state.stage
        print public_state.chips
        print public_state.bets
        print public_state.dealer_id
        # dealer_id = 0
        # turn  = 2
        # stage = 1
        # chips:40,   440, 980
        # bets :60,   60,  20
        # state:n,   n,  n
        # raise_account: 40
        # expected:f,f,t

        action = TexasHoldemAction("call_40")
        infos,public_state, person_states, private_state  = env.forward(action)
        print "\n\n"
        print "stage",public_state.stage
        print "dealer_id+1", (public_state.dealer_id+1)%public_state.num_players
        print "is_needed_to_action", public_state.is_needed_to_action
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


        action = TexasHoldemAction("call_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        infos,public_state, person_states, private_state  = env.forward(action)
        infos,public_state, person_states, private_state  = env.forward(action)
        self.assertEqual(env.public_state.stage,3)
        self.assertEqual(len(env.public_state.public_cards),4)
        p = 0
        tmp = [roomai.abstract.PokerCard(3,1),roomai.abstract.PokerCard(4,2),roomai.abstract.PokerCard(5,3),roomai.abstract.PokerCard(6,0)]
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


        action = TexasHoldemAction("allin_440")
        infos,public_state, person_states, private_state  = env.forward(action)
        self.assertEqual(infos[0].public_state.max_bet_sofar, 500)
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


        action = TexasHoldemAction("call_440")
        infos,public_state, person_states, private_state  = env.forward(action)
        action = TexasHoldemAction("allin_40")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # chips:0,     0,    500
        # bets :100,   500,  500
        # 0 > 1 = 2
        self.assertEqual(public_state.scores[0],200)
        self.assertEqual(public_state.scores[1],-100)
        self.assertEqual(public_state.scores[2],-100)



    def testEnv2players(self):
        env = TexasHoldemEnv()
        env.num_players = 2

    def testRandomPlayer(self):
        import random
        random.seed(0)

        for i in xrange(100):
            players = [TexasHoldemRandomPlayer() for i in xrange(3)]

            env = TexasHoldemEnv()
            env.num_players = 3
            env.chips = [1000 for i in xrange(env.num_players)]
            infos, public_state, person_states, private_state = env.init()

            while public_state.is_terminal != True:
                for i in xrange(3):
                    players[i].receive_info(infos[i])
                turn   = public_state.turn
                action = players[turn].take_action()

                infos, public_state, person_states, private_state = env.forward(action)