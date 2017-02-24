#!/bin/python

import sys
import unittest
sys.path.append("DouDiZhuPoker")

from DouDiZhuPokerUtil import *


class DouDiZhuPokerUtilTester(unittest.TestCase):
    '''
    def testAction2Patterns(self):
        
        a = Action([1,1,1],[2]).complement()
        self.assertEqual(a.pattern[0], "p_3_1_0_1_1")

        a = Action([1,1,1,2,3,3],[]).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([1,1,1,1,1],[2]).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([ActionSpace.cheat],[2]).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = Action([ActionSpace.cheat],[]).complement()
        self.assertEqual(a.pattern[0], "i_cheat")
        
        a = Action([ActionSpace.R, ActionSpace.r],[]).complement()
        self.assertEqual(a.pattern[0], "x_twoKings")
        

    def testAllPatterns(self):
        for k in AllPatterns:
            p = AllPatterns[k]
            self.assertEqual(k,p[0])
            self.assertEqual(len(p),8)
            if "p" in p[0]:
                self.assertEqual("p_%d_%d_%d_%d_%d"%(p[2],p[3],p[4],p[5],p[6]), p[0])

    '''

    def testCompare(self):
        
        a  = Action([1,1,1],[2])
        b  = Action([1,1,1,1],[])

        #with self.assertRaises(Exception):
        #    x = compareActions(a,b)

        c = Action([2,2,2],[1])
        rankdiff = compareActions(a,c)
        self.assertTrue(rankdiff < 0)
