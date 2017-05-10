#!/bin/python
from roomai.fivecardstud import FiveCardStudEnv
import unittest

class FiveCardStudTester(unittest.TestCase):
    def test(self):
        env = FiveCardStudEnv();
        env.init()
