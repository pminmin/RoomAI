#!/bin/python
import roomai.common
import roomai.sevenking.SevenKingFiveTwoThreePokerCard

class SevenKingFiveTwoThreeAction(roomai.common.AbstractAction):
    check = 'x'
    def __init__(self, key):
        if not isinstance(key,str):
            raise TypeError("The key for SevenKingFiveTwoThreeAction is an str, not %s"%(type(str)))
        if self.check not in key and len(self.key) != 1:
            raise ValueError("The %s is an invalid key for SevenKingFiveTwoThreeAction" % (self.key))

        self.key   = key
        self.cards = []
        for c in self.key:
            if c != self.check:
                self.cards.append(roomai.sevenking.SevenKingFiveTwoThreePokerCard(c))


    def get_key(self):
        return self.key

    def __deepcopy__(self, memodict={}):
        copy = SevenKingFiveTwoThreeAction(self.key)
        return copy
