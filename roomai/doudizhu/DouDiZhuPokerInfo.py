#!/bin/python
import os
import roomai.common
from roomai.doudizhu.DouDiZhuPokerAction import DouDiZhuActionElement
import copy


class DouDiZhuPokerHandCards:
    '''
    The hand cards in the DouDiZhuPoker game.
    
    '''
    def __init__(self, cardstr):
        self.__card_pointrank_count__ = [0 for i in range(DouDiZhuActionElement.total_normal_cards)]
        for c in cardstr:
            idx = DouDiZhuActionElement.str_to_rank[c]
            self.__card_pointrank_count__[idx] += 1
            if idx >= DouDiZhuActionElement.total_normal_cards:
                raise Exception("%s is invalid for a handcard" % (cardstr))

        self.__num_card__  = sum(self.card_pointrank_count)
        self.__count2num__ = [0 for i in range(5)]
        for count in self.__card_pointrank_count__:
            self.__count2num__[count] += 1

        strs = []
        for h in range(len(self.__card_pointrank_count__)):
            for count in range(self.__card_pointrank_count__[h]):
                strs.append(DouDiZhuActionElement.rank_to_str[h])
        strs.sort()
        self.__key__ = "".join(strs)

    def __get_card_pointrank_count__(self): return tuple(self.__card_pointrank_count__)
    card_pointrank_count = property(__get_card_pointrank_count__,
                                    doc="The card_pointrank_count is an array of counts for different card point\n" +
                                        "cardpoint_to_rank  = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, 'T':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, 'r':13, 'R':14}.\n" +
                                        "If key = \"33rR\", card_pointrank_count = [2,0,...,0,1,1], len(card_pointrank_count) = 15")

    def __get_num_card__(self): return self.__num_card__
    num_card = property(__get_num_card__, doc="The number of cards in HandCards. For example, key = \"33rR\", num_card = 4")

    def __get_key__(self): return self.__key__
    key = property(__get_key__, doc = "The key of HandCards. For example, key = \"33rR\". ")

    def __get_count2num__(self):    return tuple(self.__count2num__)
    count2num = property(__get_count2num__, doc =
    "The count2num is an array of the number of the different counts.\n"+
    "For example, key = \"333rR\", count2num = [0,2,0,1,0]. count2num[1] = 2 denotes that two cards (r and R) appear onces. count2num[3] = 1 that one card(3) appears three times ")

    def __compute_key__(self):
        strs = []
        for h in range(len(self.__card_pointrank_count__)):
            for count in range(self.__card_pointrank_count__[h]):
                strs.append(DouDiZhuActionElement.rank_to_str[h])
        strs.sort()
        return "".join(strs)

    def __add_cards__(self, cards):
        if isinstance(cards, str) == True:
            cards = DouDiZhuPokerHandCards(cards)

        for c in range(len(cards.__card_pointrank_count__)):
            count = cards.__card_pointrank_count__[c]
            self.__num_card__ += count
            self.__count2num__[self.card_pointrank_count[c]] -= 1
            self.__card_pointrank_count__[c] += count
            self.__count2num__[self.card_pointrank_count[c]] += 1

        self.__key__ = self.__compute_key__()


    def __remove_cards__(self, cards):
        if isinstance(cards, str) == True:
            cards = DouDiZhuPokerHandCards(cards)

        for c in range(len(cards.__card_pointrank_count__)):
            count = cards.__card_pointrank_count__[c]
            self.__num_card__ -= count
            self.__count2num__[self.card_pointrank_count[c]] -= 1
            self.__card_pointrank_count__[c] -= count
            self.__count2num__[self.card_pointrank_count[c]] += 1

        self.__key__ = self.__compute_key__()

    def __remove_action__(self, action):
        str = action.key
        if str == 'x' or str == 'b':
            return
        self.__remove_cards__(DouDiZhuPokerHandCards(str))

    def __deepcopy__(self, memodict={}, newinstance = None):
        return DouDiZhuPokerHandCards(self.key)

class DouDiZhuPrivateState(roomai.common.AbstractPrivateState):
    def __init__(self):
        self.__keep_cards__ = None

    def __get_keep_cards__(self):   return self.__keep_cards__
    keep_cards = property(__get_keep_cards__, doc = "A DouDiZhuPokerHandCards class about the keep cards")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPrivateState()
        newinstance.__keep_cards__ = self.keep_cards.__deepcopy__()
        return newinstance


class DouDiZhuPublicState(roomai.common.AbstractPublicState):
    '''
    The public state of DouDiZhuPoker
    '''
    def __init__(self):
        self.__landlord_candidate_id__ = -1
        self.__landlord_id__ = -1
        self.__license_playerid__ = -1
        self.__license_action__ = None
        self.__continuous_cheat_num__ = 0
        self.__is_response__ = False

        self.__keep_cards__ = None
        self.__first_player__ = -1
        self.__phase__ = -1
        self.__epoch__ = -1

    def __get_landlord_candidate_id__(self):    return self.__landlord_candidate_id__
    landlord_candidate_id = property(__get_landlord_candidate_id__, doc = "The candiate landlord player id during the betting_for_be_landlord phase")

    def __get_landlord_id__(self):  return self.__landlord_id__
    landlord_id = property(__get_landlord_id__, doc = "The landlord player id.")
    def __get_license_playerid__(self): return self.__license_playerid__
    license_playerid = property(__get_license_playerid__, doc="The license player id."+
                                                               " During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                              "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_license_action__(self):   return self.__license_action__
    license_action = property(__get_license_action__, doc="The license action.  During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_continuous_cheat_num__(self): return self.__continuous_cheat_num__
    continuous_cheat_num = property(__get_continuous_cheat_num__, doc="The number of the continuous cheat actions.During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "+
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_is_response__(self):  return  self.__is_response__
    is_response = property(__get_is_response__, doc = "is_response.  During the \"playing\" phase, if is_response is True, the current player need take an valid action with the same pattern as the license action, which was taken by the license player. "
                                                      "Unless, he takes the check action. If two continuous cheat actions are taken, is_response will be false, so that the current player needn't response the license action and can take any valid action")

    def __get_keep_cards__(self):   return self.__keep_cards__
    keep_cards = property(__get_keep_cards__, doc = "The keep cards")

    def __get_first_player__(self): return self.__first_player__
    first_player = property(__get_first_player__, doc = "The players[first_player] is first to take an action")

    def __get_phase__(self):    return self.__phase__
    phase = property(__get_phase__,
                     doc = "There are two stages in DouDiZhu, namely 0) betting for being the landlord and 1) playing the game.\n"+
                           "0 denotes the betting for being the landlord phase, 1 denotes the playing the game phase.\n")

    def __get_epoch__(self):    return self.__epoch__
    epoch = property(__get_epoch__, doc = "The epoch denotes the count about a player takes an action.")

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = DouDiZhuPublicState()
        newinstance = super(DouDiZhuPublicState, self).__deepcopy__(newinstance=newinstance)

        newinstance.__landlord_candidate_id__ = self.landlord_candidate_id
        newinstance.__landlord_id__ = self.landlord_id
        newinstance.__license_playerid__ = self.license_playerid
        if self.license_action is None:
            newinstance.__license_action__  = None
        else:
            newinstance.__license_action__ = self.license_action.__deepcopy__()
        newinstance.__continuous_cheat_num__ = self.continuous_cheat_num
        newinstance.__is_response__ = self.is_response

        if self.keep_cards == None:
            newinstance.__keep_cards__ = None
        else:
            newinstance.__keep_cards__ = self.keep_cards.__deepcopy__()

        newinstance.__first_player__ = self.first_player
        newinstance.__phase__ = self.phase
        newinstance.__epoch__ = self.epoch

        return newinstance

class DouDiZhuPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of DouDiZhu game environment
    '''
    def __init__(self):
        self.__hand_cards__        = None

    def __get_hand_cards__(self):
        return self.__hand_cards__

    hand_cards = property(__get_hand_cards__, doc="The cards in the hand of the corresponding player")

    def __deepcopy__(self, memodict={}, newinstance = None):
        newinstance = super(DouDiZhuPersonState,self).__deepcopy__(newinstance=newinstance)
        if self.hand_cards is None:
            newinstance.__hand_cards__ = None
        else:
            newinstance.__hand_cards__ = self.hand_cards.__deepcopy__()

        return newinstance

