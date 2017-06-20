#!/bin/python
import roomai.abstract
class CRMPlayer(roomai.abstract.AbstractPlayer):
    def get_counterfactual_values(self):
        raise NotImplementedError("get_counterfactual_values hasn't been implemented")
    def update_counterfactual_values(self, origin_counterfactual_values, target_counterfactual_values):
        raise NotImplementedError("update_counterfactual_values hasn't been implemented")
    def get_actions_probs(self):
        raise NotImplementedError("get_action_probs hasn't been implemented")
    def save_model(self,address):
        raise NotImplementedError("save_model hasn't been implemented")
    def load_model(self, address):
        raise NotImplementedError("load_model hasn't been implemented")


class CRMAlgorithm:

    def dfs(self, env, players, deep = 0):
        if deep == 0:
            env.init()

        elif env.public_state.is_terminal == True: ##terminal
            scores = env.public_state.scores

        else:
            turn = env.public_state.turn
            

