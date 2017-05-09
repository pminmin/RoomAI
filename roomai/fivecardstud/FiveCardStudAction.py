#!/bin/python
import roomai.abstract

class FiveCardStudAction(roomai.abstract.AbstractAction):
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

    def __init__(self,key):
        opt_price = key.strip().split("_")
        self.option = opt_price[0]
        self.price  = int(opt_price[1])
        self.String = "%s_%d"%(self.option, self.price)

    def get_key(self):
        return self.String
