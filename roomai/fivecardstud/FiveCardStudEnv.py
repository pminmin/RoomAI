#!/bin/python
import roomai.abstract
import copy
import random

from FiveCardStudUtils import Card_FiveCardStud
from FiveCardStudInfo import PublicState_FiveCardStud
from FiveCardStudInfo import PersonState_FiveCardStud
from FiveCardStudInfo import PrivateState_FiveCardStud
from FiveCardStudInfo import Info_FiveCardStud

class FiveCardStudEnv(roomai.abstract.AbstractEnv):
    def __init__(self):
        num_players = 3
        self.logger         = roomai.get_logger()

    def gen_infos(self):
        infos = [Info_FiveCardStud() for i in xrange(4)]
        infos[3].private_state    = copy.deepcopy(self.private_state)
        for i in xrange(3):
            infos[i].person_state = copy.deepcopy(self.person_states[i])
        for i in xrange(4):
            infos[i].public_state = copy.deepcopy(self.public_state)

        return infos

    #@override
    def init(self):
        self.public_state   = PublicState_FiveCardStud()
        self.private_state  = PrivateState_FiveCardStud()
        self.person_states  = [PersonState_FiveCardStud for i in xrange(3)]
        for i in xrange(self.num_players):
            self.person_states[i].id = i

        ## initialize the cards
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(Card_FiveCardStud(i, j))
        random.shuffle(allcards)
        self.private_state.first_hand_cards  = allcards[0:                  1*self.num_players]
        self.private_state.second_hand_cards = allcards[1*self.num_palyers, 2*self.num_players]
        self.private_state.third_hand_cards  = allcards[2*self.num_players, 3*self.num_players]
        self.private_state.fourth_hand_cards = allcards[3*self.num_palyers, 4*self.num_players]
        self.private_state.fifth_hand_cards  = allcards[4*self.num_palyers, 5*self.num_players]

        ##
        for i in xrange(self.num_players):
            self.person_states[i].first_hand_card = self.private_state.first_hand_cards[i]


        return False,[],self.gen_infos()


    #@override
    def forward(self, action):
        pass

    #@override
    def compete(cls, env, players):
        pass
