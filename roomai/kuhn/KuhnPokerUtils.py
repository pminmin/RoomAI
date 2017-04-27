#!/bin/python
import random
import math
import roomai.abstract

class ActionSpace_Kuhn:
    bet   = 0;
    check = 1;

class Action_Kuhn(roomai.abstract.AbstractAction):
    def __init__(self, action1):
        self.action = action1
    def toString(self):
        if self.action == ActionSpace_Kuhn.bet:
            return "bet"
        else:
            return "check"

class PublicState_Kuhn(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.turn                       = 0
        self.first                      = 0
        self.epoch                      = 0
        self.action_list                = []

class PrivateState_Kuhn(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.hand_cards = []

class PersonState_Kuhn(roomai.abstract.AbsractPersonState):
    def __init__(self):
        self.available_actions  = None
        self.id                 = None
        self.card               = None

class Info_Kuhn(roomai.abstract.AbstractInfo):
    def __init__(self):
        self.public_state       = None
        self.private_state      = None
        self.person_state       = None

