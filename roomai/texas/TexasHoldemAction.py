#!/bin/python
#coding:utf-8
import roomai.common

class TexasHoldemAction(roomai.common.AbstractAction):
    """
    """
    # 弃牌
    Fold        = "Fold"
    # 过牌
    Check       = "Check"
    # 更注
    Call        = "Call"
    # 加注
    Raise       = "Raise"
    # all in
    AllIn       = "Allin"
    def __init__(self, key):
        """

        Args:
            key:
        """
        opt_price = key.strip().split("_")
        self.__option = opt_price[0]
        self.__price  = int(opt_price[1])
        self.__key    = "%s_%d"%(self.option, self.price)

    @property
    def key(self):
        """

        Returns:

        """
        return self.__key
    @property
    def option(self):
        """

        Returns:

        """
        return self.__option
    @property
    def price(self):
        """

        Returns:

        """
        return self.__price

    @classmethod
    def lookup(cls, key):
        """

        Args:
            key:

        Returns:

        """
        if key not in AllTexasActions:
            AllTexasActions[key] = TexasHoldemAction(key)
        return AllTexasActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """
        if self.key not in AllTexasActions:
            AllTexasActions[self.key] = TexasHoldemAction(self.key)
        return AllTexasActions[self.key]

AllTexasActions = dict()
