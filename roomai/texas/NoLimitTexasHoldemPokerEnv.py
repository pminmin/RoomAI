#!/bin/python
#coding:utf-8

import random
import copy
import roomai.abstract

from NoLimitTexasHoldemPokerUtil import *

class NoLimitTexasHoldemPokerEnv(roomai.abstract.AbstractEnv):

    def __init__(self):
        self.num_players    = 3 
        self.dealer_id      = int(random.random * self.num_players)
        self.chips          = [0.0 for i in xrange(self.num_players)]

    def state2info(self):
        infos = [Info() for i in xrange(self.num_players)]
        for i in xrange(len(infos)):
            infos[i].public_state = self.public_state
        infos[len(infos)-1].private_state = self.private_state

    def compute_scores(self, win_id):
        num_players = len(self.private_state.hand_cards)
        scores      = [0 for i in xrange(num_players)]
        sum1        = sum(self.chips)
        scores[win_id] = sum1
        for i in xrange(len(self.private_state.hand_cards)):
            if i == win_id: continue
            scores[i] =  -self.public_state.chips[i]
        return scores


    # Before init, you need set the num_players, dealer_id, and chips
    #@override
    def init(self):
        isTerminal = False
        scores     = []

        #init the public state
        self.public_state                   = PublicState()
        self.public_state.num_players       = self.num_players
        self.public_state.chips             = self.chips
        self.public_state.stage             = StageSpace.firstStage
        self.public_state.is_quit           = [False for i in xrange(self.num_players)]
        self.public_state.num_quit          = 0
        self.public_state.is_allin          = [False for i in xrange(self.num_players)]
        self.public_state.num_allin         = 0
        self.public_state.public_cards      = []
        self.public_state.previous_id       = None
        self.public_state.previous_action   = None

        self.public_state.pots = [0 for i in xrange(self.num_players)]
        small_blind_id =  (self.dealer_id+1)%self.num_players
        big_blind_id   =  (self.dealer_id+2)%self.num_players
        self.public_state.pots[small_blind_id] += 5
        self.public_state.pots[big_blind_id]   += 10

        self.public_state.turn              = (big_blind_id+1)%self.num_players

        # init the private state
        self.private_state = PrivateState() 
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(Card(i,j))
        random.shuffle(allcards)        
        self.private_state.hand_cards       = [[] for i in xrange(self.num_players)]
        for i in xrange(self.num_players):
            self.private_state.hand_cards[i]    = allcards[i*2:(i+1)*2]
        self.private_state.keep_cards   = allcards[self.num_players*2:self.num_players*2+5]         
        
        #gen info
        infos = self.state2infos()
        for i in xrange(2):
            infos[i].player_id = i
        
        return isTerminal, scores, infos

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):

        if is_action_valid(action) == False:
            raise  Exception("invalid action")

        pu = self.public_state
        pr = self.private_state

        if pu.stage == StageSpace.firstStage:
            turn = pu
            if action.option == OptionSpace.Fold:
                pu.is_quit[turn] = True
                pu.num_quit += 1
            elif action.option == OptionSpace.Check:
                pass
            elif action.option == OptionSpace.Call:
                previous_id = pu.previous_id;
                money = pu.pots[previous_id]
                pu.pots[turn] = money
            elif action.option == OptionSpace.Raise:
                pass

            if is_ready_for_showdown() == True:
                adf = 0
            elif is_ready_for_nextstage() == True:
                afd = 0
            else:
                pu.turn = self.next_turn()

       elif self.public_state.stage == StageSpace.secondStage:

       elif self.public_state.stage == StageSpace.thirdStage:

       elif self.public_state.stage == StageSpace.fourthStage:

       else:
           raise
             

    @classmethod
    def round(cls, env, players, num_round):
        pass
    def is_ready_for_nextstage(self):
        pass

    def is_ready_for_showdown(self):
        pass
    def is_action_valid(self,action):
        pass
    def next_turn(self):
        pu = self.public_state

        turn = self.public_state.turn
        n_turn = (turn + 1) % pu.num_players
        while pu.is_quit[n_turn] == True or pu.is_allin[n_turn] == True:
            n_turn = (n_turn + 1) % pu.num_players
        return n_turn