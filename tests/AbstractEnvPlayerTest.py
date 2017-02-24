#!/bin/python
import unittest
from AbstractEnvPlayer import *

class AbstractEnvTester(unittest.TestCase):
    def test_functions(self):
        aEnv = AbstractEnv();
        with self.assertRaises(NotImplementedError):
            aEnv.setPlayers([]);
        with self.assertRaises(NotImplementedError):
            aEnv.round()

class AbstractPlayerTester(unittest.TestCase):
    def test_functions(self):
        aPlayer = AbstractPlayer();
        with self.assertRaises(NotImplementedError):
            aPlayer.receiveActions([]);
        with self.assertRaises(NotImplementedError):
            aPlayer.receiveInformation([]);
        with self.assertRaises(NotImplementedError):
            aPlayer.takeAction([]);

