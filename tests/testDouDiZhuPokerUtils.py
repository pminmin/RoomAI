#!/bin/python

import sys
import unittest
from roomai.doudizhu import *

class DouDiZhuPokerUtilTester(unittest.TestCase):
    def testAction2Patterns(self):
        
        a = DouDiZhuAction([1, 1, 1], [2]).complement()
        self.assertEqual(a.pattern[0], "p_3_1_0_1_1")

        a = DouDiZhuAction([1, 1, 1, 2, 3, 3], []).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuAction([1, 1, 1, 1, 1], [2]).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuAction([DouDiZhuActionElement.cheat], [2]).complement()
        self.assertEqual(a.pattern[0], "i_invalid")

        a = DouDiZhuAction([DouDiZhuActionElement.cheat], []).complement()
        self.assertEqual(a.pattern[0], "i_cheat")
        
        a = DouDiZhuAction([DouDiZhuActionElement.R, DouDiZhuActionElement.r], []).complement()
        self.assertEqual(a.pattern[0], "x_rocket")
        

    def testAllPatterns(self):
        for k in AllPatterns:
            p = AllPatterns[k]
            self.assertEqual(k,p[0])
            self.assertEqual(len(p),7)
            if "p" in p[0]:
                self.assertEqual("p_%d_%d_%d_%d_%d"%(p[1],p[2],p[3],p[4],p[5]), p[0])

         
