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

        if opt_price[0] not in  [self.Fold,self.Check, self.Call] and int(opt_price[1]) <= 0:
            raise  ValueError("%s is an invalid key.]"%key)

        if int(opt_price[1]) < 0:
            raise  ValueError("%s is an invalid key.]"%key)

        self.__option = opt_price[0]
        self.__price  = int(opt_price[1])


    @property
    def option(self):
        return self.__option
    @property
    def price(self):
        return self.__price

    def get_key(self):
        return super(FiveCardStudAction,self).get_key()


    def __deepcopy__(self, memodict={}, newinstance = None,):
        if newinstance is None:
            newinstance        = AllFiveCardStudActions[self.get_key()]
        return newinstance


AllFiveCardStudActions = dict()
options = ["Fold", "Check","Call","Raise","Bet","Showhand"]
for option in options:
    if option != "Fold":
        for p in range(100000):
            AllFiveCardStudActions["%s_%d"%(option,p)] = FiveCardStudAction("%s_%d"%(option,p))
    else:
        AllFiveCardStudActions["Fold_0"] = FiveCardStudAction("Fold_0")