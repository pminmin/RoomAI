#!/bin/python
import sys
sys.path.append(".")
sys.stdout.flush()
from roomai.doudizhu import *

print "start"
sys.stdout.flush()

actions_file            = open("actions.txt","w")
handcards2actions_file  = open("handcards2actions.txt","w")
AllActionsDict          = dict()

def extractStraight(hand_cards, numStraightK, count, exclude):
    cardss = []
    count = 0

    if numStraightK == 0:
        return cardss

    for i in xrange(12,-1,-1): 
        sys.stdout.flush()
        if i not in exclude:
            count  = 0 
        elif hand_cards[i] >= count:
            count += 1
        else:
            count  = 0        

        if count >= numStraightK:
            cardss.append(hand_cards[i:i+numStraightK])


    return cardss          

    
def extractDiscrete(hand_cards, numDiscreteV, count, exclude):
    cardss  = []
    
    if numDiscreteV == 0:
        return cardss

    for c in xrange(len(hand_cards)):
        old_cardss = copy.deepcopy(cardss)
        if (hand_cards[c] >= count) and (c not in exclude):
            for origin in old_cardss:
                if len(origin) == numDiscreteV:  continue
                copy1 = copy.deepcopy(origin)
                copy1.append(c)
                cardss.append(copy1)        
            cardss.append([c])
    
    return copy.deepcopy(cardss)


def gen_actions(hand_cards, pattern):
    sys.stdout.flush()
    if "i_" in pattern[0]:
         return []    

    actions = [];
    if pattern[0] == "x_rocket":
         if  hand_cards[ActionSpace.r] == 1 and \
             hand_cards[ActionSpace.R] == 1:
            action = Action([ActionSpace.r, ActionSpace.R],[])
            actions.append(action)
         return actions       

    numMaster   = pattern[1]
    numMasterV  = pattern[2]
    isStraight  = pattern[3]
    numSlave    = pattern[4]
    numSlaveV   = pattern[5]
     
    numMasterCount  = -1
    numSlaveCount   = -1
    if numMasterV > 0:
        numMasterCount  = numMaster/numMasterV
    if numSlaveV  > 0:
        numSlaveCount   = numSlave /numSlaveV

    mCardss = []
    if isStraight == 1:
        sys.stdout.flush()
        mCardss = extractStraight(hand_cards, numMasterV, numMasterCount, [])
    else:
        mCardss = extractDiscrete(hand_cards, numMasterV, numMasterCount, [])

    for mCards in mCardss:
        m = []
        for mc in mCards:
            m.extend([mc for i in xrange(numMasterCount)])
        m.sort()
      
        if  numSlaveV == 0:
            actions.append(Action(copy.deepcopy(m), []))
            continue

        sCardss = extractDiscrete(hand_cards, numSlaveV, numSlaveCount, mCards)
        if len(sCardss) > 0:
            for sCards in sCardss:
                s = []
                for sc in sCards:
                    s.extend([sc for i in xrange(numSlaveCount)])
                s.sort()
                actions.append(Action(copy.deepcopy(m), s))
        

    return actions


def gen_handcards_dfs(hand_cards, currentP, currentNum, numList):
    sys.stdout.flush()
    if currentNum > numList or currentP > 15:
        return

    hand_cards_str = ""
    for i in hand_cards:
        hand_cards_str += "%d,"%(i)

    if currentNum < numList and currentP < 15:
        range1 = 5
        if currentP == 13 or currentP == 14:
            range1 = 2
        for i in xrange(range1):
            hand_cards[currentP] = i
            gen_handcards_dfs(hand_cards, currentP+1, currentNum + i, numList)
            hand_cards[currentP] = 0

    sys.stdout.flush()
    idxStr = ""
    for p in AllPatterns: 

            actions = gen_actions(hand_cards, AllPatterns[p])
            for act in actions:
                act.masterCards.sort()
                act.slaveCards.sort()

                mStr = ""
                for c in act.masterCards:
                    mStr += "%d,"%c
                sStr = ""
                for c in act.slaveCards:
                    sStr += "%d,"%c
                actionStr = mStr + "\t" + sStr
                

                if actionStr not in AllActionsDict:  
                    AllActionsDict[actionStr] = len(AllActionsDict)
                    actions_file.write("%s\t%d\n"%(actionStr, AllActionsDict[actionStr]))
                    actions_file.flush()

                idx = AllActionsDict[actionStr]
                idxStr += "%d,"%idx
        
    if len(idxStr) > 0: 
        handcards2actions_file.write("%s\t%s\n"%(hand_cards_str, idxStr))

gen_handcards_dfs([0 for i in xrange(15)], 0, 0, 20)
actions_file.close()
handcards2actions_file.close()
print "end"
