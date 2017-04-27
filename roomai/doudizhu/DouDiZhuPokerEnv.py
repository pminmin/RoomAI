#!/bin/python
#coding:utf-8

import roomai.abstract
import random
import copy
import roomai
from roomai.doudizhu.DouDiZhuPokerUtils import *

class DouDiZhuPokerEnv(roomai.abstract.AbstractEnv):

    def __init__(self):
        self.is_force_check = True ## an issure left over by history
        self.public_state   = PublicState_DouDiZhu()
        self.private_state  = PrivateState_DouDiZhu()
        self.person_states  = [PersonState_DouDiZhu() for i in xrange(3)]
        for i in xrange(3):
            self.person_states[i].id = i
        self.logger         = roomai.get_logger()

    def gen_infos(self):
        infos = [Info_DouDiZhu() for i in xrange(4)]
        infos[3].private_state    = copy.deepcopy(self.private_state)
        for i in xrange(3):
            infos[i].person_state = copy.deepcopy(self.person_states[i])
        for i in xrange(4):
            infos[i].public_state = copy.deepcopy(self.public_state)

        return infos

    def update_license(self, turn, action):
        if action.pattern[0] != "i_cheat":
            self.public_state.license_playerid = turn
            self.public_state.license_action   = action 

    def update_cards(self, turn, action):
        self.private_state.hand_cards[turn].remove_action(action)

    def update_phase_bid2play(self):
        self.public_state.phase            = PhaseSpace.play
        
        self.public_state.landlord_id      = self.public_state.landlord_candidate_id
        self.public_state.license_playerid = self.public_state.turn        

        landlord_id = self.public_state.landlord_id
        self.person_states[landlord_id].add_cards = copy.deepcopy(self.private_state.keep_cards)
        self.private_state.hand_cards[landlord_id].add_cards(self.private_state.keep_cards)


    def is_action_valid(self, action):
        public_state = self.public_state
        turn = public_state.turn
        hand_cards = self.private_state.hand_cards[turn]
        return Utils_DouDiZhu.is_action_valid(hand_cards, public_state, action)

    #@Overide
    def init(self):

        self.public_state.firstPlayer       = int(random.random() * 3)
        self.public_state.turn              = self.public_state.firstPlayer
        self.public_state.phase             = PhaseSpace.bid
        self.public_state.epoch             = 0
        self.public_state.landlord_id       = -1
        self.public_state.license_playerid  = self.public_state.turn
        self.public_state.license_action    = None

        cards = []
        for i in xrange(13):
            for j in xrange(4):
                cards.append(ActionSpace_DouDiZhu.key_to_str[i])
        cards.append(ActionSpace_DouDiZhu.key_to_str[13])
        cards.append(ActionSpace_DouDiZhu.key_to_str[14])
        random.shuffle(cards)

        hand_cards = []
        for i in xrange(3):
            tmp = cards[i * 17:(i + 1) * 17]
            tmp.sort()
            hand_cards.append(HandCards("".join(tmp)))
        keep_cards = HandCards([cards[-1], cards[-2], cards[-3]])

        self.private_state.hand_cards = hand_cards;
        self.private_state.keep_cards = keep_cards;
        for i in xrange(3):
            self.person_states[i].cards = copy.deepcopy(hand_cards[i])
        turn = self.public_state.turn
        hand_cards = self.private_state.hand_cards[turn]
        self.person_states[turn].available_actions = Utils_DouDiZhu.candidate_actions(hand_cards, self.public_state)

        infos = self.gen_infos()
        return False, [], infos;


    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):

        if self.is_force_check == True and not self.is_action_valid(action):
            self.logger.critical("action=%s is invalid"%(action.toString()))
            raise ValueError("action=%s is invalid"%(action.toString()))

        isTerminal   = False
        scores       = []
        turn = self.public_state.turn
        turnNotChange = False

        if self.public_state.phase == PhaseSpace.bid:  
            
            if action.pattern[0] == "i_bid":
                self.public_state.landlord_candidate_id = turn

            new_landlord_candidate_id = self.public_state.landlord_candidate_id
            if self.public_state.epoch == 3 and new_landlord_candidate_id == -1:
                infos = self.gen_infos()
                return True,[0,0,0], infos

            if (self.public_state.epoch == 2 and new_landlord_candidate_id != -1)\
                or self.public_state.epoch == 3:
                    self.update_phase_bid2play()
                    turnNotChange = True
                     

        else: #phase == play

            self.person_states[self.public_state.landlord_id].add_cards = None

            if action.pattern[0] != "i_cheat":

                self.update_cards(turn,action)
                self.update_license(turn,action)                
    
                num = self.private_state.hand_cards[turn].num_cards
                if num == 0:
                    isTerminal = True
                    if turn == self.public_state.landlord_id:
                        scores = [-1,-1,-1]
                        scores[self.public_state.landlord_id] = 2
                    else:
                        scores = [1,1,1]
                        scores[self.public_state.landlord_id] = -2

        if turnNotChange == False:
            self.public_state.turn            = (turn+1)%3
        self.public_state.is_response         = True
        if self.public_state.turn == self.public_state.license_playerid:
            self.public_state.is_response     = False
        self.public_state.previous_id         = turn
        self.public_state.previous_action     = action
        self.public_state.epoch              += 1

        self.person_states[self.public_state.previous_id].available_actions = None
        hand_cards = self.private_state.hand_cards[self.public_state.turn]
        self.person_states[self.public_state.turn].available_actions        = Utils_DouDiZhu.candidate_actions(hand_cards, self.public_state)
        infos = self.gen_infos()

        return isTerminal, scores, infos


    #@override
    @classmethod
    def round(cls, env, players):
        isTerminal, _, infos = env.init()
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])

        while isTerminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()

            isTerminal, scores, infos = env.forward(action)
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

        return scores