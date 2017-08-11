#!/bin/python
from roomai.sevenking import SevenKingEnv
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingRandomPlayer
from roomai.sevenking import SevenKingPokerCard
import roomai.common
import unittest

class AlwaysFoldPlayer(roomai.common.AbstractPlayer):
    def take_action(self):



        if "" not in self.available_actions:
            min_card = None
            for a in self.available_actions.values():
                if a.pattern[0] == "p_0":
                    if min_card is None:    min_card = a.hand_card[0]
                    else:
                        card = a.hand_card[0]
                        if SevenKingPokerCard.compare(card, min_card) < 0 : min_card = card
            if min_card is None:
                return self.available_actions.values()[0]
            else:
                return SevenKingAction.lookup(min_card.key)
        else:
            return SevenKingAction("")

    def receive_info(self,info):
        self.public_state      = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        pass

class AlwaysNotFoldPlayer(roomai.common.AbstractPlayer):
    def take_action(self):
        for a in self.available_actions.values():
            if a.key != "":
                return a
        return SevenKingAction.lookup("")

    def receive_info(self, info):
        self.available_actions = info.person_state.available_actions

    def reset(self):
        pass



class testSevenKing(unittest.TestCase):

    def show_hand_card(self,hand_card):
        print (",".join([c.key for c in hand_card]))
    def testEnv(self):
        env = SevenKingEnv()
        env.num_players = 2

        infos, public_state, person_states, private_state = env.init()
        assert(len(infos) == 2)
        turn = public_state.turn
        self.show_hand_card(person_states[turn].hand_cards)
        print (turn)
        print ("available_actions=",person_states[turn].available_actions.keys())
        print ("available_actions_v=",person_states[turn].available_actions.values())


        action = SevenKingAction("%s,%s" % (person_states[turn].hand_cards[0].key, person_states[turn].hand_cards[1].key))
        infos, public_state, person_states, private_state = env.forward(action)


    def testRandom(self):
        env = SevenKingEnv()
        env.num_players = 2
        players = [SevenKingRandomPlayer() for i in xrange(2)]

        for i in range(100):
            SevenKingEnv.compete(env, players)




    def testScores(self):
        env = SevenKingEnv()
        env.num_players = 3

        print "aaa"
        players = [AlwaysFoldPlayer(), AlwaysFoldPlayer(), AlwaysNotFoldPlayer()]
        scores  = env.compete(env, players)
        print scores


