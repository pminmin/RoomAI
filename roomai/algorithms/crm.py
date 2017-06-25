#!/bin/python
import roomai.common
import random
import copy

class CRMPlayer(roomai.common.AbstractPlayer):
    def get_state_actions_regrets(self, state):
        raise NotImplementedError("get_counterfactual_values hasn't been implemented")
    def update_state_actions_regrets(self, state, origin_actions_regret, target_actions_regret):
        raise NotImplementedError("update_counterfactual_values hasn't been implemented")

    def get_state_actions_probs(self):
        raise NotImplementedError("get_action_probs hasn't been implemented")

    def pop_info(self):
        raise NotImplementedError("The pop_info function hasn't been implemented")


class CRMAlgorithm:

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
            turn           = public_state.turn
            #print turn, infos[turn].public_state.action_list, infos[turn].person_state.id

            player.receive_info(infos[turn])

            actions_regrets = player.get_state_actions_regrets()
            actions_probs   = player.get_state_actions_probs()

            new_actions_regret = [None for i in xrange(len(actions_regrets))]
            for i in xrange(len(actions_probs)):
                action                       = actions_probs[i][0]
                new_players_probs            = [v for v in players_probs]
                new_players_probs[turn]     *= actions_probs[i][1]
                new_actions_regret[i]        = -1 * self.dfs(env, player, new_players_probs, action, deep + 1)
            sum1 = 0
            for i in xrange(len(new_actions_regret)):
                sum1 += actions_probs[i][1] * new_actions_regret[i]
            ##print new_actions_regret, actions_probs, sum1
            for i in xrange(len(new_actions_regret)):
                new_actions_regret[i] = (actions_regrets[i][0],new_actions_regret[i] - sum1)

            player.update_state_actions_regrets(actions_regrets, new_actions_regret)
            player.pop_info()
            result = sum1

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





