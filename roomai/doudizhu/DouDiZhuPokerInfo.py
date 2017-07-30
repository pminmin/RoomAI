#!/bin/python
import os
import roomai.common
from roomai.doudizhu.DouDiZhuPokerAction import DouDiZhuActionElement
import copy


class DouDiZhuHandCards:
    def __init__(self, cardstr):
        self.cards = [0 for i in range(DouDiZhuActionElement.total_normal_cards)]
        for c in cardstr:
            idx = DouDiZhuActionElement.str_to_rank[c]
            self.cards[idx] += 1
            if idx >= DouDiZhuActionElement.total_normal_cards:
                raise Exception("%s is invalid for a handcard" % (cardstr))

        self.num_cards = sum(self.cards)
        self.count2num = [0 for i in range(DouDiZhuActionElement.total_normal_cards)]
        for count in self.cards:
            self.count2num[count] += 1

        strs = []
        for h in range(len(self.cards)):
            for count in range(self.cards[h]):
                strs.append(DouDiZhuActionElement.rank_to_str[h])
        strs.sort()
        self.__key = "".join(strs)

    def compute_key(self):
        strs = []
        for h in range(len(self.cards)):
            for count in range(self.cards[h]):
                strs.append(DouDiZhuActionElement.rank_to_str[h])
        strs.sort()
        return "".join(strs)

    @property
    def key(self):
        return self.__key


    def add_cards_str(self, str):
        self.add_cards(DouDiZhuHandCards(str))
        self.__key = self.compute_key()

    def add_cards(self, cards):
        for c in range(len(cards.cards)):
            count = cards.cards[c]
            self.num_cards += count
            self.count2num[self.cards[c]] -= 1
            self.cards[c] += count
            self.count2num[self.cards[c]] += 1

        self.__key = self.compute_key()

    def remove_cards_str(self, str):
        self.remove_cards(DouDiZhuHandCards(str))
        self.__key = self.compute_key()

    def remove_cards(self, cards):
        for c in range(len(cards.cards)):
            count = cards.cards[c]
            self.num_cards -= count
            self.count2num[self.cards[c]] -= 1
            self.cards[c] -= count
            self.count2num[self.cards[c]] += 1

        self.__key = self.key(is_recomputing=True)

    def remove_action_cards(self, action):
        str = action.key()
        if str == 'x' or str == 'b':
            str = ''
        self.remove_cards(DouDiZhuHandCards(str))
        self.__key = self.compute_key()


class DouDiZhuPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        self.keep_cards = []


class DouDiZhuPublicState(roomai.common.AbstractPublicState):
    def __init__(self):
        self.landlord_candidate_id = -1
        self.landlord_id = -1
        self.license_playerid = -1
        self.license_action = None
        self.continous_cheat_num = 0
        self.is_response = False

        self.first_player = -1
        self.turn = -1
        self.phase = -1
        self.epoch = -1

        self.previous_id = -1
        self.previous_action = None


class DouDiZhuPersonState(roomai.common.AbstractPersonState):
    def __init__(self):
        self.id                = None
        self.hand_cards        = None
        self.available_actions = dict()


