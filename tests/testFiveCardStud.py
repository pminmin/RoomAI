#!/bin/python
from roomai.fivecardstud import FiveCardStudEnv
from roomai.fivecardstud import FiveCardStudPokerCard
from roomai.fivecardstud import FiveCardStudAction
import unittest

class FiveCardStudTester(unittest.TestCase):
    def test(self):
        env = FiveCardStudEnv();
        env.init()

    def testCase(self):

        cards   =[FiveCardStudPokerCard("3_Spade"), FiveCardStudPokerCard("4_Spade"),FiveCardStudPokerCard("5_Spade"),FiveCardStudPokerCard("6_Spade")]
        pattern = FiveCardStudEnv.fourcards2pattern(cards)
        assert(pattern[0] =="Straight_SameSuit")

        cards = [FiveCardStudPokerCard("3_Spade"), FiveCardStudPokerCard("4_Spade"), FiveCardStudPokerCard("5_Spade"),
                 FiveCardStudPokerCard("6_Spade")]


    def testEnv(self):
        env = FiveCardStudEnv();
        infos, pu, pes, pr = env.init()

        turn = pu.turn
        assert(pes[turn].available_actions is not None)
        print pes[turn].available_actions
        available_actions = pes[turn].available_actions
        assert("Call_0" not in available_actions)
        assert("Fold_0" in available_actions)
        assert("Check_0"  in available_actions)

        showhand_act_key = ""
        for act_str in available_actions:
            if "Showhand" in act_str:
                showhand_act_key = act_str

        env.forward(FiveCardStudAction(showhand_act_key))
        env.forward(FiveCardStudAction(showhand_act_key))
        env.forward(FiveCardStudAction(showhand_act_key))

        assert(env.public_state.is_terminal == True)



