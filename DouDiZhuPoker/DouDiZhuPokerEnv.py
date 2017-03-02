#!/bin/python
#coding:utf-8
from AbstractEnvPlayer import *;
from DouDiZhuPokerUtil import *;

import random
import copy

class DouDiZhuPokerEnv(AbstractEnv):

    def __init__(self):
        self.public_state  = PublicState()
        self.private_state = PrivateState() 

    def generateInitialCards(self):
        cards = [];

        for i in xrange(13):
            for j in xrange(4):
                cards.append(i)
        cards.append(13)
        cards.append(14)
        random.shuffle(cards)

        handCards    = [[0 for j in xrange(15)] for i in xrange(3)]
        for i in xrange(len(cards)-3):
            idx = cards[i]
            handCards[i%3][idx] += 1

        keepCards = cards[-3:]

        return handCards, keepCards;

    #@Override
    def isActionValid(self, action):
        if action.isComplemented() == False:
            action.complement()

        if action.pattern[0] == "i_invalid":
            return False;

        turnCards = self.private_state.hand_cards[self.public_state.turn] 
        if isActionGeneratedFromCards(action, turnCards) == False:
            return False


        if self.public_state.phase == Phase.bid:
            if action.pattern[0] not in ["i_cheat","i_bid"]:  
                return False
            return True
                
        elif self.public_state.phase == Phase.play:
            license_action = self.public_state.license_action
            
            if action.pattern[0]  == "i_bid":  
                return False
            elif action.pattern[0]  == "i_cheat":
                if self.public_state.turn == self.public_state.license_id:
                    return False
                return True
            

            if self.public_state.turn == self.public_state.license_id:
                return True

            elif action.pattern[6] > license_action.pattern[6]:  
                return True
               
            elif action.maxMasterCard - license_action.maxMasterCard > 0: 
                return True

            else:
                return False


    #@Overide
    def init(self, players):
         
        if len(players) != 3:
            raise Exception("The DouDiZhuPoker is a game with two players, len(players) = %d"%(len(players)))

        ## init the info
        infos  = [Info(), Info(), Info(), Info()]; 
        
        self.private_state.hand_cards, self.private_state.additive_cards \
        = self.generateInitialCards()
        self.private_state.num_hand_cards     = [17,17,17]
        
        self.public_state.firstPlayer      = int(random.random() * 3)
        self.public_state.turn             = self.public_state.firstPlayer
        self.public_state.phase            = Phase.bid
        self.public_state.epoch            = 0
        
        self.public_state.landlord_id       = -1
        self.public_state.license_id        = self.public_state.turn
        self.public_state.license_action    = None

        for i in xrange(3):
            infos[i].init_id         = i
            infos[i].init_cards      = self.private_state.hand_cards[i];
            infos[i].public_state    = copy.deepcopy(self.public_state)
        infos[3].public_state        = copy.deepcopy(self.public_state)
        infos[3].private_state       = copy.deepcopy(self.private_state)


        return False, [], copy.deepcopy(infos);


    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        isTerminal   = False
        scores       = []
        infos        = [Info(), Info(), Info(), Info()]

        if action.isComplemented() == False:
            action.complement() 

        flag = False
        turn = self.public_state.turn

        if self.public_state.phase == Phase.bid:  

            if self.public_state.epoch == 0:      
                if action.pattern[0] == "i_bid":
                    self.public_state.landlord_candidate_id =\
                        self.public_state.turn

            elif self.public_state.epoch == 1:
                if action.pattern[0] == "i_bid":
                    self.public_state.landlord_candiate_id  = \
                        self.public_state.turn

            elif self.public_state.epoch == 2:
                if action.pattern[0] == "i_bid":
                    self.public_state.landlord_candidate_id = \
                        self.public_state.turn

                if self.public_state.landlord_candidate_id == -1:   
                ## no player bids for landlord
                    self.public_state.landlord_candiate_id = \
                        self.public_state.first_player
        
                self.public_state.landlord_id = \
                    self.public_state.landlord_candidate_id
                infos[self.public_state.landlord_id].init_addcards =\
                    copy.deepcopy(self.private_state.additive_cards)
                self.public_state.phase = Phase.play

                flag = True

        else: #phase == play

            if action.pattern[0] == "i_cheat":
                pass

            elif action.pattern[1] + action.pattern[4] ==\
                 self.public_state.num_hand_cards[turn]:

                removeActionFromCards(action, self.public_state.hand_cards[turn])
                self.public_state.num_hand_cards[turn] = 0
                self.public_state.licese_id = \
                    (self.public_state.license_id+1)%3
                self.public_state.license_action = action

                isTerminal = True
                if self.public_state.turn == self.public_state.landlord_id:
                    scores = [-1,-1,-1]
                    scores[self.public_state.landlord_id] = 2
                else:
                    scores = [1,1,1]
                    scores[self.public_state.landlord_id] = -2
                

            else: #action.pattern[0] != "i_cheat" and not complete
                ## the action exerts the influence
                removeActionFromCards(action, self.public_state.hand_cards[turn])
                self.public_state.num_hand_cards[turn] -= \
                    action.pattern[1]+ action.pattern[4]
                self.public_state.license_id     = \
                    (self.public_state.licenseId+1)%3
                self.public_state.license_action = \
                    action
                

        self.public_state.previous_id         = turn
        self.public_state.previous_action     = action
        self.public_state.turn                = (turn+1)%3
        self.public_state.epoch              += 1

        for i in xrange(3):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[3].public_state  = copy.deepcopy(self.public_state)
        infos[3].private_state = copy.deepcopy(self.private_state)
        
        if flag == True:
            infos[self.public_state.landlord_id].init_addcards = \
                self.private_state.additive_cards

        return isTerminal, scores, copy.deepcopy(infos)


        

