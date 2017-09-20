#!/bin/python
import roomai.common
import roomai.sevenking
from roomai.sevenking import AllSevenKingPatterns

from functools import cmp_to_key

class SevenKingAction(roomai.common.AbstractAction):
    """
    """

    def __init__(self, key):
        """

        Args:
            key:
        """
        if not isinstance(key,str):
            raise TypeError("The key for SevenKingAction is an str, not %s"%(type(str)))

        super(SevenKingAction,self).__init__(key)
        self.__key         = key.strip()
        self.__cards       = []
        if len(key) > 0:
            for c in self.key.split(","):
                self.__cards.append(roomai.sevenking.SevenKingPokerCard(c))
            self.__cards.sort(key = cmp_to_key(roomai.sevenking.SevenKingPokerCard.compare))
        self.__pattern = self.action2pattern(self)

    @classmethod
    def action2pattern(cls, action):
        """

        Args:
            action:

        Returns:

        """
        ###numCards
        num_cards  = len(action.cards)
        return AllSevenKingPatterns["p_%d"%(num_cards)]

    @property
    def key(self):
        """

        Returns:

        """
        return self.__key

    @property
    def cards(self):
        """

        Returns:

        """
        return tuple(self.__cards)

    @property
    def pattern(self):
        """

        Returns:

        """
        return self.__pattern

    @classmethod
    def lookup(cls, key):
        """

        Args:
            key:

        Returns:

        """
        if key in AllSevenKingActions:
            return AllSevenKingActions[key]
        else:
            AllSevenKingActions[key] = SevenKingAction(key)
            return AllSevenKingActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        '''

        Args:
            memodict:
            newinstance:

        Returns:

        '''

        if self.__key in AllSevenKingActions:
            return AllSevenKingActions[self.__key]

        else:
            if newinstance is None:
                newinstance = SevenKingAction(self.key)
            else:
                newinstance           = super(SevenKingAction,self).__deepcopy__(newinstance = newinstance)
                newinstance.__key     = self.__key
                newinstance.__cards   = [card.__deepcopy__() for card in self.__cards]
                newinstance.__pattern = self.__pattern
            AllSevenKingActions[self.__key] = newinstance

            return newinstance

AllSevenKingActions = dict()

