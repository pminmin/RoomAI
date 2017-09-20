#!/bin/python
import roomai.kuhn
import roomai.common
import random
class HumanInputPlayer(roomai.common.AbstractPlayer):
    """
    """
    def receive_info(self, info):
        """

        Args:
            info:
        """
        available_actions = info
    def take_action(self):
        """

        Returns:

        """
        action = raw_input("choosed_acton:")
        #action = ""
        return roomai.kuhn.KuhnPokerAction.lookup(action)
    def reset(self):
        """

        """
        pass


def show_person(person_state):
    print ("%s"%(person_state.id) + "'s card:%d"%(person_state.card))
    print ("%s"%(person_state.id) + "'s available_actions:\t" + " ".join(person_state.available_actions.keys()))

def show_public(public_state):
    print ("turn:%d"%public_state.turn)

if __name__ == "__main__":
    
    import crm_kuhn
    crm_player = crm_kuhn.KuhnPokerCRMPlayer()
    import algorithms
    algo       = algorithms.CRMAlgorithm()
    env        = roomai.kuhn.KuhnPokerEnv()
    for i in range(10000):
        algo.dfs(env = env, player=crm_player, p0 = 1, p1 = 1, deep = 0)

    print crm_player.regrets
    print crm_player.strategies
    crm_player.is_train = False
    
    players     = [HumanInputPlayer(), crm_player]


    num_players = len(players)
    infos, public_state, person_states, private_state = env.init({"num_players":2,"record_history":False})
    for i in range(num_players):
        players[i].receive_info(infos[i])
        show_person(infos[i].person_state)
    show_public(public_state)
    print ("\n")


    while public_state.is_terminal == False:
        turn = public_state.turn
        action = players[turn].take_action()
        print "%d player take an action (%s)"%(turn,action.key)
        infos, public_state, person_states, private_state = env.forward(action)
        for i in range(num_players):
            players[i].receive_info(infos[i])
            show_person(infos[i].person_state)
        show_public(public_state)
        print ("\n")

    print (public_state.scores)
