#!/bin/python
import unittest
import roomai.fivecardstud

class FiveCardStudUtils(unittest.TestCase):
    def test(self):
        public_state = roomai.fivecardstud.FiveCardStudPublicState()
        public_state.num_players  = 3
        public_state.round        = 1
        public_state.public_cards = [[roomai.fivecardstud.FiveCardStudPokerCard("2_Spade"),\
                                     roomai.fivecardstud.FiveCardStudPokerCard("3_Spade"), \
                                     roomai.fivecardstud.FiveCardStudPokerCard("r_Spade")]]
        turn = roomai.fivecardstud.FiveCardStudEnv.choose_player_at_begining_of_round(public_state)
        print turn
        assert(turn == 2)

    def test1(self):
        public_cards = [[roomai.fivecardstud.FiveCardStudPokerCard("2_Spade"),\
                                     roomai.fivecardstud.FiveCardStudPokerCard("3_Spade"), \
                                     roomai.fivecardstud.FiveCardStudPokerCard("r_Spade")]]
        public_cards.sort(roomai.fivecardstud.FiveCardStudPokerCard.compare)
        for i in xrange(len(public_cards[0])):
            print public_cards[0][i].get_key()
