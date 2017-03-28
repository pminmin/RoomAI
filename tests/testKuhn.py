import unittest
import roomai.kuhn

class KuhnTester(unittest.TestCase):
    def testKuhn(self):
        players = [roomai.kuhn.KuhnPokerAlwaysBetPlayer() for i in xrange(3)]
        env     = roomai.kuhn.KuhnPokerEnv()

        isTerminal, _, infos = env.init()

        for i in xrange(len(players)):
            players[i].receiveInfo(infos[i])

        count = 0
        while isTerminal == False:
            turn = infos[-1].public_state.turn
            actions = [roomai.kuhn.ActionSpace.cheat, roomai.kuhn.ActionSpace.bet]
            action = players[turn].takeAction()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receiveInfo(infos[i])

            count += 1
            if count > 10000:
                raise Exception("A round has more than 10000 epoches")
