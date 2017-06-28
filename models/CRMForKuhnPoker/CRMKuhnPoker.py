#!/bin/python
from roomai.algorithms import CRMPlayer
from roomai.algorithms import CRMAlgorithm
from roomai.kuhn       import KuhnPokerEnv
from roomai.kuhn       import KuhnPokerRandomPlayer
from roomai.kuhn       import KuhnPokerAlwaysBetPlayer
from roomai.kuhn       import KuhnPokerAction
import random

class KuhnPokerCRMPlayer(CRMPlayer):
    def __init__(self):
        self.is_train                  = False
        self.state                     = []
        self.state_actions_regrets     = dict()
        self.state_actions_probs       = dict()


    def receive_info(self, info):
        if self.is_train == True:
            id      = info.person_state.id
            card    = info.person_state.card
            history = info.public_state.action_list


            self.state.append("%d_%s"%(card,"".join(history)))
            state = self.state[len(self.state)-1]
            if state not in self.state_actions_regrets:
                self.state_actions_regrets[state] = []
                for action in info.person_state.available_actions.values():
                    regret = 1.0 / len(info.person_state.available_actions)
                    self.state_actions_regrets[state].append((action, regret))

        else:
            id      = info.person_state.id
            card    = info.person_state.card
            history = info.public_state.action_list


            self.state = ["%d_%s"%(card,"".join(history))]


    def pop_info(self):
        self.state.pop()

    def get_state_actions_probs(self):
        state = self.state[len(self.state)-1]

        if state not in self.state_actions_probs:
            self.state_actions_probs[state] = []
            sum1 = 0
            for action_regret in self.state_actions_regrets[state]:
                sum1 += max(0, action_regret[1])

            if sum1 > 0:
                for action_regret in self.state_actions_regrets[state]:
                    self.state_actions_probs[state].append((action_regret[0], max(0, action_regret[1]) / sum1))
            else:
                for action_regret in self.state_actions_regrets[state]:
                    self.state_actions_probs[state].append(
                        (action_regret[0], 1.0 / len(self.state_actions_regrets[state])))


        return self.state_actions_probs[state]

    def get_state_actions_regrets(self):
        state = self.state[len(self.state)-1]
        return self.state_actions_regrets[state]

    def update_state_actions_regrets(self, origin_actions_regret, target_actions_regret):
        state = self.state[len(self.state)-1]
        self.state_actions_regrets[state] = target_actions_regret

        ##update state_actions_probs
        self.state_actions_probs[state] = []
        sum1 = 0
        for action_regret in self.state_actions_regrets[state]:
            sum1 += max(0, action_regret[1])

        if sum1 > 0:
            for action_regret in self.state_actions_regrets[state]:
                self.state_actions_probs[state].append((action_regret[0], max(0, action_regret[1]) / sum1))
        else:
            for action_regret in self.state_actions_regrets[state]:
                self.state_actions_probs[state].append((action_regret[0], 1.0 / len(self.state_actions_regrets[state])))

    def take_action(self):
        r     = random.random()
        sum1  = 0
        state = self.state[len(self.state)-1]
        for i in xrange(len(self.state_actions_probs[state])):
            sum1 += self.state_actions_probs[state][i][1]
            if sum1 > r:
                return self.state_actions_probs[state][i][0]

        return self.state_actions_probs[state][len(self.state_actions_probs[state]) - 1][0]


    def reset(self):
        pass

if __name__ == "__main__":
    env     = KuhnPokerEnv()
    player  = KuhnPokerCRMPlayer()
    player.is_train = True
    algo    = CRMAlgorithm()
    for i in xrange(10000):
        algo.dfs(env = env, player=player, p0 = 1, p1 = 1, deep = 0)

    print player.state_actions_regrets
    print player.state_actions_probs
    player.is_train = False

    player_random = KuhnPokerRandomPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env,[player, player_random])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores


    player_alwaysbet = KuhnPokerAlwaysBetPlayer()
    sum_scores = [0.0,0.0]
    num        = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env,[player, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num           += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores

    sum_scores = [0.0, 0.0]
    num = 0
    for i in xrange(100000):
        scores = KuhnPokerEnv.compete(env, [player_random, player_alwaysbet])
        sum_scores[0] += scores[0]
        sum_scores[1] += scores[1]
        num += 1
    for i in xrange(len(sum_scores)):
        sum_scores[i] /= num
    print sum_scores
