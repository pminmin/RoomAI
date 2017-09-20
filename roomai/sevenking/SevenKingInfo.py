#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPokerCard

class SevenKingPublicState(roomai.common.AbstractPublicState):
    """
    """
    def __init__(self):
        """

        """
        super(SevenKingPublicState,self).__init__()
        self.__stage            = None
        self.__num_players      = None
        self.__showed_cards     = None
        self.__num_showed_cards = None
        self.__num_keep_cards   = None
        self.__num_hand_cards   = None
        self.__is_fold          = None
        self.__num_fold         = None
        self.__license_action   = None

    @property
    def stage(self):
        return self.__stage

    @property
    def num_players(self):
        return self.__num_players

    @property
    def showed_cards(self):
        if self.__showed_cards is None:
            return None
        return tuple(self.__showed_cards)

    @property
    def num_showed_cards(self):
        return self.__num_showed_cards

    @property
    def is_fold(self):
        if self.__is_fold is None:
            return None
        return tuple(self.__is_fold)

    @property
    def num_fold(self):
        return self.__num_fold

    @property
    def license_action(self):
        return self.__license_action

    def __deepcopy__(self, newinstance = None, memodict={}):
        """

        Args:
            newinstance:
            memodict:

        Returns:

        """
        if  newinstance is None:
            newinstance = SevenKingPublicState()
        newinstance   = super(SevenKingPublicState,self).__deepcopy__(newinstance = newinstance)

        if self.showed_cards is None:
            newinstance.__showed_cards = None
        else:
            newinstance.__showed_cards = [card.__deepcopy__() for card in self.showed_cards]
        return newinstance

class SevenKingPrivateState(roomai.common.AbstractPrivateState):
    """
    """
    def __init__(self):
        """

        """
        super(SevenKingPrivateState,self).__init__()
        self.__keep_cards   = []

    @property
    def keep_cards(self):
        return tuple(self.__keep_cards)

    def __deepcopy__(self, newinstance = None, memodict={}):
        """

        Args:
            newinstance:
            memodict:

        Returns:

        """
        if newinstance is None:
            newinstance = SevenKingPrivateState()
        newinstance              = super(SevenKingPrivateState,self).__deepcopy__(newinstance = newinstance)
        newinstance.__keep_cards =  [card.__deepcopy__() for card in self.keep_cards   ]
        return newinstance


class SevenKingPersonState(roomai.common.AbstractPersonState):
    """
    """
    def __init__(self):
        """

        """
        super(SevenKingPersonState,self).__init__()
        self.__hand_cards         = []
        self.__hand_cards_set     = set()
        self.__hand_cards_key     = ""


    @property
    def hand_cards(self):
        return tuple(self.__hand_cards)

    @property
    def hand_cards_key(self):
        return self.__hand_cards_key

    @property
    def hand_cards_set(self):
        return frozenset(self.__hand_cards_set)


    def __add_card(self, c):
        self.__hand_cards.append(c)
        self.__hand_cards_set.add(c.key)

        for j in range(len(self.__hand_cards)-1,0,-1):
            if SevenKingPokerCard.compare(self.__hand_cards[j - 1], self.__hand_cards[j]) > 0:
                tmp = self.__hand_cards[j]
                self.__hand_cards[j] = self.__hand_cards[j-1]
                self.__hand_cards[j-1] = tmp
            else:
                break

        self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards])

    def __add_cards(self, cards):
        len1 = len(self.__hand_cards)
        for c in cards:
            self.__hand_cards.append(c)
            self.__hand_cards_set.add(c.key)
        len2 = len(self.__hand_cards)


        for i in range(len1,len2-1):
            for j in range(i,0,-1):
                if SevenKingPokerCard.compare(self.__hand_cards[j-1], self.__hand_cards[j]) > 0:
                    tmp      = self.__hand_cards[j]
                    self.__hand_cards[j] = self.__hand_cards[j-1]
                    self.__hand_cards[j-1] = tmp
                else:
                    break


        #self.__hand_cards.sort(cmp=SevenKingPokerCard.compare)
        self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards])



    def __del_card(self, c):
        self.__hand_cards_set.remove(c.key)

        tmp = self.__hand_cards
        self.__hand_cards = []
        for i in range(len(tmp)):
            if c.key == tmp[i].key:
                continue
            self.__hand_cards.append(tmp[i])
        self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards])


    def __del_cards(self, cards):
        for c in cards:
            self.__hand_cards_set.remove(c.key)

        tmp = self.__hand_cards
        self.__hand_cards = []
        for i in range(len(tmp)):
            if tmp[i].key not in self.__hand_cards_set:
                continue
            self.__hand_cards.append(tmp[i])
        self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards])

    def __gen_pointrank2cards(self):
        if self.__hand_cards_key in AllPointRank2Cards:
            return AllPointRank2Cards[self.__hand_cards_key]
        else:
            point2cards = dict()
            for c in self.hand_cards:
                point = c.point_rank
                if point not in point2cards:
                    point2cards[point] = []
                point2cards[point].append(c)
            #for p in point2cards:
            #    point2cards[p].sort(cmp=SevenKingPokerCard.compare)

            AllPointRank2Cards[self.__hand_cards_key] = point2cards
            return point2cards

    def __deepcopy__(self, memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """
        if newinstance is None:
            newinstance          = SevenKingPersonState()
        newinstance                     = super(SevenKingPersonState, self).__deepcopy__(newinstance= newinstance)
        newinstance.__hand_cards        = list(tuple(self.__hand_cards))
        newinstance.__hand_cards        = set(self.__hand_cards_set)
        newinstance.__hand_cards_key    = self.__hand_cards_key
        return newinstance



AllPointRank2Cards = dict()