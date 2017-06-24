#!/bin/python
import roomai.common
import copy


class KuhnPokerAction(roomai.common.AbstractAction):
    bet   = 0;
    check = 1;
    def __init__(self, key):
        self.action = ""
        if key == "bet": self.action = KuhnPokerAction.bet
        elif key == "check":self.action = KuhnPokerAction.check
        else:
            raise KeyError("%s is invalid key for Kuhn Action"%(key))

    def get_key(self):
        if self.action == KuhnPokerAction.bet:
            return "bet"
        else:
            return "check"

    def __deepcopy__(self, memodict={}):
        copy = KuhnPokerAction()
        copy.action = self.action
        return copy


class KuhnPokerPublicState(roomai.common.AbstractPublicState):
    def __init__(self):
        self.turn                       = 0
        self.first                      = 0
        self.epoch                      = 0
        self.action_list                = []


    def __deepcopy__(self, memodict={}):
        copy = KuhnPokerPublicState()
        copy.turn  = self.turn
        copy.first = self.first
        copy.epoch = self.epoch
        for a in self.action_list:
            copy.action_list.append(a)
        return copy

class KuhnPokerPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        self.hand_cards = []

    def __deepcopy__(self, memodict={}):
        copy            = KuhnPokerPrivateState()
        copy.hand_cards = [card for card in self.hand_cards]
        return copy

class KuhnPokerPersonState(roomai.common.AbsractPersonState):
    def __init__(self):
        self.available_actions  = dict()
        self.id                 = 1
        self.card               = 0

    def __deepcopy__(self, memodict={}):
        copy                   = KuhnPokerPersonState()
        copy.id                = self.id
        copy.card              = self.card
        copy.available_actions = dict()

        if self.available_actions is None:
            self.available_actions = None
        else:
            for action_key in self.available_actions:
                copy.available_actions[action_key] = self.available_actions[action_key].__deepcopy__()
            return copy