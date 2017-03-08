#!/bin/python
import random
import math
import roomai

class Action:
    bet   = 0;
    cheat = 1;

class PublicState(roomai.AbstractPublicState):
    def __init__(self):
        self.turn                       = 0
        self.first                      = 0
        self.epoch                      = 0
        self.action_list                = 0

class PrivateState(roomai.AbstractPrivateState):
    def __init__(self):
        self.hand_cards = []

class Info(roomai.AbstractInfo):
    def __init__(self):
        self.public_state  = None
        self.private_state = None
        self.id            = -1
        self.card          = -1

class Utils(roomai.AbstractUtils):
    #@overide
    def is_action_valid(public_state, action):
        if  isinstance(public_state, PublicState) and \
            isinstance(action,Action):
            return True       
