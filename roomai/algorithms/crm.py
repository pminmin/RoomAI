#!/bin/python
import roomai.abstract
import random

class CRMPlayer(roomai.abstract.AbstractPlayer):
    def get_actions_regret(self):
        raise NotImplementedError("get_counterfactual_values hasn't been implemented")
    def update_actions_regret(self, origin_actions_regret, target_actions_regret):
        raise NotImplementedError("update_counterfactual_values hasn't been implemented")

    def get_actions_prob(self):
        raise NotImplementedError("get_action_probs hasn't been implemented")


class CRMAlgorithm:

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
            env.backforward()
            return result

        else:
            for i in xrange(len(infos)):
                players.receive_info(infos[i])

            turn           = public_state.turn
            actions_regret = players[turn].get_actions_regret()
            actions_prob   = players[turn].get_actions_prob()

            new_actions_regret = [None for i in xrange(len(actions_regret))]
            for i in xrange(len(actions_prob)):
                action                       = actions_prob[i][0]
                new_players_prob             = [v for v in players_prob]
                new_players_prob[turn]      *= actions_prob[i][1]
                new_actions_regret[i]        = -1 * self.dfs(env, players, new_players_prob, action, deep + 1)
            sum1 = 0
            for i in xrange(len(new_actions_regret)):
                sum1 += actions_prob[i][1] * actions_regret[i][1]
            for i in xrange(len(new_actions_regret)):
                new_actions_regret -= sum1

            players[turn].update_actions_regret(actions_regret, new_actions_regret)

            env.backforward()
            return sum1



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
            env.backforward()
            return result

        else:
            for i in xrange(len(infos)):
                players.receive_info(infos[i])

            turn           = public_state.turn
            actions_regret = players[turn].get_actions_regret()
            actions_prob   = players[turn].get_actions_prob()

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
            players[turn].update_actions_regret(actions_regret, new_actions_regret)

            env.backforward()
            return sum1





