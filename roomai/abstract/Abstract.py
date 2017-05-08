#!/bin/python
#coding=utf8

class AbstractPublicState:
    pass

class AbstractPrivateState:
    pass

class AbsractPersonState:
    id                = None
    available_actions = None

class AbstractInfo:
    def __init__(self):
        self.public_state       = None
        self.private_state      = None
        self.person_state       = None
'''
The info is the information sent by env to player, which is 
consisted of private_state、 public_state and person_state.

Three properties of info

1.1 If there are n players, env.forward will return n+1 infos. 
The i-th info is w.r.t the i-th player except the last info. 
The last info is designed for recording private_state, and 
only the last info contains non-None private_state. Hence, no 
player will get private_state

1.2 All infos contain the public_state.

1.3 All infos contain the person_state. For different players,
the person state is different. Only the person_state in the 
info w.r.t the player who will take a action, contains non-None
available_actions dict. non-None available_actions dict is with (action_key, action)
'''

class AbstractAction:
    def toString(self):
        '''
        :return:
            key: action's key 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented")

'''
The toString function generate its key.
'''

class AbstractPlayer:

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


class AbstractEnv:

    def init(self):
        raise NotImplementedError("The init function hasn't been implemented")

    def forward(self, action):
        raise NotImplementedError("The receiveAction hasn't been implemented")

    @classmethod
    def compete(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")