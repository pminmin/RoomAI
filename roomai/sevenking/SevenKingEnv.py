#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPublicState
from roomai.sevenking import SevenKingPrivateState
from roomai.sevenking import SevenKingPersonState
from roomai.sevenking import SevenKingAction


AllPatterns = dict()
###
###numCards, requireSamePoint, requireStraight
AllPatterns["p_0_0_0"] = ("p_0_0_0",0,0,0) ## check
AllPatterns["p_1_1_0"] = ("p_1_1_0",1,1,0)
AllPatterns["p_2_1_0"] = ("p_1_1_0",2,1,0)
AllPatterns["p_3_1_0"] = ("p_3_1_0",3,1,0)
AllPatterns["p_4_1_0"] = ("p_4_1_0",4,1,0)
AllPatterns["p_3_0_1"] = ("p_3_0_1",3,0,1)
AllPatterns["p_4_0_1"] = ("p_4_0_1",4,0,1)
AllPatterns["p_5_0_1"] = ("p_3_0_1",5,0,1)

class SevenKingEnv(roomai.common.AbstractEnv):
    num_players = 2

    def init(self):
        self.public_state  = SevenKingPublicState()
        self.private_state = SevenKingPrivateState()
        self.person_states = [SevenKingPersonState() for i in range(self.num_players)]

        self.public_state_history  = []
        self.private_state_history = []
        self.person_states_history = []

        self.gen_history()
        infos = self.gen_infos()
        return infos, self.public_state, self.person_states, self.private_state

    def forward(self, action):
        self.gen_history()
        infos = self.gen_infos()
        return infos, self.public_state, self.person_states, self.private_state


    @classmethod
    def action2pattern(cls, action):
        ###numCards, isSamePoint, isStraight
        num_cards               = len(action.cards)
        if num_cards == 0:
            return AllPatterns["p_0_0_0"]
        else:
            isSamePoint = 1
            isStraight  = 1
            point  = action.cards[0].get_point_rank()
            for i in range(1,len(action.cards)):
                card = action.cards[i]
                if point != card.get_point_rank():
                    isSamePoint = 0
                if point != card.get_point_rank() - 1:
                    isStraight  = 0
                point = card.get_point_rank()
            return AllPatterns["p_%d_%d_%d"%(num_cards,isSamePoint,isStraight)]

    @classmethod
    def gen_available_actions(cls, public_state, person_state):
        available_actions      = dict()
        available_actions[""]  = SevenKingAction("")

        previous_action = public_state.previous_action
        if previous_action is None:
            previous_action = SevenKingAction("")

        return available_actions

