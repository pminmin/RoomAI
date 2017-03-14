#!/bin/python
import unittest
from roomai.abstract import *

class AbstractEnvTester(unittest.TestCase):
    def test_functions(self):
        aEnv = AbstractEnv();

class AbstractPlayerTester(unittest.TestCase):
    def test_functions(self):
        aPlayer = AbstractPlayer();
        with self.assertRaises(NotImplementedError):
            aPlayer.receiveInfo([]);
        with self.assertRaises(NotImplementedError):
            aPlayer.takeAction();

