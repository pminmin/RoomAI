#!/bin/python
#coding:utf-8

import random
import copy
import roomai.abstract

from NoLimitTexasHoldemPokerUtil import *

class NoLimitTexasHoldemPokerEnv(roomai.abstract.AbstractEnv):

    def __init__(self):
        self.blind_id = None
       
 
    def set_blind_id(id1):
        self.blind_id = id1    

    
    def state2info(self):
        infos = [Info(), Info(), Info()]
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos)-1].private_state = copy.deepcopy(self.private_state)        

    def judge_winner_with_cards(self):
        for i in xrange(self.public_state.num_public_cards, len(self.private_state.keep_cards)):
            self.public_state.public_cards.append(self.private_state.keep_cards[i])
        self.public_state.num_public_cards = len(self.public_state.public_cards)
        
        pattern0 = cards2pattern(self.private_state.hand_cards[0], self.public_state.public_cards)
        pattern1 = cards2pattern(self.private_state.hand_cards[1], self.public_state.public_cards)

        if pattern0[5] > pattern1[5]:
            pass

        elif pattern0[5] < pattern1[5]:
            pass
        else: #=
            pass
        return scores

    #@override
    def init(self):
        isTerminal = False
        scores     = []
        
        self.public_state       = PublicState()
        self.public_state.chips = [0,0]
        if self.blind_id == None:
            self.public_state.blind_id  = int(random.random() * 2)
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
        infos = self.state2infos()
        for i in xrange(2):
            infos[i].player_id = i
        
        return isTerminal, scores, infos

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        isTerminal = False
        turn = self.public_state.turn

        if action.option == ActionSpace.quit:
            if self.public_state.previous_action.option in [ActionSpace.check, ActionSpace.bet]:
                isTerminal      = True
                scores          = [0,0]
                scores[turn]    = sum(chips)                
                scores[1-turn]  = -sum(chips)
            else:   #quit
                pass

        elif action.option == ActionSpace.check:
            if self.public_state.previous_action.option == ActionSpace.check:
                self.judge_winner            

            elif self.public_state.previous_action.option == ActionSpace.bet:
                pass
            else:   ##self.public_state.previous_action.option == ActionSpace.quit
                pass
        elif action.option == ActionSpace.bet:
            if self.public_state.previous_action.option in [ActionSpace.check, ActionSpace.bet]:
                pass
            else:   #quit
                pass
            self.public_state.chips[turn] += action.price
            self.public_state.previous_id  = self.public_state.turn
            
                      

        

