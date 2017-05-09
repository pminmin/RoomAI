#!/bin/python
import roomai.abstract
<<<<<<< HEAD
class OptionSpace:
=======

class FiveCardStudAction(roomai.abstract.AbstractAction):
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
    # 弃牌
    Fold        = "fold"
    # 过牌
    Check       = "check"
    # 更注
    Call        = "call"
    # 加注
    Raise       = "raise"
    # all in
    AllIn       = "allin"

<<<<<<< HEAD

class Action_FiveCardStud(roomai.abstract.AbstractAction):
    def __init__(self, option, price):
        self.option = option
        self.price  = price
        self.string = "%s_%d"%(self.option, self.price)

    def toString(self):
        return self.string
=======
    def __init__(self,key):
        opt_price = key.strip().split("_")
        self.option = opt_price[0]
        self.price  = int(opt_price[1])
        self.String = "%s_%d"%(self.option, self.price)

    def get_key(self):
        return self.String
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
