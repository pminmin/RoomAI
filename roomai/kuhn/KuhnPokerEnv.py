#!/bin/python
import random
import math
import copy
import roomai.abstract
from KuhnPokerUtils import *;

class KuhnPokerEnv(roomai.abstract.AbstractEnv):

    #@override
    def init(self):
        self.available_action = dict()
        self.available_action[KuhnPokerAction("check").get_key()] = KuhnPokerAction("check")
        self.available_action[KuhnPokerAction("bet").get_key()]   = KuhnPokerAction("bet")

        self.private_state = KuhnPokerPrivateState()
        self.public_state  = KuhnPokerPublicState()
        self.person_states = [KuhnPokerPersonState() for i in xrange(2)]

        card0 = math.floor(random.random() * 3)
        card1 = math.floor(random.random() * 3)
        while card0 == card1:
            card0 = math.floor(random.random() * 3)
        self.private_state.hand_cards = [card0, card1]

        self.public_state.turn          = int(random.random() * 2)
        self.public_state.first         = self.public_state.turn
        self.public_state.epoch         = 0
        self.public_state.action_list   = []
        self.person_states[0].id = 0
        self.person_states[0].card      = card0
        self.person_states[1].id        = 1
        self.person_states[1].card      = card1

        infos = self.gen_infos()
        
        return False, [], infos, self.public_state, self.person_states, self.private_state

    #@override
    def forward(self, action):
        self.person_states[self.public_state.turn].available_actions = None
        self.public_state.epoch                                     += 1
        self.public_state.turn                                       = (self.public_state.turn+1)%2
        self.public_state.action_list.append(action.get_key())
        infos = self.gen_infos()

        if self.public_state.epoch == 1:
            return False, [], infos, self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 2:
            scores = self.evaluteTwo()
            if scores[0] != -1:
                return True, scores, infos,self.public_state, self.person_states, self.private_state
            else:
                return False, [],    infos,self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 3:
            scores = self.evaluteThree()
            return True, scores, infos,self.public_state, self.person_states, self.private_state

        else:
            raise Exception("KuhnPoker has 3 turns at most")

    #@Overide
    @classmethod
    def compete(cls, env, players):

        isTerminal, scores, infos, public_state, person_state, private_state = env.init()
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])

        while isTerminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()
            isTerminal, scores, infos,public_state, person_state, private_state = env.forward(action)
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

        return scores

    def gen_infos(self):
        infos = [KuhnPokerInfo(), KuhnPokerInfo()]
        for i in xrange(len(infos)):
            infos[i].person_state = copy.deepcopy(self.person_states[i])
            infos[i].public_state = copy.deepcopy(self.public_state)

        turn = self.public_state.turn
        infos[turn].person_state.available_actions = self.available_action

        return infos

    def WhoHasHigherCard(self):
        hand_cards = self.private_state.hand_cards
        if hand_cards[0] > hand_cards[1]:
            return 0
        else:
            return 1

    def evaluteTwo(self):
        win    = self.WhoHasHigherCard()
        first  = self.public_state.first
        scores = [0, 0];
        actions = self.public_state.action_list
        
        if actions[0] == "check" and \
           actions[1] == "bet":
            return [-1,-1]
        
        if actions[0] == actions[1] and \
           actions[0] == "check":
            scores[win] = 1;
            return scores;

        if actions[0] == "bet" and \
           actions[1] == "check":
            scores[first] = 1;
            return scores;

        if actions[0] == actions[1] and \
           actions[0] == "bet":
            scores[win] = 2
            return scores;


    def evaluteThree(self):
        first   = self.public_state.first 
        win     = self.WhoHasHigherCard()
        scores  = [0, 0]
        if self.public_state.action_list[2] == "check":
            scores[1 - first] = 1;
        else:
            scores[win] = 2;
        return scores;
       
