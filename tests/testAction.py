#!/bin/python
from roomai.doudizhu import *
import unittest

class testAllActions(unittest.TestCase):
    def test(self):
        idx = [ 0 for i in xrange(len(AllActions))];
        for a in AllActions:
            act = AllActions[a]
            self.assertTrue(act.pattern[0] != "i_invalid")
