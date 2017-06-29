#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPublicState
from roomai.sevenking import SevenKingPrivateState
from roomai.sevenking import SevenKingPersonState

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