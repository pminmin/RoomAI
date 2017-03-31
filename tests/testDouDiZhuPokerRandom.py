#!/bin/python
import roomai
import roomai.doudizhu
import unittest

class DouDiZhuPokerRandomPlayerTester(unittest.TestCase):


    def testPlayers(self):

        players = [roomai.doudizhu.DouDiZhuPokerRandomPlayer() for i in xrange(3)]
        env     = roomai.doudizhu.DouDiZhuPokerEnv()
        scores  = env.round(env,players,1000)
        print (scores)
        self.assertTrue(abs(scores[0] -scores[1]) < 0.2)
        self.assertTrue(abs(scores[1] -scores[2]) < 0.2)

