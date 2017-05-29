#!/bin/python
#coding:utf-8
import random
import roomai.abstract
import roomai.kuhn.KuhnPokerUtils

class KuhnPokerAlwaysBetPlayer(roomai.abstract.AbstractPlayer):
    def __init__(self):
        pass
           
    def receive_info(self, info):
        pass     

    def take_action(self):
        return roomai.kuhn.KuhnPokerUtils.KuhnPokerAction("bet")

    def reset(self):
        pass
