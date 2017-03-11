#!/bin/python
import roomai
import roomai.doudizhu
import unittest

class DouDiZhuPokerRandomPlayerTester(unittest.TestCase):
    
    def testPlayersRepeat(self):
        for i in xrange(10000):
            self.testPlayers()

    def testPlayers(self):

        players = [roomai.createPlayer("DouDiZhuRandomPlayer") for i in xrange(3)]
        env     = roomai.createEnv("DouDiZhuEnv")

        isTerminal, _, infos = env.init(players)

        for i in xrange(len(players)):
            players[i].receiveInfo(infos[i])

        count = 0
        while isTerminal == False: 
            turn = infos[-1].public_state.turn 
        
            action = players[turn].takeAction()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receiveInfo(infos[i])

            count += 1
            if count > 10000:
                raise Exception("A round has more than 10000 epoches")

        print scores

