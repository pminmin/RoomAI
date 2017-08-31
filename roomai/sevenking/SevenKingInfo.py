#!/bin/python
import roomai.common

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
        self.__hand_cards   = []

    @property
    def hand_cards(self):
        return tuple(self.__hand_cards)

    def __deepcopy__(self, memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """
        if newinstance is None:
            newinstance          = SevenKingPersonState()
        newinstance              = super(SevenKingPersonState, self).__deepcopy__(newinstance= newinstance)
        newinstance.__hand_cards = [card.__deepcopy__() for card in self.hand_cards]
        return newinstance



