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
        infos = [Info(), Info(), Info()]
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos)-1].private_state = copy.deepcopy(self.private_state)        

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

        ## public info
        small = (self.dealer_id + 1) % self.num_players
        big   = (self.dealer_id + 1) % self.num_players

        self.public_state                   = PublicState()
        self.public_state.dealer_id         = self.dealer_id
        self.public_state.is_quit           = [False for i in xrange(self.num_players)]
        self.public_state.num_quit          = 0
        self.public_state.is_allin          = [False for i in xrange(self.num_players)]
        self.public_state.num_allin         = 0
        self.public_state.pots              = [0 for i in xrange(self.num_players)]
        self.public_state.chips             = self.chips
        self.public_state.stage             = StageSpace.firstStage
        self.public_state.max_bet_holder    = big
        self.public_state.previous_id       = None
        self.public_state.previous_action   = None

        self.public_state.pots[small]   = 5
        self.public_state.pots[big]     = 10
        self.public_state.chips[small] -= 5
        self.public_state.chips[big]   -= 10

        # private info
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
        pu = self.public_state
        pr = self.private_state

        if pu.stage == StageSpace.firstStage:

        elif pu.stage == StageSpace.secondStage:

        elif pu.stage == StageSpace.thirdStage:

        elif pu.stage == StageSpace.fourthStage:

        else:
            raise Exception("public.stage(%d) not in [1,2,3,4]"%(pu.stage))



    #override
    @classmethod
    def round(cls, env, players, num_round):
        total_scores = [0, 0, 0]
        for i in xrange(num_round):
            isTerminal, _, infos = env.init()

            for i in xrange(len(players)):
                players[i].receiveInfo(infos[i])

            while isTerminal == False:
                turn = infos[-1].public_state.turn
                action = players[turn].takeAction()
                isTerminal, scores, infos = env.forward(action)
                for i in xrange(len(players)):
                    players[i].receiveInfo(infos[i])

            for i in xrange(len(scores)):
                total_scores[i] += scores[i]

        for i in xrange(len(total_scores)):
            total_scores[i] /= num_round * 1.0

        return total_scores

    ### if next_valid_player == max_bet_holder, it is time to enter into the next stage

    def is_ready_for_showdown(self):
        pu = self.public_state

        if pu.num_players - 1 == pu.num_allin + pu.num_quit:
            return True
        if  pu.stage == StageSpace.fourthStage and \
            self.next_valid_player(pu.turn) == pu.max_bet_holder:
            return True

        else:
            return False

    def next_player(self,i):
        return (i+1)%self.num_players

    def next_valid_player(self,i):
        pu = self.public_state
        p = self.next_player(i)
        while (pu.is_quit[p] or pu.is_allin[p]) and p != pu.max_bet_holder:
            p = self.next_player(p)
        return p