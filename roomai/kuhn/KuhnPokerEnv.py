#!/bin/python
import random
import math
import copy
import roomai.kuhn.KuhnPokerUtils
import roomai.common
logger = roomai.get_logger()

class KuhnPokerEnv(roomai.common.AbstractEnv):
    '''
    The KuhnPoker game environment
    '''


    #@override
    def init(self, params=dict()):
        '''
        Initialize the KuhnPoker game environment
        
        :param params: the initialization params
        :return: infos, public_state, person_states, private_state 
        '''
        self.__params__ = dict()

        if "record_history" in params:
            self.__params__["record_history"] = params["record_history"]
        else:
            self.__params__["record_history"] = False

        if "start_turn" in params:
            self.__params__["start_turn"] = params["start_turn"]
        else:
            self.__params__["start_turn"] = int(random.random() * 2)

        self.__params__["num_players"] = 2

        if "num_players" in params:
            logger.warning("KuhnPoker is a game of two players and the number of players always be 2. Ingores the \"num_players\" option")


        self.available_action = dict()
        self.available_action[roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("check").key] = roomai.kuhn.KuhnPokerAction.lookup("check")
        self.available_action[roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("bet").key]   = roomai.kuhn.KuhnPokerAction.lookup("bet")

        self.private_state = roomai.kuhn.KuhnPokerUtils.KuhnPokerPrivateState()
        self.public_state  = roomai.kuhn.KuhnPokerUtils.KuhnPokerPublicState()
        self.person_states = [roomai.kuhn.KuhnPokerUtils.KuhnPokerPersonState() for i in range(2)]


        card0 = math.floor(random.random() * 3)
        card1 = math.floor(random.random() * 3)
        while card0 == card1:
            card0 = math.floor(random.random() * 3)


        self.public_state.__turn__          = self.__params__["start_turn"]
        self.public_state.__first__         = self.public_state.turn
        self.public_state.__epoch__         = 0
        self.public_state.__action_list__   = []
        self.public_state.__is_terminal__   = False
        self.public_state.__scores__        = None
        self.person_states[0].__id__          = 0
        self.person_states[0].__number__      = card0
        self.person_states[1].__id__          = 1
        self.person_states[1].__number__      = card1

        self.person_states[self.public_state.turn].__available_actions__ = self.available_action

        self.__gen_history__()
        infos = self.__gen_infos__()

        
        return  infos, self.public_state, self.person_states, self.private_state

    #@override
    def forward(self, action):
        """
        The KuhnPoker game environment steps with the action taken by the current player

        :param action
        :returns:infos, public_state, person_states, private_state
        """

        self.person_states[self.public_state.turn].__available_actions__ = dict()
        self.public_state.__epoch__                                     += 1
        self.public_state.__turn__                                       = (self.public_state.turn+1)%2
        self.public_state.__action_list__.append(action.key)

        if self.public_state.epoch == 1:
            self.public_state.__is_terminal__ = False
            self.public_state.__scores__      = []
            self.person_states[self.public_state.turn].__available_actions__ = self.available_action

            self.__gen_history__()
            infos = self.__gen_infos__()
            return infos, self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 2:
            scores = self.__evalute_two_round__()
            if scores is not None:
                self.public_state.__is_terminal__ = True
                self.public_state.__scores__      = scores

                self.__gen_history__()
                infos = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state
            else:
                self.public_state.is_terminal = False
                self.public_state.scores      = []
                self.person_states[self.public_state.turn].available_actions = self.available_action

                self.__gen_history__()
                infos                         = self.__gen_infos__()
                return infos,self.public_state, self.person_states, self.private_state

        elif self.public_state.epoch == 3:
            self.public_state.is_terminal = True
            self.public_state.scores      = self.__evalute_three_round__()

            self.__gen_history__()
            infos                         = self.__gen_infos__()
            return infos,self.public_state, self.person_states, self.private_state

        else:
            raise Exception("KuhnPoker has 3 turns at most")


    #@Overide
    @classmethod
    def compete(cls, env, players):
        '''
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: scores for the players
        '''

        infos, public_state, person_state, private_state = env.init()
        for i in range(len(players)):
            players[i].receive_info(infos[i])

        while public_state.is_terminal == False:
            turn = infos[-1].public_state.turn
            action = players[turn].take_action()
            infos,public_state, person_state, private_state = env.forward(action)
            for i in range(len(players)):
                players[i].receive_info(infos[i])

        return public_state.scores



    def __higher_number_player__(self):
        if self.person_states[0].number > self.person_states[1].number:
            return 0
        else:
            return 1

    def __evalute_two_round__(self):
        win    = self.__higher_number_player__()
        first  = self.public_state.first
        scores = [0, 0];
        actions = self.public_state.action_list

        if actions[0] == "check" and \
           actions[1] == "bet":
            return None
        
        if actions[0] == actions[1] and \
           actions[0] == "check":
            scores[win]   = 1;
            scores[1-win] = -1
            return scores;

        if actions[0] == "bet" and \
           actions[1] == "check":
            scores[first]   = 1;
            scores[1-first] = -1
            return scores;

        if actions[0] == actions[1] and \
           actions[0] == "bet":
            scores[win]   = 2
            scores[1-win] = -2
            return scores;


    def __evalute_three_round__(self):
        first   = self.public_state.first 
        win     = self.__higher_number_player__()
        scores  = [0, 0]

        if self.public_state.action_list[2] == "check":
            scores[1 - first] = 1;
            scores[first]     = -1
        else:
            scores[win]   = 2;
            scores[1-win] = -2
        return scores;
       
