#!/bin/python
import roomai.abstract
import roomai.kuhn.ActionSpace

class KuhnPokerExamplePlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        self.player_id      = -1
        self.card           = -1
        self.public_state   = None
    #@override
    def receiveInfo(self, info):
        if info.player_id is not None:        
            self.player_id = info.player_id
        if info.card is not None:
            self.card = info.card
        if info.public_state is not None:
            self.public_state = info.public_state

    #@override
    def takeAction(self):
        # you are the first player
        if self.player_id == self.public_state.first: 
            ## the first turn
            if len(self.public_state.action_list) == 0: 

            ## the third turn
            else:

        # you are the second player
        else:
            
    
    #@reset
    def reset(self):
        self.player_id      = -1
        self.card           = -1
        self.public_state   = None 
