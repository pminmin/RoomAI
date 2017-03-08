#!/bin/python
import sys
sys.path.append("..")
from DouDiZhuPokerUtils import *

actions_file            = open("actions.txt","w")
handcards2actions_file  = open("handcards2actions.txt","w")

AllActionsDict = dict()

def gen_actions(hand_cards):
    

def gen_handcards_dfs(hand_cards, currentP, currentNum, numList):

    hand_cards_str = ""
    for i in hand_cards:
        hand_cards_str += "%d,"%(i)

    if currentNum > numList:
        pass

    elif currentNum == numList or currentP == 15:
        actions = gen_actions(hand_cards)
        for act in actions:
            act.masterCards.sort()
            act.slaveCards.sort()
            if act not in AllActionsDict:   
                idx = len(AllActionsDict)
                AllActionsDict[act] = idx
                
                mStr = ""
                for c in act.masterCards:
                    mStr += "%d,"%c
                sStr = ""
                for c in act.slaveCards:
                    sStr += "%d,"%c

                actions_file.write("%s\t%s"%(mStr,sStr))
                handcards2actions_file.write("%s\t%d"%(hand_cards_str,idx))

            else:
                idx = AllActionsDict[act]
                handcards2actions_file.write("%s\t%s"%(hand_cards_str,idx))
                

    else:
        range1 = 5
        if currentP == 13 or currentP == 14:
            range1 = 2
        for i in xrange(range1):
            hand_cards[currentP] = i
            gen_handcards_dfs(hand_cards, currentP+1, currentNum + i, numList)
            hand_cards[currentP] = 0


gen_handcards_dfs([0 for i in xrange(15)], 0, 0, 20)
actions_file.close()
handcards2actions_file.close()

