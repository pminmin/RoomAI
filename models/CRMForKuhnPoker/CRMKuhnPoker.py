#!/bin/python
from roomai.algorithms import CRMPlayer
from roomai.algorithms import CRMAlgorithm
from roomai.kuhn       import KuhnPokerEnv
import random

class KuhnPokerCRMPlayer(CRMPlayer):
    def __init__(self):
        super.__init__()
        self.regret_dict         = dict()
        self.state               = None
        self.actions_regret      = []
        self.actions_prob        = []
    def receive_info(self, info):
        if info.public_state.is_terminal == True:
            return

        id      = info.person_state.id
        card    = info.person_state.card
        history = info.public_state.action_history

        self.state   = "%d_%d_%s"%(id,card,"".join(history))
        if self.state not in self.regret_dict:
            self.regret_dict[self.state] = []
            for action in info.person_state.available_actions:
                self.regret_dict.append((action.get_key(),1.0/len(info.person_state.available_actions)))

        self.actions_regret = self.regret_dict[self.state]
        self.actions_prob   = []
        sum1 = 0
        for action_regret in self.actions_regret:
            sum1 += max(0, action_regret[1])
        if sum1 > 0:
            for action_regret in self.actions_regret:
                self.actions_prob.append((action_regret[0], max(0,action_regret[1])/sum1))
        else:
            for action_regret in self.actions_regret:
                self.actions_prob.append((action_regret[0], 1.0 / len(self.actions_prob)))


    def get_actions_prob(self):
        return self.actions_prob

    def get_actions_regret(self):
        return self.actions_prob

    def update_actions_regret(self, origin_actions_regret, target_actions_regret):
        self.regret_dict[self.state] = target_actions_regret

    def take_action(self):
        r    = random.random()
        sum1 = 0
        for i in xrange(len(self.actions_prob)):
            sum1 += self.actions_prob[i][0]
            if sum1 > r:
                return self.actions_prob[i][1]

        return self.actions_prob[len(self.actions_prob)-1][1]


    def reset(self):
        pass

if __name__ == "__main__":
    env     = KuhnPokerEnv()
    players = [KuhnPokerCRMPlayer() for i in xrange(2)]

    algo    = CRMAlgorithm()
    for i in xrange(1000):
        algo.dfs(env = env,players=players,player_probs = [1,1],action=None,deep = 0)