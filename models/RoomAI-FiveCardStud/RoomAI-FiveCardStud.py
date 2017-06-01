#!/bin/python
import roomai.abstract
import tensorflow as tf
import numpy as np

class Player(roomai.abstract.AbstractPlayer):


    def __init__(self, is_train = True, num_players = 3):
        self.is_train =  is_train




    #@take a action
    def take_action(self):
        pass

    #@reset
    def reset(self):
        pass

    #@receive_info
    def receive_info(self, info):
        pu             = info.public_state
        pe             = info.person_state

        if pu.turn != pe.id:    return

        floor_bet           = pu.floor_bet
        self.chips          = np.asarray(pu.chips) /floor_bet
        self.bets           = np.asarray(pu.bets)  /floor_bet


        self.hand_cards          = parseCards(pu, pe.id)
        self.opponent_hand_cards = []
        for i in xrange(pu.num_players):
            if i != pe.id:
                self.opponent_hand_cards.append(parseCards(pu,i))
        


def parseCards(public_state, player_id):
    pu    = public_state
    cards =np.asarray([[0 for j in xrange(4)] for i in xrange(13)])

    hand_cards_set = [pu.second_hand_cards,pu.third_hand_cards,pu.fourth_hand_cards, pu.fifth_hand_cards]
    for hand_cards in hand_cards_set:
        if hand_cards is not None:
            card = hand_cards[player_id]
            cards[card.get_point_rank(), card.get_suit_rank()]

    return cards