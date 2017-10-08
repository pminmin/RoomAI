#!/bin/python
import unittest
import roomai.fivecardstud

class FiveCardStudUtils(unittest.TestCase):
    """
    """
    def test(self):
        """

        """
        public_state = roomai.fivecardstud.FiveCardStudPublicState()
        public_state.num_players      = 3
        public_state.round            = 1
        public_state.second_hand_cards= [roomai.fivecardstud.FiveCardStudPokerCard("2_Spade"), \
                                         roomai.fivecardstud.FiveCardStudPokerCard("3_Spade"), \
                                         roomai.fivecardstud.FiveCardStudPokerCard("A_Spade")]
        public_state.is_quit          = [False for i in range(public_state.num_players)]
        turn = roomai.fivecardstud.FiveCardStudEnv.choose_player_at_begining_of_round(public_state)
        print (turn)
        assert(turn == 2)

    def test1(self):
        """

        """
        from functools import cmp_to_key
        public_cards = [[roomai.fivecardstud.FiveCardStudPokerCard("2_Spade"),\
                                     roomai.fivecardstud.FiveCardStudPokerCard("3_Spade"), \
                                     roomai.fivecardstud.FiveCardStudPokerCard("A_Spade")]]
        public_cards.sort(key = cmp_to_key(roomai.fivecardstud.FiveCardStudPokerCard.compare))
        for i in range(len(public_cards[0])):
            print (public_cards[0][i].key)
