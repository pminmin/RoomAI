#!/bin/python
from roomai.doudizhu import *
import unittest

class testAllActions(unittest.TestCase):
    def test(self):
        idx = [ 0 for i in xrange(len(ActionSpace.AllActions))];
        for a in ActionSpace.AllActions:
            act = ActionSpace.AllActions[a]
            self.assertTrue(act.pattern[0] != "i_invalid")
