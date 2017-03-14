#!/bin/python
from roomai.doudizhu import *
import unittest

class testAllActions(unittest.TestCase):
    def test(self):
        idx = [ 0 for i in xrange(len(AllActions))];
        for a in AllActions:
            act = AllActions[a]
            idx[act.idx] = 1

        for i in xrange(len(AllActions)):
            self.assertEqual(idx[i],1) 
