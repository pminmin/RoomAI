#!/bin/python
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingRandomPlayer
import roomai.common
import unittest

class AlwaysFoldPlayer(roomai.common.AbstractPlayer):
    def take_action(self):
        return SevenKingAction("")
    def receive_info(self,info):
        pass
    def reset(self):
        pass

class AlwaysNotFoldPlayer(roomai.common.AbstractPlayer):
    def take_action(self):
        for a in self.available_actions.values():
            if a.key != "":
                print "take a action=",a.key
                return a
        print "len=",len(self.available_actions)

    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    def reset(self):
        pass



class testSevenKing(unittest.TestCase):
    def show_hand_card(self,hand_card):
        str = ""
        for c in hand_card:
            str += "," + c.key
        print (str)
    def testEnv(self):
        env = SevenKingEnv()
        env.num_players = 2

        infos, public_state, person_states, private_state = env.init()
        assert(len(infos) == 2)
        turn = public_state.turn
        self.show_hand_card(person_states[turn].hand_card)
        print (turn)
        print ("available_actions=",person_states[turn].available_actions.keys())
        print ("available_actions_v=",person_states[turn].available_actions.values())


        action = SevenKingAction("%s,%s" % (person_states[turn].hand_card[0].key, person_states[turn].hand_card[1].key))
        infos, public_state, person_states, private_state = env.forward(action)

    def testRandom(self):
        env = SevenKingEnv()
        env.num_players = 2

        players = [SevenKingRandomPlayer() for i in xrange(2)]

        for i in range(1000):
            SevenKingEnv.compete(env, players)




    def testScores(self):
        env = SevenKingEnv()
        env.num_players = 3

        players = [AlwaysFoldPlayer(), AlwaysFoldPlayer(), AlwaysNotFoldPlayer()]
        scores  = env.compete(env, players)
        print scores
        0/0

