#!/bin/python
#coding:utf-8

import roomai.abstract
import copy

class StageSpace:
    firstStage  = 1
    secondStage = 2
    thirdStage  = 3
    fourthStage = 4


class TexasHoldemAction(roomai.abstract.AbstractAction):
    # 弃牌
    Fold        = "fold"
    # 过牌
    Check       = "check"
    # 更注
    Call        = "call"
    # 加注
    Raise       = "raise"
    # all in
    AllIn       = "allin"
    def __init__(self, key):
        opt_price = key.strip().split("_")
        self.option = opt_price[0]
        self.price  = int(opt_price[1])
        self.String = "%s_%d"%(self.option, self.price)
    def get_key(self):
        return self.String

    def roomai_deepcopy(self):
        return TexasHoldemAction(self.String)

class TexasHoldemPublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.num_players        = None
        self.big_blind_bet      = None

        #state of players
        self.is_quit                        = None
        self.num_quit                       = None
        self.is_allin                       = None
        self.num_allin                      = None
        self.is_needed_to_action            = None
        self.num_needed_to_action           = None

        # who is expected to take a action
        self.turn               = None

        #chips is array which contains the chips of all players
        self.chips              = None

        #bets is array which contains the bets from all players
        self.bets               = None

        #max_bet = max(self.bets)
        self.max_bet_sofar      = None
        #the raise acount
        self.raise_account      = None

        self.previous_id        = None
        self.previous_action    = None        


class TexasHoldemPrivateState(roomai.abstract.AbstractPrivateState):
    keep_cards = None
    hand_cards = None


class TexasHoldemPersonState(roomai.abstract.AbsractPersonState):
    id                =    None
    hand_cards        =    None
    available_actions =    None

    def roomai_deepcopy(self, memodict={}):
        copyinstance    = TexasHoldemPersonState()
        copyinstance.id = self.id
        if self.hand_cards is not None:
            copyinstance.hand_cards = [copy.deepcopy(self.hand_cards[i]) for i in xrange(len(self.hand_cards))]
        else:
            copyinstance.hand_cards = None

        if self.available_actions is not None:
            copyinstance.available_actions = dict()
            for key in self.available_actions:
                copyinstance.available_actions[key] = copy.deepcopy(self.available_actions[key])
        else:
            copyinstance.available_actions = None
        return copyinstance

class TexasHoldemInfo(roomai.abstract.AbstractInfo):
    public_state            = None
    person_state            = None

    def roomai_deepcopy(self, memodict={}):
        info = TexasHoldemInfo()
        info.public_state = copy.deepcopy(self.public_state)
        info.public_state = copy.deepcopy(self.person_state)
        return info


AllCardsPattern = dict()
#0     1           2       3           4                                    5     6
#name, isStraight, isPair, isSameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [],        100, []]
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1],     98,  []]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2],     97,  []]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [],        96,  []]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [],        95,  []]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1],   94,  []]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1],   93,  []]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1], 92,  []]
AllCardsPattern["1_1_1_1_1"] = \
["1_1_1_1_1",           False, True,  False, [1,1,1,1,1],91, []]




