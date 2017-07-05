#!/bin/python
#coding:utf-8
import roomai.common


class FiveCardStudAction(roomai.common.AbstractAction):

    # 弃牌
    Fold        = "Fold"
    # 过牌
    Check       = "Check"
    # 更注
    Call        = "Call"
    # 加注
    Raise       = "Raise"
    # 下注
    Bet         = "Bet"
    # all in
    Showhand    = "Showhand"

    def __init__(self,key):
        super(FiveCardStudAction,self).__init__(key)

        opt_price = key.strip().split("_")
        if  opt_price[0] != self.Fold    and opt_price[0] != self.Call  and \
            opt_price[0] != self.Check   and opt_price[0] != self.Raise and \
            opt_price[0] != self.Bet     and opt_price[0] != self.Showhand:
            raise  ValueError("%s is an invalid key. The Option must be in [Fold,Check,Call,Raise,Bet,Showhand]"%key)
        self.option = opt_price[0]
        self.price  = int(opt_price[1])


    def get_key(self):
        return self.key


    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = FiveCardStudAction(self.key)

        newinstance        = super(FiveCardStudAction,self).__deepcopy__(newinstance = newinstance)
        newinstance.price  = self.price
        newinstance.option = self.option
        return newinstance
