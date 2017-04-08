#!/bin/python
import roomai
import roomai.doudizhu
import unittest

class DouDiZhuPokerRandomPlayerTester(unittest.TestCase):


    def testPlayers(self):

        players = [roomai.doudizhu.DouDiZhuPokerRandomPlayer() for i in xrange(3)]
        env     = roomai.doudizhu.DouDiZhuPokerEnv()
        scores  = [0,0,0]
        for i in xrange(1000):
            new_scores  = env.round(env,players)
            for j in xrange(len(scores)):
                scores[j] += new_scores[j]
        for j in xrange(len(scores)):scores[j] /= 1000.0;
        print (scores)
        self.assertTrue(abs(scores[0] -scores[1]) < 0.2)
        self.assertTrue(abs(scores[1] -scores[2]) < 0.2)

