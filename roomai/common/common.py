#!/bin/python
#coding=utf8

######################################################################### Basic Concepts #####################################################
class AbstractPublicState(object):
    def __init__(self):
        self.turn            = 0
        self.previous_id     = 0
        self.previous_action = None

        self.is_terminal     = False
        self.scores          = []

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is  None:
            newinstance = AbstractPublicState()
        newinstance.turn             = self.turn
        newinstance.previous_id      = self.previous_id
        if self.previous_action is not None:
            newinstance.previous_action  = self.previous_action.__deepcopy__()
        else:
            newinstance.previous_action  = None
        newinstance.is_terminal      = self.is_terminal
        newinstance.scores           = [score for score in self.scores]
        return newinstance


class AbstractPrivateState(object):
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is  None:
            return AbstractPrivateState()
        else:
            return newinstance


class AbsractPersonState(object):
    def __init__(self):
        self.id                = 0
        self.available_actions = dict()
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is  None:
            newinstance = AbsractPersonState()
        newinstance.id                = self.id
        newinstance.available_actions = dict()
        for k in self.available_actions:
            newinstance.available_actions[k] = self.available_actions[k].__deepcopy__()
        return newinstance

class Info(object):
    def __init__(self):
        self.public_state       = AbstractPublicState()
        self.person_state       = AbsractPersonState()
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = Info()
        newinstance.public_state = self.public_state.__deepcopy__()
        newinstance.public_state = self.person_state.__deepcopy__()
        return newinstance

class AbstractAction(object):
    def __init__(self, key):
        self.key = key
    def get_key(self):
        '''
        :return:
            key: action's key , All Actions in RoomAI have a key
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The get_key function hasn't been implemented")
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = AbstractAction()
        newinstance.key = self.key
        return newinstance

class AbstractPlayer(object):
    def receive_info(self, info):
        '''
        :param:
            info: the information produced by a game environments 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        '''
        :return: A Action produced by this player
        '''
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")




class AbstractEnv(object):
    public_state          = AbstractPublicState()
    private_state         = AbstractPrivateState()
    person_states         = [AbstractPrivateState()]

    public_state_history  = []
    private_state_history = []
    person_states_history = []

    def gen_infos(self):
        num_players = len(self.person_states)
        infos = [Info() for i in xrange(num_players)]
        for i in xrange(num_players):
            infos[i].person_state = self.person_states[i].__deepcopy__()
            infos[i].public_state = self.public_state.__deepcopy__()

        return infos

    def gen_history(self):
        self.public_state_history.append(self.public_state.__deepcopy__())
        self.private_state_history.append(self.private_state.__deepcopy__())
        self.person_states_history.append([person_state.__deepcopy__() for person_state in self.person_states])

    def init(self):
        raise ("The init function hasn't been implemented")

    def forward(self, action):
        '''
        :param action: 
        :return: infos, public_state, person_states, private_state
        '''
        raise NotImplementedError("The forward hasn't been implemented")

    def backward(self):
        '''
        The game goes back to the previous states
        :return: infos, public_state, person_states, private_state 
        :ValueError: if Env has reached the initializaiton state, and we call this backward function, we will get ValueError.
        '''

        if len(self.public_state_history) == 1:
            raise ValueError("Env has reached the initialization state and can't go back further. ")
        self.public_state_history.pop()
        self.private_state_history.pop()
        self.person_states_history.pop()

        p = len(self.public_state_history) - 1
        self.public_state  = self.public_state_history[p].__deepcopy__()
        self.private_state = self.private_state_history[p].__deepcopy__()
        self.person_states = [person_state.__deepcopy__() for person_state in self.person_states_history[p]]

        infos  = self.gen_infos()
        return infos, self.public_state, self.person_states, self.private_state


    @classmethod
    def compete(cls, env, players):
        '''
        :param env: 
        :param players: 
        :return: [score_for_player0, score_for_player1,...]
        '''
        raise NotImplementedError("The round function hasn't been implemented")

############################################################### Some Utils ############################################################################

point_str_to_rank  = {'2':0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12, 'r':13, 'R':14}
point_rank_to_str  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A', 13: 'r', 14: 'R'}
suit_str_to_rank   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4}
suit_rank_to_str   = {0:'Spade', 1: 'Heart', 2: 'Diamond', 3:'Club', 4:'ForKing'}


class PokerCard(object):
    def __init__(self, point, suit = None):
        point1 = 0
        suit1  = 0
        if suit is None:
            kv = point.split("_")
            point1 = point_str_to_rank[kv[0]]
            suit1  = suit_str_to_rank[kv[1]]
        else:
            point1 = point
            if isinstance(point, str):
                point1 = point_str_to_rank[point]
            suit1  = suit
            if isinstance(suit, str):
                suit1 = suit_str_to_rank[suit]

        self.point_str = point_rank_to_str[point1]
        self.suit_str  = suit_rank_to_str[suit1]
        self.String = "%s_%s"%(self.point_str, self.suit_str)

    def get_key(self):
        return self.String

    def get_point_rank(self):
        return point_str_to_rank[self.point_str]

    def get_suit_rank(self):
        return suit_str_to_rank[self.suit_str]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        pr1 = pokercard1.get_point_rank()
        pr2 = pokercard2.get_point_rank()

        if pr1 != pr2:
            return pr1 - pr2
        else:
            return pokercard1.get_suit_rank() - pokercard2.get_suit_rank()

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = PokerCard(self.get_key())
        newinstance.point_str = self.point_str
        newinstance.suit_str  = self.suit_str
        newinstance.String    = self.String
        return newinstance