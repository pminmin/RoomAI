#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingFiveTwoThreePublicState
from roomai.sevenking import SevenKingFiveTwoThreePrivateState
from roomai.sevenking import SevenKingFiveTwoThreePersonState

class SevenKingFiveTwoThreeEnv(roomai.common.AbstractEnv):
    num_players = 2

    def init(self):
        self.public_state  = SevenKingFiveTwoThreePublicState()
        self.private_state = SevenKingFiveTwoThreePrivateState()
        self.person_states = [SevenKingFiveTwoThreePersonState() for i in range(self.num_players)]

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