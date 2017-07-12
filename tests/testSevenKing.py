#!/bin/python
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingAction
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



