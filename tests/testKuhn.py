import unittest
import roomai.kuhn

class KuhnTester(unittest.TestCase):
    def testKuhn(self):
        for i in xrange(1000):
            players = [roomai.kuhn.KuhnPokerAlwaysBetPlayer() for i in xrange(2)]
            env     = roomai.kuhn.KuhnPokerEnv()

            isTerminal, _, infos = env.init()

            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

            while isTerminal == False:
                turn = infos[-1].public_state.turn
                action = players[turn].take_action()

                isTerminal, scores, infos = env.forward(action)
                for i in xrange(len(players)):
                    players[i].receive_info(infos[i])

