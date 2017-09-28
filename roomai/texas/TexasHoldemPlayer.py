#!/bin/python
#coding:utf-8
import random
import roomai.common
import sys

class TexasHoldemRandomPlayer(roomai.common.AbstractPlayer):
    '''
    A TexasHoldem AI, who chooses an action from all available actions randomly
    '''
    def __init__(self):
        self.available_actions = None
        self.info              = None
           
    def receive_info(self, info):
        '''
        :param info: The information given by the TexasHoldem environment
        '''
        self.info              = info
        self.available_actions = info.person_state.available_actions

    def take_action(self):
        '''
        :return: A random valid action
        '''


        idx  = int(random.random() * len(self.available_actions))
        keys = list(self.available_actions.keys())

        return self.available_actions[keys[idx]]

    def reset(self):
        '''
        reset for a new game
        
        '''
        pass