#!/bin/python
import roomai.common
import random
import copy

class CRMPlayer(roomai.common.AbstractPlayer):
    def gen_state(self,info):
        raise NotImplementedError("")
    def update_strategies(self, state, actions, targets):
        raise NotImplementedError("")
    def get_strategies(self, state, actions):
        raise NotImplementedError("")
    def update_regrets(self, state, actions, targets):
        raise NotImplementedError("")
    def get_regrets(self, state, actions):
        raise NotImplementedError("")


class CRMAlgorithm:
    regrets = dict()

    def dfs(self, env, player, players_probs, action = None, deep = 0):
        infos         = None
        public_state  = None
        person_states = None
        private_state = None


        if deep == 0:
            infos, public_state, person_states, private_state = env.init()
        else:
            infos, public_state, person_states, private_state = env.forward(action)

        if public_state.is_terminal == True:
            turn   = public_state.turn
            scores = public_state.scores
            result = scores[turn]

        else:

            turn                  = public_state.turn
            state                 = player.gen_state(infos[turn])
            available_actions     = infos[turn].person_state.available_actions.values()
            num_available_actions = len(available_actions)
            cur_regrets           = player.get_regrets(state, available_actions)
            cur_strategy          = [0 for i in xrange(num_available_actions)]
            


            counterfactual_h_a    = [0 for i in xrange(num_available_actions)]
            counterfactual_h      = 0

            for i in xrange(num_available_actions):
                counterfactual_h_a[i] = -1 * self.dfs(env, player, players_probs,action,deep+1)
                counterfactual_h     += cur_strategy[i] * counterfactual_h_a[i]

            new_regrets    = [0 for i in xrange(num_available_actions)]
            new_strategies = [0 for i in xrange(num_available_actions)]
            for i in xrange(num_available_actions):
                new_regrets


            player.update_regrets(state, available_actions, new_regrets)
            player.update_strategies(state, available_actions, new_strategies)

            result = counterfactual_h

        if deep != 0:
            env.backward()
        return result



class FastCRMAlgorithm:


    def dfs(self, env, players, players_prob, action = None, deep = 0):
        infos         = None
        public_state  = None
        person_states = None
        private_state = None

        if deep == 0:
            infos, public_state, person_states, private_state = env.init()
        else:
            infos, public_state, person_states, private_state = env.forward(action)

        if public_state.is_terminal == True:
            turn   = public_state.turn
            scores = public_state.scores
            result = scores[turn]

        else:
            for i in xrange(len(infos)):
                players.receive_info(infos[i])

            turn           = public_state.turn
            actions_regret = players[turn].get_state_actions_regrets()
            actions_prob   = players[turn].get_state_actions_probs()

            new_actions_regret           = [r for r in actions_prob]
            action                       = players[turn].take_action()
            new_players_prob             = [v for v in players_prob]
            new_players_prob[turn]      *= actions_prob[i][1]
            new_actions_regret[i]        = -1 * self.dfs(env, players, new_players_prob, action, deep + 1)

            sum1 = 0
            for i in xrange(len(new_actions_regret)):
                sum1 += actions_prob[i][1] * actions_regret[i][1]
            for i in xrange(len(new_actions_regret)):
                new_actions_regret -= sum1
            players[turn].update_state_actions_regrets(actions_regret, new_actions_regret)

        if deep != 0:
            env.backward()
        return result





