#!/bin/python
#coding:utf-8
import roomai.common


class FiveCardStudAction(roomai.common.AbstractAction):
    '''
    In Five Card Stud, the action has two parts: option (action type) and price (count of chips). The option has six types: Fold, Check, Call, Raise, Bet
    and Showhand. The prices for Fold must be zero. The basic usage is as follows:
    <pre>
    >> action = roomai.fivecardstud.FiveCardStudAction.lookup("Fold_0")
    >> action.option
    "Fold"
    >> action.price
    0
    >> action.key()
    "Fold_0"
    </pre>
    '''

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
            """

            Args:
                key:
            """
            super(FiveCardStudAction,self).__init__(key)
            opt_price = key.strip().split("_")
            if  opt_price[0] != self.Fold    and opt_price[0] != self.Call  and \
                opt_price[0] != self.Check   and opt_price[0] != self.Raise and \
                opt_price[0] != self.Bet     and opt_price[0] != self.Showhand:
                raise  ValueError("%s is an invalid key. The Option must be in [Fold,Check,Call,Raise,Bet,Showhand]"%key)

            if opt_price[0] not in  [self.Fold,self.Check, self.Call] and int(opt_price[1]) <= 0:
                raise  ValueError("%s is an invalid key.]"%key)

            if opt_price[0] == self.Fold and int(opt_price[1]) > 0:
                raise  ValueError("%s is an invalid key"%(key))

            if int(opt_price[1]) < 0:
                raise  ValueError("%s is an invalid key.]"%key)

            self._roomai_option = opt_price[0]
            self._roomai_price  = int(opt_price[1])



    @property
    def option(self):
        """

        Returns:

        """
        return self._roomai_option
    @property
    def price(self):
        """

        Returns:

        """
        return self._roomai_price

    @classmethod
    def lookup(cls,key):
        """

        Args:
            key:

        Returns:

        """
        return AllFiveCardStudActions[key]

    def __deepcopy__(self, memodict={}, newinstance = None):
        """

        Args:
            memodict:
            newinstance:

        Returns:

        """
        if newinstance is None:
            newinstance        = AllFiveCardStudActions[self.key]
        return newinstance

AllFiveCardStudActions = dict()
options = ["Fold", "Check","Call","Raise","Bet","Showhand"]
for option in options:
    if option in ["Check","Call"]:
        for p in range(100000):
            AllFiveCardStudActions["%s_%d"%(option,p)] = FiveCardStudAction("%s_%d"%(option,p))
    elif option in ["Raise","Bet","Showhand"]:
        for p in range(1,100000):
            AllFiveCardStudActions["%s_%d"%(option,p)] = FiveCardStudAction("%s_%d"%(option,p))
    else:
        AllFiveCardStudActions["Fold_0"] = FiveCardStudAction("Fold_0")
is_init_action = False
