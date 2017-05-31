#!/bin/python
import roomai.abstract
import tensorflow

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
        chips     = info.public_state.chips
        bets      = info.public_state.bets
        floor_bet = info.public_state.floor_bet

        players   = info.public_state.first_