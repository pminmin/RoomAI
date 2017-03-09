#!/bin/python
#coding:utf-8

import random
import copy
import roomai.utils

from NoLimitTexasHoldemPokerUtil import *

class NoLimitTexasHoldemPokerEnv(roomai.utils.AbstractEnv):

    def __init__(self):
        self.blind_id = None
       
 
    def set_blind_id(id1):
        self.blind_id = id1    

    
    def state2info(self, infos):
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos)-1].private_state = copy.deepcopy(self.private_state)        


    #@override
    def init(self, players):
        isTerminal = False
        scores     = []
        infos      = [Info(), Info(), Info()]

        if len(players) != 2:
            raise Exception("NoLimitTexasHoldemPoker is a game with two players.")

        self.public_state       = PublicState()
        self.public_state.chips = [0,0]
        if self.blind_id == None:
            self.public_state.blind_id  = int(random.random() * len(players))
        else:
            self.public_state.blind_id  = self.blind_id
        self.public_state.chips[self.public_state.blind_id] =  5        
        self.public_state.turn                              =  2 - self.public_state.blind_id
        self.public_state.public_cards                      = []
        self.public_state.previous_id                       = -1
        self.public_state.previous_action                   = None

        self.private_state = PrivateState() 
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(Card(i,j))
        random.shuffle(allcards)        
        self.private_state.hand_cards       = [[],[]]
        self.private_state.hand_cards[0]    = allcards[0:2]
        self.private_state.hand_cards[1]    = allcards[2:4]
        self.private_state.keep_cards       = allcards[4:9]         
        
        #gen info
        self.state2infos(infos)
        for i in xrange(len(players)-1):
            infos[i].player_id = i
        
        return isTerminal, scores, infos

    #@Override
    def isActionValid(self, action):
        pass

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        pass

        

