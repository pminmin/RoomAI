#!/bin/python
#coding=utf8

import sys
sys.path.append("DouDiZhuPoker")

import KuhnPokerEnv
#import RockPaperScissorsEnv
import DouDiZhuPokerEnv

import KuhnPokerPlayer
#import RockPaperScissorsPlayer
import DouDiZhuPokerPlayer

#####################################################
                # environment list #
#####################################################
def createEnv(name):

    if name == "DouDiZhuPokerEnv":
        return DouDiZhuPokerEnv.DouDiZhuPokerEnv()
    elif name == "KuhnPokerEnv":
        return KuhnPokerEnv.KuhnPokerEnv()
    #elif name == "RockPaperScissorsEnv":
    #    return RockPaperScissorsEnv.RockPaperScissorsEnv()
    else: 
        raise KeyError("%s isn't a ChessEnvironment name"%(name))



#####################################################
                 # players list #
#####################################################
def createPlayer(name):

    if name == "DouDiZhuPokerMaxPlayer":
        return DouDiZhuPokerPlayer.DouDiZhuPokerMaxPlayer();

    elif name == "KuhnPokerCounterfactualRegretPlayer":
        return KuhnPokerPlayer.KuhnPokerCounterfactualRegretPlayer();
    elif name =="KuhnPokerAlwaysBetPlayer":
        return KuhnPokerPlayer.KuhnPokerAlwaysBetPlayer();

    #elif name == "RockPaperScissorsAlwaysRockPlayer":
    #    return RockPaperScissorsPlayer.RockPaperScissorsAlwaysRockPlayer();
    #elif name == "RockPaperScissorsRandomPlayer":
    #    return RockPaperScissorsPlayer.RockPaperScissorsRandomPlayer();
    #elif name == "RockPaperScissorsRegretMatchPlayer":
    #    return RockPaperScissorsPlayer.RockPaperScissorsRegretMatchPlayer();

    else:
        raise KeyError("%s isn't a ChessPlayer name"%(name))

 
## is it easy to get you attentions
