#!/bin/python
import roomai.abstract
import copy
import random

from FiveCardStudUtils import FiveCardStudPokerCard
from FiveCardStudInfo import FiveCardStudPublicState
from FiveCardStudInfo import FiveCardStudPersonState
from FiveCardStudInfo import FiveCardStudPrivateState
from FiveCardStudInfo import FiveCardStudInfo

class FiveCardStudEnv(roomai.abstract.AbstractEnv):
    def __init__(self):
        num_players = 3
        self.logger         = roomai.get_logger()

    def gen_infos(self):
        infos = [FiveCardStudInfo() for i in xrange(4)]
        infos[3].private_state    = copy.deepcopy(self.private_state)
        for i in xrange(3):
            infos[i].person_state = copy.deepcopy(self.person_states[i])
        for i in xrange(4):
            infos[i].public_state = copy.deepcopy(self.public_state)

        return infos

    #@override
    def init(self):
        self.public_state   = FiveCardStudPublicState()
        self.private_state  = FiveCardStudPrivateState()
        self.person_states  = [FiveCardStudPersonState for i in xrange(3)]
        for i in xrange(self.num_players):
            self.person_states[i].id = i

        ## initialize the cards
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(FiveCardStudPokerCard(i, j))
        random.shuffle(allcards)
        self.private_state.first_hand_cards  = allcards[0:                  1*self.num_players]
        self.private_state.second_hand_cards = allcards[1*self.num_palyers, 2*self.num_players]
        self.private_state.third_hand_cards  = allcards[2*self.num_players, 3*self.num_players]
        self.private_state.fourth_hand_cards = allcards[3*self.num_palyers, 4*self.num_players]
        self.private_state.fifth_hand_cards  = allcards[4*self.num_palyers, 5*self.num_players]

        ##
        for i in xrange(self.num_players):
            self.person_states[i].first_hand_card = self.private_state.first_hand_cards[i]

        return False,[],self.gen_infos(), self.public_state, self.person_states, self.private_state


    #@override
    def forward(self, action):
        pass

    #@override
    def compete(cls, env, players):
        pass

############################################# Utils Function ######################################################
    @classmethod
    def available_actions(cls, public_state):
        pass


    @classmethod
    def cards2pattern(cls, cards):
        pointrank2cards = dict()
        for c in cards:
            if c.get_point_rank() in pointrank2cards:
                pointrank2cards[c.get_point_rank()].append(c)
            else:
                pointrank2cards[c.get_point_rank()] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(FiveCardStudPokerCard.compare_cards)

        suitrank2cards = dict()
        for c in cards:
            if c.get_suit_rank() in suitrank2cards:
                suitrank2cards[c.get_suit_rank()].append(c)
            else:
                suitrank2cards[c.get_suit_rank()] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(FiveCardStudPokerCard.compare_cards)

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in xrange(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point == suitrank2cards[s][i + 1].point - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) ==1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["4_1"]
            return pattern

        ##3_2
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_pointrank[p]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return  roomai.fivecardstud.AllCardsPattern_FiveCardStud["1_1_1_1_1"]
