#!/bin/python
#coding:utf-8
import random
import roomai.abstract
from roomai.kuhn import *

class KuhnPokerAlwaysBetPlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        pass
           
    def receiveInfo(self,info):
        pass     

    def takeAction(self):
        return ActionSpace.bet

    def reset(self):
        pass
