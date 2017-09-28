#!/bin/python
#coding:utf-8
import roomai.common
import copy

class TexasHoldemPublicState(roomai.common.AbstractPublicState):
    '''
    The public state of the TexasHoldem Poker game
    '''
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.num_players        = None
        self.big_blind_bet      = None

        #state of players
        self.is_fold                        = None
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

    def __deepcopy__(self, memodict={}, newinstance=None):
            copyinstance = TexasHoldemPublicState()

            copyinstance.stage         = self.stage
            copyinstance.num_players   = self.num_players
            copyinstance.dealer_id     = self.dealer_id
            copyinstance.big_blind_bet = self.big_blind_bet

            if self.public_cards is None:
                copyinstance.public_cards = None
            else:
                copyinstance.public_cards = [self.public_cards[i].__deepcopy__() for i in range(len(self.public_cards))]


            ######## quit, allin , needed_to_action
            copy.num_quit = self.num_quit
            if self.is_fold is None:
                copyinstance.is_fold = None
            else:
                copyinstance.is_fold = [self.is_fold[i] for i in range(len(self.is_fold))]

            copyinstance.num_allin = self.num_allin
            if self.is_allin is None:
                copyinstance.is_allin = None
            else:
                copyinstance.is_allin = [self.is_allin[i] for i in range(len(self.is_allin))]

            copyinstance.num_needed_to_action = self.num_needed_to_action
            if self.is_needed_to_action is None:
                copyinstance.is_needed_to_action = None
            else:
                copyinstance.is_needed_to_action = [self.is_needed_to_action[i] for i in
                                                    range(len(self.is_needed_to_action))]

            # chips is array which contains the chips of all players
            if self.chips is None:
                copyinstance.chips = None
            else:
                copyinstance.chips = [self.chips[i] for i in range(len(self.chips))]

            # bets is array which contains the bets from all players
            if self.bets is None:
                copyinstance.bets = None
            else:
                copyinstance.bets = [self.bets[i] for i in range(len(self.bets))]

            copyinstance.max_bet_sofar = self.max_bet_sofar
            copyinstance.raise_account = self.raise_account
            copyinstance.turn = self.turn

            copyinstance.previous_id = self.previous_id
            if self.previous_action is None:
                copyinstance.previous_action = None
            else:
                copyinstance.previous_action = self.previous_action.__deepcopy__()

            ### isterminal, scores
            copyinstance.is_terminal = self.is_terminal
            if self.scores is None:
                copyinstance.scores = None
            else:
                copyinstance.scores = [self.scores[i] for i in range(len(self.scores))]

            return copyinstance


class TexasHoldemPrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of the TexasHoldem Poker game
    '''
    def __init__(self):
        self.keep_cards = []

    def __deepcopy__(self, memodict={}):
        copy = TexasHoldemPrivateState()
        if self.keep_cards is None:
            copy.keep_cards = None
        else:
            copy.keep_cards = [self.keep_cards[i].__deepcopy__() for i in range(len(self.keep_cards))]



class TexasHoldemPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of the TexasHoldem Poker game    
    '''

    def __init__(self):
        self.id = 0
        self.hand_cards = []
        self.available_actions = dict()


    def __deepcopy__(self, memodict={}):
        copyinstance    = TexasHoldemPersonState()
        copyinstance.id = self.id
        if self.hand_cards is not None:
            copyinstance.hand_cards = [self.hand_cards[i].__deepcopy__() for i in range(len(self.hand_cards))]
        else:
            copyinstance.hand_cards = None

        if self.available_actions is not None:
            copyinstance.available_actions = dict()
            for key in self.available_actions:
                copyinstance.available_actions[key] = self.available_actions[key].__deepcopy__()
        else:
            copyinstance.available_actions = None
        return copyinstance


AllCardsPattern = dict()
#0     1           2       3           4                                    5     6
#name, isStraight, isPair, isSameSuit, [SizeOfPair1, SizeOfPair2,..](desc), rank, cards
AllCardsPattern["Straight_SameSuit"] = \
["Straight_SameSuit",   True,  False, True,  [],         100]
AllCardsPattern["4_1"] = \
["4_1",                 False, True,  False, [4,1],      98]
AllCardsPattern["3_2"] = \
["3_2",                 False, True,  False, [3,2],      97]
AllCardsPattern["SameSuit"] = \
["SameSuit",            False, False, True,  [],         96]
AllCardsPattern["Straight_DiffSuit"] = \
["Straight_DiffSuit",   True,  False, False, [],         95]
AllCardsPattern["3_1_1"] = \
["3_1_1",               False, True,  False, [3,1,1],    94]
AllCardsPattern["2_2_1"] = \
["2_2_1",               False, True,  False, [2,2,1],    93]
AllCardsPattern["2_1_1_1"] = \
["2_1_1_1",             False, True,  False, [2,1,1,1],  92]
AllCardsPattern["1_1_1_1_1"] = \
["1_1_1_1_1",           False, True,  False, [1,1,1,1,1],91]