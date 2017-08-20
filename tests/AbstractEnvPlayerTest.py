#!/bin/python
import unittest
from roomai.common import *

class AbstractEnvTester(unittest.TestCase):
    """
    """
    def test_functions(self):
        """

        """
        aEnv = AbstractEnv();

class AbstractPlayerTester(unittest.TestCase):
    """
    """
    def test_functions(self):
        """

        """
        aPlayer = AbstractPlayer();
        with self.assertRaises(NotImplementedError):
            aPlayer.receive_info([]);
        with self.assertRaises(NotImplementedError):
            aPlayer.take_action();

