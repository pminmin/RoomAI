#!/bin/python
#coding:utf-8

import random
import copy
import roomai


class NoLimitTexasHoldemPokerEnv(roomai.AbstractEnv):

    def __init__(self):
        self.public_state  = PublicState()
        self.private_state = PrivateState() 

    #@Override
    def isActionValid(self, action):
        pass

    #@Overide
    def init(self, players):
        pass

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        pass

        

