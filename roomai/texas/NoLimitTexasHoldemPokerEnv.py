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
        self.big_blind_bet  = 10

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
        self.public_state.big_blind_bet         = self.big_blind_bet
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

        if self.public_state.chips[big] > self.big_blind_bet:
            self.public_state.chips[big] -= self.big_blind_bet
            self.public_state.bets[big]  += self.big_blind_bet
        else:
            self.public_state.bets[big]     = self.public_state.chips[big]
            self.public_state.chips[big]    = 0
            self.public_state.is_allin[big] = True
            self.public_state.num_allin    += 1

        if self.public_state.chips[small] > self.big_blind_bet / 2:
            self.public_state.chips[small] -= self.big_blind_bet /2
            self.public_state.bets[small]  += self.big_blind_bet /2
        else:
            self.public_state.bets[small]     = self.public_state.chips[small]
            self.public_state.chips[small]    = 0
            self.public_state.is_allin[small] = True
            self.public_state.num_allin      += 1

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
            infos[i].init_player_id  = i
            infos[i].init_hand_cards = self.private_state.hand_cards[i]
        
        return isTerminal, scores, infos

    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):

        isTerminal = False
        scores     = []
        infos      = []
        pu         = self.public_state
        pr         = self.private_state

        if action.option == OptionSpace.Fold:
            self.action_call(action)
        elif action.option == OptionSpace.Check:
            self.action_check(action)
        elif action.option == OptionSpace.Call:
            self.action_call(action)
        elif action.option == OptionSpace.Raise:
            self.action_raise(action)
        else:
            raise Exception("action.option(%d) not in [Fold(0), Check(1), Call(2), Raise(3)]")

        # if it is time to showdown
        if self.is_showdown():
            isTerminal = True
            scores = self.showdown()

        # if it is time to enter into the next stage
        if self.next_player(pu.turn) == pu.flag_for_nextstage:
            add_cards = []
            if pu.stage == StageSpace.firstStage:   add_cards = pr.keep_cards[0:3]
            if pu.stage == StageSpace.secondStage:  add_cards = pr.keep_cards[3]
            if pu.stage == StageSpace.thirdStage:   add_cards = pr.keep_cards[4]

            pu.public_cards.append(add_cards)
            pu.stage = pu.stage + 1

        pu.previous_id                   = pu.turn
        pu.previous_action               = action
        pu.turn                          = self.next_player(pu.turn)

        infos                            = self.state2info()
        infos[pu.turn].available_actions = self.available_action_options()
        return isTerminal, scores, infos

    #override
    @classmethod
    def round(cls, env, players):
        total_scores = [0    for i in xrange(len(players))]
        count        = 0

        ## the first match
        env.chips       = [1000 for i in xrange(len(players))]
        env.num_players = len(players)
        env.dealer_id   = int(random.random * len(players))
        isTerminal, _, infos = env.init()
        for i in xrange(len(players)):
            players[i].receiveInfo(infos[i])
        while isTerminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].takeAction()
            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receiveInfo(infos[i])

        for i in xrange(len(players)):  total_scores[i] += scores[i]
        count += 1

        ## the following matches
        while True:
            dealer = (env.public_state.dealer_id + 1)%len(players)
            while env.public_state.chips[dealer]  == 0:
                dealer = (env.public_state.dealer_id + 1) % len(players)
            next_players_id = []  ## the available players (who still have bets) for the next match
            next_chips      = []
            next_dealer_id  = -1
            for i in xrange(len(env.public_state.chips)):
                if env.public_state.chips[i] > 0:
                    next_players_id.append(i)
                    next_chips.append(env.public_state.chips[i])
                    if i == dealer: next_dealer_id = len(next_players_id) - 1

            if len(next_players_id) == 1: break;

            if count % 10 == 0: env.big_blind_bet = env.big_blind_bet * 2
            env.chips       = next_chips
            env.dealer_id   = next_dealer_id
            env.num_players = len(next_players_id)
            isTerminal, _, infos = env.init()
            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                players[idx].receiveInfo(infos[i])
            while isTerminal == False:
                turn = infos[-1].public_state.turn
                idx = next_players_id[turn]
                action = players[idx].takeAction()
                isTerminal, scores, infos = env.forward(action)
                for i in xrange(len(next_players_id)):
                    idx = next_players_id[i]
                    players[idx].receiveInfo(infos[i])

            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                total_scores[idx] += scores[i]
            count += 1

        for i in xrange(len(players)): total_scores[i] /= count * 1.0
        return total_scores;


    def next_player(self,i):
        pu = self.public_state

        p = (i+1)%pu.num_players
        while (pu.is_quit[p] or pu.is_allin[p]) and p != pu.flag_for_nextstage:
            p = (p+1)%pu.num_players

        return p

    def is_action_valid(self, action):
        '''
        :return: A boolean variable, which indicates whether is the action valid on the current state
        '''

    def available_action_options(self):
        '''
        :return: 
            A dict contains all available actions options
        '''

    def state2info(self):
        infos = [Info() for i in xrange(self.public_state.num_players)]
        for i in xrange(len(infos)):
            infos[i].public_state = copy.deepcopy(self.public_state)
        infos[len(infos) - 1].private_state = copy.deepcopy(self.private_state)

    def is_showdown(self):
        '''
        :return: 
        A boolean variable indicates whether is it time to showdown
        '''
        pu = self.public_state

        if pu.num_players - 1 == pu.num_allin + pu.num_quit:
            return True
        if pu.stage == StageSpace.fourthStage and \
                        self.next_player(pu.turn) == pu.flag_for_nextstage:
            return True

        return False

    def showdown(self):
        pu = self.public_state
        scores = [0 for i in xrange(pu.num_players)]
        return scores

    def action_fold(self, action):
        pu = self.public_state
        pu.is_quit[pu.turn] = True
        pu.num_quit += 1

    def action_check(self, action):
        pass

    def action_call(self, action):
        pu = self.public_state
        if pu.bets[pu.turn] < pu.max_bet:
            pu.chips[pu.turn] -= (pu.max_bet - pu.bets[pu.turn])
            pu.bets[pu.turn] = pu.max_bet

        if pu.chips[pu.turn] == 0:
            pu.num_allin += 1
            pu.is_allin[pu.turn] = True

    def action_raise(self, action):
        pu = self.public_state

        if pu.bets[pu.turn] < pu.max_bet:
            pu.chips[pu.turn] -= (pu.max_bet - pu.bets[pu.turn])
            pu.bets[pu.turn]   = pu.max_bet
        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn] += action.price

        if pu.chips[pu.turn] == 0:
            pu.num_allin += 1
            pu.is_allin[pu.turn] = True

        pu.max_bet = pu.bets[pu.turn]
        pu.flag_for_nextstage = pu.turn
