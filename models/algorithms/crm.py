#!/bin/python
import roomai.abstract
class CRMPlayer(roomai.abstract.AbstractPlayer):
    def get_counterfactual_values(self):
        raise NotImplementedError("get_counterfactual_values hasn't been implemented")
    def update_counterfactual_values(self, origin_counterfactual_values, target_counterfactual_values):
        raise NotImplementedError("update_counterfactual_values hasn't been implemented")
    def get_actions_probs(self):
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
            env.backforward()
            return 0

        else:
            for i in xrange(len(infos)):
                players.receive_info(infos[i])

            turn = public_state.turn
            counterfactual_values = players[turn].get_counterfactual_values()
            actions_probs = players[turn].get_actions_probs()

            new_counterfactual_values = [None for i in xrange(len(counterfactual_values))]
            for i in xrange(len(actions_probs)):
                action = actions_probs[i][0]
                players_prob[turn] *= actions_probs[i][1]
                val = self.dfs(env, players, players_prob, action, deep + 1)
                new_counterfactual_values[i] = (actions_probs[0], val)
            players[turn].update_counterfactual_values(counterfactual_values, new_counterfactual_values)

            env.backforward()
            sum1 = 0
            for action_value in new_counterfactual_values:
                sum1 += action_value[1]
            return sum1


class FastCRMAlgorithm:
    def choose_action(self,action_probs):

    def dfs(self, env, players, action=None, deep=0):
        if deep == 0:
            infos, public_state, person_states, private_state = env.init()
            if public_state.is_terminal == True:
                env.backforward()
                return 0

            for i in xrange(len(infos)):
                players.receive_info(infos[i])

            turn = public_state.turn
            counterfactual_values = players[turn].get_counterfactual_values()
            actions_probs = players[turn].get_actions_probs()



        else:
            infos, public_state, person_states, private_state = env.forward(action)
            if public_state.is_terminal == True:
                env.backforward()

            else:
                env.backforward()



            

