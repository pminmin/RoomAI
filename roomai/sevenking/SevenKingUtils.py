#!/bin/python
import roomai.common

AllSevenKingPatterns = dict()
###
###numCards
AllSevenKingPatterns["p_0"] = ("p_0", 0) ## check
AllSevenKingPatterns["p_1"] = ("p_1", 1)
AllSevenKingPatterns["p_2"] = ("p_2", 2)
AllSevenKingPatterns["p_3"] = ("p_3", 3)
AllSevenKingPatterns["p_4"] = ("p_4", 4)


point_str_to_rank  = {'7':14, 'R':13, 'r':12, '5':11,  '2':10,  '3':9,  'A':8,  'K':7,\
                      'Q':6,  'J':5,   'T':4,   '9':3,   '8':2,   '6':1,   '4':0}
point_rank_to_str  = {14:'7', 13:'R', 12:'r',  11:'5', 10:'2',  9:'3',  8:'A',   7:'K',\
                       6:'Q',  5:'J',   4:'T',   3:'9',   2:'8',   1:'6',  0:'4'}
suit_str_to_rank   = {'Spade':3, 'Heart':2, 'Diamond':1, 'Club':0,  'ForKing':4}
suit_rank_to_str   = {3:'Spade', 2: 'Heart', 1: 'Diamond', 0:'Club', 4:'ForKing'}

class SevenKingPokerCard(roomai.common.PokerCard):
    """
    """
    def __init__(self, point, suit = None):
        """

        Args:
            point:
            suit:
        """
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1  = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1  = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.__point_str  = point_rank_to_str[point1]
        self.__suit_str   = suit_rank_to_str[suit1]
        self.__point_rank = point1
        self.__suit_rank  = suit1
        self.__key        = "%s_%s" % (self.__point_str, self.__suit_str)

    @property
    def key(self):
        return self.__key



    @property
    def point_str(self):
        return self.__point_str

    @property
    def suit_str(self):
        return self.__suit_str

    @property
    def point_rank(self):
        """

        Returns:

        """
        return self.__point_rank
    @property
    def suit_rank(self):
        """

        Returns:

        """
        return self.__suit_rank
    def lookup(cls, key):
        """

        Args:
            key:

        Returns:

        """
        return AllSevenKingPokerCards[key]
    def __deepcopy__(self,  memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """

        if self.key in AllSevenKingPokerCards:
            return AllSevenKingPokerCards[self.key]

        if newinstance is None:
            newinstance = AllSevenKingPokerCards[self.__key]
        else:
            newinstance = super(SevenKingPokerCard, self).__deepcopy__(newinstance = newinstance)

        return newinstance

AllSevenKingPokerCards = dict()
for point in point_str_to_rank:
    if point != "r" and point != "R":
        for suit in suit_str_to_rank:
            if suit != "ForKing":
                AllSevenKingPokerCards["%s_%s" % (point, suit)] = SevenKingPokerCard("%s_%s" % (point, suit))
AllSevenKingPokerCards["R_ForKing"] = SevenKingPokerCard("R_ForKing")
AllSevenKingPokerCards["r_ForKing"] = SevenKingPokerCard("r_ForKing")
