#!/bin/python
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingRandomPlayer
import unittest

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

        for i in range(10):
            SevenKingEnv.compete(env, players)






