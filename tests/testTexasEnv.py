#!/bin/python
import unittest
import logging

from roomai.texas import *
import roomai
import random
from roomai.common import RandomPlayer

class TexasEnvTester(unittest.TestCase):
    """
    """

    def testEnv3players(self):
        """

        """
        env = TexasHoldemEnv()
        num_players   = 3
        dealer_id     = 0
        chips         = [100,100,100]
        big_blind_bet = 20
        params  = {"num_players":num_players, "dealer_id":dealer_id, "chips":chips, "big_blind_bet":big_blind_bet}
        players =  [RandomPlayer() for i in range(3)]


        infos,public_state, person_states, private_state  = env.init(params)
        self.assertEqual(infos[0].person_state.id,0)
        env.person_states[0].__hand_cards__ = [roomai.common.PokerCard(0, 0), roomai.common.PokerCard(0, 1)]
        env.person_states[0].__hand_cards__ = [roomai.common.PokerCard(2, 0), roomai.common.PokerCard(2, 1)]
        env.person_states[0].__hand_cards__ = [roomai.common.PokerCard(2, 0), roomai.common.PokerCard(2, 1)]
        env.private_state.__keep_cards__    = [roomai.common.PokerCard(3,0),  roomai.common.PokerCard(4,0),roomai.common.PokerCard(5,0),roomai.common.PokerCard(6,0),roomai.common.PokerCard(7,0)]

        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].person_state.available_actions), 0)
        self.assertTrue("Allin_100" in infos[0].person_state.available_actions.keys())
        # dealer_id = 0
        # turn = 0
        # chips:100, 90, 80
        # bets :0,   10,  20
        # state:n,   n,  n


        action = TexasHoldemAction("Allin_100")
        infos,public_state, person_states, private_state  = env.forward(action)
        self.assertEqual(env.public_state.turn, 1)
        self.assertNotEqual(len(infos[1].person_state.available_actions), 0)
        self.assertTrue("Allin_90" in infos[1].person_state.available_actions.keys())
        self.assertEqual(env.public_state.turn, 1)
        self.assertEqual(env.public_state.chips[0],0)
        self.assertEqual(env.public_state.chips[1],90)
        self.assertEqual(env.public_state.stage, StageSpace.firstStage)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  n,  n


        action = TexasHoldemAction("Fold_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # turn = 2
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        self.assertEqual(env.public_state.turn, 2)


        action = TexasHoldemAction("Fold_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # turn = 1
        # chips:0,   90, 80
        # bets :100, 10, 20
        # state:all,  q,  n
        print (env.public_state.bets)
        print (env.public_state.is_allin)
        print (env.public_state.is_fold)
        print (env.public_state.chips)
        print (env.public_state.turn)
        self.assertTrue(public_state.is_terminal)
        self.assertEqual(public_state.scores[0], 30.0/public_state.big_blind_bet)
        self.assertEqual(public_state.scores[1], -10.0/public_state.big_blind_bet)
        self.assertEqual(public_state.scores[2], -20.0/public_state.big_blind_bet)

    def testEnv3Players2(self):
        """

        """

        env = TexasHoldemEnv()
        num_players   = 3
        dealer_id     = 0
        chips         = [100, 500,1000]
        big_blind_bet = 20
        params  = {"num_players":num_players, "dealer_id":dealer_id, "chips":chips, "big_blind_bet":big_blind_bet}
        players =  [RandomPlayer() for i in range(3)]


        infos,public_state, person_states, private_state = env.init(params)
        self.assertEqual(infos[0].person_state.id,0)
        env.person_states[0].__hand_cards__ = [roomai.common.PokerCard(7, 0), roomai.common.PokerCard(7, 1)]
        env.person_states[1].__hand_cards__ = [roomai.common.PokerCard(2, 0), roomai.common.PokerCard(2, 1)]
        env.person_states[2].__hand_cards__ = [roomai.common.PokerCard(2, 2), roomai.common.PokerCard(2, 3)]
        env.private_state.__keep_cards__    = [roomai.common.PokerCard(3,1),roomai.common.PokerCard(4,2),roomai.common.PokerCard(5,3),roomai.common.PokerCard(6,0),roomai.common.PokerCard(7,3)]
        self.assertEqual(env.public_state.turn, 0)
        self.assertNotEqual(len(infos[0].person_state.available_actions), 0)
        self.assertTrue("Raise_60" in infos[0].person_state.available_actions.keys())
        self.assertEqual(env.public_state.raise_account, 20)
        # dealer_id = 0
        # turn = 0
        # chips:100, 490, 980
        # bets :0,   10,  20
        # state:n,   n,  n
        # flag_next:0
        # raise_account: 20


        action = TexasHoldemAction("Raise_60")
        infos,public_state, person_states, private_state  = env.forward(action)
        print (env.public_state.num_needed_to_action, env.public_state.is_needed_to_action)
        self.assertEqual(env.public_state.turn, 1)
        self.assertTrue("Raise_60" not in infos[1].person_state.available_actions)
        self.assertTrue("Raise_80" not in infos[1].person_state.available_actions)
        self.assertEqual(env.public_state.raise_account, 40)
        action = TexasHoldemAction("Call_40")
        self.assertRaises(ValueError, env.forward, action)
        # dealer_id = 0
        # turn  = 1
        # stage = 1
        # chips:40,   490, 980
        # bets :60,   10,  20
        # state:n,   n,  n
        # raise_account: 40



        action = TexasHoldemAction("Call_50")
        infos,public_state, person_states, private_state  = env.forward(action)
        assert(public_state.stage == StageSpace.firstStage)
        print (env.public_state.num_needed_to_action, env.public_state.is_needed_to_action)
        print (public_state.stage)
        print (public_state.chips)
        print (public_state.bets)
        print (public_state.dealer_id)
        # dealer_id = 0
        # turn  = 2
        # stage = 1
        # chips:40,   440, 980
        # bets :60,   60,  20
        # state:n,   n,  n
        # raise_account: 40
        # expected:f,f,t

        action = TexasHoldemAction("Call_40")
        infos,public_state, person_states, private_state  = env.forward(action)
        print ("\n\n")
        print ("stage",public_state.stage)
        print ("dealer_id+1", (public_state.dealer_id+1)%public_state.num_players)
        print ("is_needed_to_action", public_state.is_needed_to_action)
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


        action = TexasHoldemAction("Check_0")
        infos,public_state, person_states, private_state  = env.forward(action)
        infos,public_state, person_states, private_state  = env.forward(action)
        infos,public_state, person_states, private_state  = env.forward(action)
        self.assertEqual(env.public_state.stage,3)
        self.assertEqual(len(env.public_state.public_cards),4)
        p = 0
        tmp = [roomai.common.PokerCard(3,1),roomai.common.PokerCard(4,2),roomai.common.PokerCard(5,3),roomai.common.PokerCard(6,0)]
        self.assertEqual(env.public_state.raise_account, 40)
        self.assertEqual(env.public_state.stage, 3)
        self.assertEqual(env.public_state.turn, 1)
        print ("1",infos[1].person_state.available_actions.keys())
        # dealer_id = 0
        # turn  = 1
        # stage = 3
        # chips:40,  440, 940
        # bets :60,   60,  60
        # state:n,   n,  n
        # raise_account: 40


        action = TexasHoldemAction("Allin_440")
        infos,public_state, person_states, private_state  = env.forward(action)
        self.assertEqual(infos[0].public_state.max_bet_sofar, 500)
        print ("2", infos[2].person_state.available_actions.keys())
        self.assertEqual(env.public_state.is_allin[1],True)
        self.assertEqual(infos[0].public_state.stage, 3)
        # dealer_id = 0
        # turn  = 2
        # stage = 3
        # chips:40,   0, 940
        # bets :60,   500,  60
        # state:n,   n,  n
        # raise_account: 40


        action = TexasHoldemAction("Call_440")
        infos,public_state, person_states, private_state  = env.forward(action)
        action = TexasHoldemAction("Allin_40")
        infos,public_state, person_states, private_state  = env.forward(action)
        # dealer_id = 0
        # chips:0,     0,    500
        # bets :100,   500,  500
        # 0 > 1 = 2
        self.assertEqual(public_state.scores[0],200.0/public_state.big_blind_bet)
        self.assertEqual(public_state.scores[1],-100.0/public_state.big_blind_bet)
        self.assertEqual(public_state.scores[2],-100.0/public_state.big_blind_bet)



    def testEnv2players(self):
        """

        """
        env = TexasHoldemEnv()
        env.num_players = 2

    def testRandomPlayer(self):
        """

        """

        random.seed(0)

        for i in range(100):
            players = [RandomPlayer() for i in range(3)]

            env = TexasHoldemEnv()
            num_players = 3
            chips       = [1000 for i in range(num_players)]
            params = {"num_players": num_players,  "chips": chips}
            infos, public_state, person_states, private_state = env.init(params)

            while public_state.is_terminal != True:
                for i in range(3):
                    players[i].receive_info(infos[i])
                turn   = public_state.turn
                action = players[turn].take_action()

                infos, public_state, person_states, private_state = env.forward(action)



        for i in range(100):
            players = [RandomPlayer() for i in range(2)]

            env = TexasHoldemEnv()
            num_players = 2
            chips     = [1000 for i in range(num_players)]
            dealer_id = i%2
            params = {"num_players": num_players, "dealer_id": dealer_id, "chips": chips}
            infos, public_state, person_states, private_state = env.init(params)

            while public_state.is_terminal != True:
                for i in range(2):
                    players[i].receive_info(infos[i])
                turn   = public_state.turn
                action = players[turn].take_action()

                infos, public_state, person_states, private_state = env.forward(action)

    def testCompete(self):
        """

        """
        import random
        random.seed(100)
        players = [RandomPlayer() for i in range(5)]
        env = TexasHoldemEnv()

        scores = TexasHoldemEnv.compete(env, players)
        print (scores)

