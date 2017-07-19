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


class AbstractPersonState(object):
    def __init__(self):
        self.id                = 0
        self.available_actions = dict()
    def __deepcopy__(self, memodict={}, newinstance = None):
        #print "enter AbstractPersonState __deepcopy__"
        if newinstance is  None:
            newinstance = AbstractPersonState()
        newinstance.id                = self.id
        newinstance.available_actions = dict()
        for k in self.available_actions:
            #print "fuck"
            newinstance.available_actions[k] = self.available_actions[k].__deepcopy__()
        return newinstance

class Info(object):
    def __init__(self):
        self.public_state       = AbstractPublicState()
        self.person_state       = AbstractPersonState()
    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = Info()
        newinstance.public_state = self.public_state.__deepcopy__()
        newinstance.public_state = self.person_state.__deepcopy__()
        return newinstance

class AbstractAction(object):
    def __init__(self, key):
        self.__key = key

    @property
    def key(self):
        return self.__key

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AbstractAction()
        newinstance.__key = self.__key
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

    def __gen_infos__(self):
        num_players = len(self.person_states)
        infos = [Info() for i in xrange(num_players)]
        for i in xrange(num_players):
            infos[i].person_state = self.person_states[i].__deepcopy__()
            infos[i].public_state = self.public_state.__deepcopy__()

        return infos

    def __gen_history__(self):
        self.public_state_history.append(self.public_state.__deepcopy__())
        self.private_state_history.append(self.private_state.__deepcopy__())
        self.person_states_history.append([person_state.__deepcopy__() for person_state in self.person_states])

    def init(self, chance_action = None, is_gen_chances = None):
        '''
        :param chance_action: 
        :return: infos, public_state, person_states, private_state, other_chance_actions
        '''
        raise ("The init function hasn't been implemented")

    def forward(self, action, chance_action = None, is_gen_chances = None):
        '''
        :param action, chance_action
        :return: infos, public_state, person_states, private_state, other_chance_actions
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

        infos  = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    ### provide some util functions
    @classmethod
    def compete(cls, env, players):
        '''
        :param env: 
        :param players: 
        :return: [score_for_player0, score_for_player1,...]
        '''
        raise NotImplementedError("The round function hasn't been implemented")

    @classmethod
    def is_action_valid(cls, action, public_state, person_state):
        '''
        :param public_state: 
        :param person_state: 
        :return: is  the action valid
        '''
        raise  NotImplementedError("The is_action_valid function hasn't been implemented")

    def available_actions(self, public_state, person_state):
        '''
        :param public_state: 
        :param person_state: 
        :return: all available_actions
        '''
        raise NotImplementedError("The available_actions function hasn't been implemented")

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

        self.__point_str = point_rank_to_str[point1]
        self.__suit_str  = suit_rank_to_str[suit1]
        self.__key = "%s_%s" % (self.point_str, self.suit_str)

    @property
    def point_str(self):
        return self.__point_str

    @property
    def suit_str(self):
        return self.__suit_str

    @property
    def key(self):
        return self.__key

    @classmethod
    def lookup(cls, key):
        return AllPokerCards[key]

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

    def __deepcopy__(self,  memodict={}, newinstance = None):
        if newinstance is None:
            newinstance = AllPokerCards[self.key]
        return newinstance

AllPokerCards = dict()
for point_str in point_str_to_rank:
    if point_str != 'r' and point_str != "R":
        for suit_str in suit_str_to_rank:
            if suit_str != "ForKing":
                AllPokerCards["%s_%s"%(point_str,suit_str)] = PokerCard("%s_%s"%(point_str,suit_str))
AllPokerCards["r_ForKing"] = (PokerCard("r_ForKing"))
AllPokerCards["R_ForKing"] = (PokerCard("R_ForKing"))