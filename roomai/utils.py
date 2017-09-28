#!/bin/python
import roomai
import os

def version():
    '''
    
    :return: The version of RoomAI 
    '''
    version = "0.1.1"
    print ("roomai-%s"%version)
    return ("roomai-%s"%version)


class FrozenDict(dict):
    def __setitem__(self, key, value):
        raise NotImplementedError("The FrozenDict doesn't support the __setitem__ function")