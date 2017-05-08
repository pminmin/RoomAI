#!/bin/python
import roomai.abstract
class OptionSpace:
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


class Action_FiveCardStud(roomai.abstract.AbstractAction):
    def __init__(self, option, price):
        self.option = option
        self.price  = price
        self.string = "%s_%d"%(self.option, self.price)

    def toString(self):
        return self.string
