#!/bin/python
import os
import roomai.common
import copy


#
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11, 12, 13, 14
#^                ^   ^              ^       ^
#|                |   |              |       |
#3,               10, J, Q,  K,  A,  2,  r,  R
#

class DouDiZhuActionElement:
    str_to_rank  = {'3':0, '4':1, '5':2, '6':3, '7':4, '8':5, '9':6, 'T':7, 'J':8, 'Q':9, 'K':10, 'A':11, '2':12, 'r':13, 'R':14, 'x':15, 'b':16}
    # x means check, b means bid
    rank_to_str  = {0: '3', 1: '4', 2: '5', 3: '6', 4: '7', 5: '8', 6: '9', 7: 'T', 8: 'J', 9: 'Q', 10: 'K', 11: 'A', 12: '2', 13: 'r', 14: 'R', 15: 'x', 16: 'b'}
    three       = 0;
    four        = 1;
    five        = 2;
    six         = 3;
    seven       = 4;
    eight       = 5;
    night       = 6;
    ten         = 7;
    J           = 8;
    Q           = 9;
    K           = 10;
    A           = 11;
    two         = 12;
    r           = 13;
    R           = 14;
    cheat       = 15;
    bid         = 16;

    total_normal_cards = 15



class DouDiZhuAction(roomai.common.AbstractAction):
    def __init__(self, masterCards, slaveCards):
        self.__masterCards        = copy.deepcopy(masterCards)
        self.__slaveCards         = copy.deepcopy(slaveCards)

        self.__masterPoints2Count = None
        self.__slavePoints2Count  = None
        self.__isMasterStraight   = None
        self.__maxMasterPoint     = None
        self.__minMasterPoint     = None
        self.__pattern            = None
        DouDiZhuAction.action2pattern(self)
        self.__key = DouDiZhuPokerEnv.master_slave_cards_to_key(masterCards, slaveCards)

    @property
    def key(self):  return self.__key
    @property
    def masterCards(self):  return self.__masterCards
    @property
    def slaveCards(self):   return self.__slaveCards
    @property
    def masterPoints2Count(self):   return self.__masterPoints2Count
    @property
    def slavePoints2Count(self):    return self.__slavePoints2Count
    @property
    def isMasterStraight(self):     return self.__isMasterStraight
    @property
    def maxMasterPoint(self):       return self.__maxMasterPoint
    @property
    def minMasterPoint(self):       return self.__minMasterPoint
    @property
    def pattern(self):              return self.__pattern

    @classmethod
    def lookup(cls, key):
        return AllActions[key]

    @classmethod
    def master_slave_cards_to_key(cls, masterCards, slaveCards):
        key_int = (masterCards + slaveCards)
        key_str = []
        for key in key_int:
            key_str.append(DouDiZhuActionElement.rank_to_str[key])
        key_str.sort()
        return "".join(key_str)

    @classmethod
    def action2pattern(cls, action):

        action.masterPoints2Count = dict()
        for c in action.masterCards:
            if c in action.masterPoints2Count:
                action.masterPoints2Count[c] += 1
            else:
                action.masterPoints2Count[c] = 1

        action.slavePoints2Count = dict()
        for c in action.slaveCards:
            if c in action.slavePoints2Count:
                action.slavePoints2Count[c] += 1
            else:
                action.slavePoints2Count[c] = 1

        action.isMasterStraight = 0
        num = 0
        for v in action.masterPoints2Count:
            if (v + 1) in action.masterPoints2Count and (v + 1) < DouDiZhuActionElement.two:
                num += 1
        if num == len(action.masterPoints2Count) - 1 and len(action.masterPoints2Count) != 1:
            action.isMasterStraight = 1

        action.maxMasterPoint = -1
        action.minMasterPoint = 100
        for c in action.masterPoints2Count:
            if action.maxMasterPoint < c:
                action.maxMasterPoint = c
            if action.minMasterPoint > c:
                action.minMasterPoint = c

        ########################
        ## action 2 pattern ####
        ########################


        # is cheat?
        if len(action.masterCards) == 1 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] == DouDiZhuActionElement.cheat:
            action.pattern = AllPatterns["i_cheat"]

        # is roblord
        elif len(action.masterCards) == 1 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] == DouDiZhuActionElement.bid:
            action.pattern = AllPatterns["i_bid"]

        # is twoKings
        elif len(action.masterCards) == 2 \
                and len(action.masterPoints2Count) == 2 \
                and len(action.slaveCards) == 0 \
                and action.masterCards[0] in [DouDiZhuActionElement.r, DouDiZhuActionElement.R] \
                and action.masterCards[1] in [DouDiZhuActionElement.r, DouDiZhuActionElement.R]:
            action.pattern = AllPatterns["x_rocket"]

        else:

            ## process masterCards
            masterPoints = action.masterPoints2Count
            if len(masterPoints) > 0:
                count = masterPoints[action.masterCards[0]]
                for c in masterPoints:
                    if masterPoints[c] != count:
                        action.pattern = AllPatterns["i_invalid"]

            if action.pattern == None:
                pattern = "p_%d_%d_%d_%d_%d" % (len(action.masterCards), len(masterPoints), \
                                                action.isMasterStraight, \
                                                len(action.slaveCards), 0)

                if pattern in AllPatterns:
                    action.pattern = AllPatterns[pattern]
                else:
                    action.pattern = AllPatterns["i_invalid"]

        return action



############## read data ################
AllPatterns = dict()
AllActions = dict()
import zipfile
def get_file(path):
    if ".zip" in path:
        lines = path.split(".zip")
        zip1 = zipfile.ZipFile(lines[0] + ".zip")
        len1 = len(lines[1])
        path = lines[1][1:len1]
        return zip1.open(path)
    else:
        return open(path)
path = os.path.split(os.path.realpath(__file__))[0]
pattern_file = get_file(path + "/patterns.py")
for line in pattern_file:
    line = line.replace(" ", "").strip()
    line = line.split("#")[0]
    if len(line) == 0:  continue
    lines = line.split(",")
    for i in range(1, len(lines)):
        lines[i] = int(lines[i])
    AllPatterns[lines[0]] = lines
pattern_file.close()

action_file = get_file(path + "/actions.py")
for line in action_file:
    line = line.replace(" ", "").strip()
    lines = line.split("\t")

    m = []
    ms = lines[0].split(",")
    for c in ms:
        if c != "":
            m.append(int(c))

    s = []
    ss = []
    if len(lines) == 2:
        ss = lines[1].split(",")
    for c in ss:
        if c != "":
            s.append(int(c))
    action = DouDiZhuAction(m, s)
    AllActions[action.key] = action
action_file.close()