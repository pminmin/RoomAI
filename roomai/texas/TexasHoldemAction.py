#!/bin/python
#coding:utf-8
import roomai.common



class TexasHoldemAction(roomai.common.AbstractAction):
    '''
    The action class of the TexasHoldem game
    '''

    # 弃牌
    Fold = "Fold"
    # 过牌
    Check = "Check"
    # 更注
    Call = "Call"
    # 加注
    Raise = "Raise"
    # all in
    AllIn = "Allin"

    def __init__(self, key):
        opt_price = key.strip().split("_")
        self.__option = opt_price[0]
        self.__price  = int(opt_price[1])
        self.__key    = "%s_%d"%(self.__option, self.__price)

    def key(self):
        '''
        
        :return: the key of the TexasHoldem game action 
        '''
        return self.__key

    def option(self):
        '''
        The option of the TexasHoldem game action. all options: "Fold", "Check", "Call", "Raise" and "Allin"
        
        :return: the option of the TexasHoldem game action 
        '''
        return self.__option

    def price(self):
        '''
        The price of the TexasHoldem game action is the chips used by this action.
        
        :return: the price of the TexasHoldem game action. 
        '''
        return self.__price

    @classmethod
    def lookup(cls, key):
        '''
        Lookup a action with this key. 
        We strongly recommend you to use the lookup function to get the action with this key.
        
        :param key: the key
        :return: The action with this key 
        '''
        if key not in AllTexasActions:
            AllTexasActions[key] = TexasHoldemAction(key)
        return AllTexasActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        if self.key not in AllTexasActions:
            AllTexasActions[self.key()] = TexasHoldemAction(self.key())
        return AllTexasActions[self.key()]

AllTexasActions = dict()
