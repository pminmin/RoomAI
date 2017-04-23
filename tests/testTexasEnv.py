#!/bin/python
import unittest

from roomai.texas import *

class TexasEnvTester(unittest.TestCase):
    def testEnv3players(self):
        env = TexasHoldemEnv()
        env.num_players = 3

        isTerminal, scores, infos = env.init()
        self.assertEqual(infos[0].init_player_id,0)



    def testEnv2players(self):
        env = TexasHoldemEnv()
        env.num_players = 2