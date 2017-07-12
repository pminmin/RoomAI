#!/bin/python
import roomai.common

class SevenKingPublicState(roomai.common.AbstractPublicState):
    def __init__(self):
        super(SevenKingPublicState,self).__init__()
        self.stage            = 0
        self.num_players      = 0
        self.showed_cards     = []
        self.num_showed_cards = 0
        self.num_keep_cards   = 0
        self.num_hand_cards   = []
        self.is_check         = []
        self.num_check        = 0


    def __deepcopy__(self, newinstance = None, memodict={}):
        if  newinstance is None:
            newinstance = SevenKingPublicState()
        newinstance            = super(SevenKingPublicState,self).__deepcopy__(newinstance = newinstance)
        newinstance.used_cards = [card.__deepcopy__() for card in self.showed_cards]
        return newinstance

class SevenKingPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        super(SevenKingPrivateState,self).__init__()
        self.keep_cards   = []
        self.hand_cards   = [[] for i in range(2)] ##

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = SevenKingPrivateState()
        newinstance            = super(SevenKingPrivateState,self).__deepcopy__(newinstance = newinstance)
        newinstance.keep_cards =  [card.__deepcopy__() for card in self.keep_cards   ]
        newinstance.hand_cards = [[card.__deepcopy__() for card in self.hand_cards[i]] for i in range(len(self.hand_cards))]
        return newinstance


class SevenKingPersonState(roomai.common.AbsractPersonState):
    def __init__(self):
        super(SevenKingPersonState,self).__init__()
        self.hand_card   = []

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = SevenKingPersonState()
        newinstance.hand_card = [card.__deepcopy__() for card in self.hand_card]
        return newinstance

