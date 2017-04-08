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
        big   = (self.dealer_id + 2) % self.num_players

        self.public_state                       = PublicState()
        self.public_state.dealer_id             = self.dealer_id
        self.public_state.is_quit               = [False for i in xrange(self.num_players)]
        self.public_state.num_quit              = 0
        self.public_state.is_allin              = [False for i in xrange(self.num_players)]
        self.public_state.num_allin             = 0
        self.public_state.bets                  = [0 for i in xrange(self.num_players)]
        self.public_state.chips                 = self.chips
        self.public_state.stage                 = StageSpace.firstStage
        self.public_state.turn                  = self.next_player(big)
        self.public_state.flag_for_nextstage    = self.next_player(big)

        self.public_state.previous_id           = None
        self.public_state.previous_action       = None

        self.public_state.bets[small]   = 5
        self.public_state.bets[big]     = 10
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
        self.process_action(action)

        pu = self.public_state
        pr = self.private_state
        pu.turn = self.next_player(pu.turn)

        if self.is_showdown():

        ## it is time to enter into the next stage
        if pu.turn == pu.flag_for_nextstage:
            if pu.stage == StageSpace.firstStage:
                pu.public_cards.append(pr.keep_cards[0:3])
                pu.stage = StageSpace.secondStage

            elif pu.stage == StageSpace.secondStage:
                pu.public_cards.append(pr.keep_cards[3])

            elif pu.stage == StageSpace.thirdStage:
                pu.public_cards.append(pr.keep_cards[4])

            elif pu.stage == StageSpace.fourthStage:


            else:
                raise Exception("public.stage(%d) not in [1,2,3,4]"%(pu.stage))


    def process_action(self, action):
        pu = self.public_state
        if action.option == OptionSpace.Fold:
            pu.is_quit[pu.turn]  = True
            pu.num_quit         += 1

        elif action.option == OptionSpace.Check:
            pass

        elif action.option == OptionSpace.Call:
            if pu.bets[pu.turn] < pu.max_bet:
                pu.chips[pu.turn] -= (pu.max_bet - pu.bets[pu.turn])
                pu.bets[pu.turn]   =  pu.max_bet

        elif action.option == OptionSpace.Raise:
            if pu.bets[pu.turn] < pu.max_bet:
                pu.chips[pu.turn] -= (pu.max_bet - pu.bets[pu.turn])
                pu.bets[pu.turn]   =  pu.max_bet

            pu.chips[pu.turn] -= action.price
            pu.bets[pu.turn]  += action.price

            pu.max_bet         = pu.bets[pu.turn]

            pu.flag_for_nextstage = pu.turn

        else:
            raise Exception("action.option(%d) not in [Fold(0), Check(1), Call(2), Raise(3)]")

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


    def is_showdown(self):
        '''
        :return: 
        A boolean variable indicates whether is it time to showdown
        '''
        pu = self.public_state

        if pu.num_players - 1 == pu.num_allin + pu.num_quit:
            return True
        if  pu.stage == StageSpace.fourthStage and \
            pu.turn == pu.flag_for_nextstage:
            return True

        else:
            return False


    def next_player(self,i):
        pu = self.public_state

        p = (i+1)%pu.num_players
        while (pu.is_quit[p] or pu.is_allin[p]) and p != pu.flag_for_nextstage:
            p = (p+1)%pu.num_players

        return p