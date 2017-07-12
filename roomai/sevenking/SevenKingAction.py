#!/bin/python
import roomai.common
import roomai.sevenking


class SevenKingAction(roomai.common.AbstractAction):

    def __init__(self, key):
        if not isinstance(key,str):
            raise TypeError("The key for SevenKingAction is an str, not %s"%(type(str)))

        super(SevenKingAction,self).__init__(key)
        self.key         = key.strip()
        self.cards       = []
        print ("SevenKingAction:key=%s"%(key))
        if len(key) > 0:
            for c in self.key.split(","):
                self.cards.append(roomai.sevenking.SevenKingPokerCard(c))
            self.cards.sort(cmp = roomai.sevenking.SevenKingPokerCard.compare)
        self.pattern = roomai.sevenking.SevenKingEnv.action2pattern(self)

    def key(self):
        return self.key

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = SevenKingAction(self.key)
        newinstance         = super(self).__deepcopy__(newinstance = newinstance)
        newinstance.key     = self.key
        newinstance.cards   = [card.__deepcopy__() for card in self.cards]
        newinstance.pattern = self.pattern
        return newinstance
