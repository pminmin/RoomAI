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
        self.person_state       = None

class AbstractAction:
    def toString(self):
        '''
        :return:
            key: action's key 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented")

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