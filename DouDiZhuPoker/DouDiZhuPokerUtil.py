#!/bin/python
#coding:utf-8


#
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11, 12, 13, 14
#^                ^   ^              ^       ^
#|                |   |              |       |
#3,               10, J, Q,  K,  A,  2,  r,  R
#


class PrivateState:
    def __init__(self):
        self.hand_cards         = [[],[],[]]
        self.num_hand_cards     = [-1,-1,-1]
        self.additive_cards     = []

class PublicState:

    def __init__(self):

        self.landlord_candidate_id  = -1
        self.landlord_id            = -1
        self.license_id             = -1
        self.license_action         = None

        self.first_player           = -1
        self.turn                   = -1
        self.phase                  = -1
        self.epoch                  = -1

        self.previous_id            = -1
        self.previous_action        = None


class Info:
    def __init__(self):
        ### init
        self.init_id            = -1
        self.init_cards         = []
        self.init_addcards      = []

        self.public_state       = None
        #In the info sent to players, the private info always be None.
        self.private_state      = None
        
        
class ActionSpace:
    three   = 0;
    four    = 1;
    five    = 2;
    six     = 3;
    seven   = 4;
    eight   = 5;
    night   = 6;
    ten     = 7;
    J       = 8;
    Q       = 9;
    K       = 10;
    A       = 11;
    two     = 12;
    r       = 13;
    R       = 14;
    cheat   = 15;
    bid = 16;

class Action:
    def __init__(self, masterCard, slaveCard):
        self.masterCard         = masterCard
        self.slaveCard          = slaveCard

        self.masterValues2Num   = None
        self.slaveValues2Num    = None
        self.isMasterContinuous = None
        self.maxMasterCard      = None
        self.pattern            = None

    def isComplemented(self):

        flag = (self.masterValues2Num != None and \
                self.slaveValues2Num != None and \
                self.isMasterContinuous != None and \
                self.maxMasterCard  != None and \
                self.pattern != None)
        return flag

    def complement(self):

        self.masterValues2Num   = dict()
        for c in self.masterCard:
            if c in self.masterValues2Num:
                self.masterValues2Num[c] += 1
            else:
                self.masterValues2Num[c]  = 1

        self.slaveValues2Num    = dict()
        for c in self.slaveCard:
            if c in self.slaveValues2Num:
                self.slaveValues2Num[c] += 1
            else:
                self.slaveValues2Num[c]  = 1

        self.isMasterContinuous = 0
        num = 0
        for v in self.masterValues2Num:
            if (v + 1) in self.masterValues2Num and v < ActionSpace.two: 
                num += 1
        if num == len(self.masterValues2Num) -1 and len(self.masterValues2Num) != 1:
            self.isMasterContinuous = 1

        self.maxMasterCard = -1
        for c in self.masterValues2Num:
            if self.maxMasterCard < c:
                self.maxMasterCard = c

        
        ########################
        ## action 2 pattern ####
        ########################


        # is cheat?
        if len(self.masterCard) == 1 \
            and len(self.slaveCard) == 0 \
            and self.masterCard[0] == ActionSpace.cheat:
                self.pattern = AllPatterns["i_cheat"]

        # is roblord
        elif len(self.masterCard) == 1 \
            and len(self.slaveCard) == 0 \
            and self.masterCard[0] == ActionSpace.bid:
                self.pattern = AllPatterns["i_robLord"] 

        # is twoKings
        elif len(self.masterCard) == 2 \
            and len(self.masterValues2Num) == 2\
            and len(self.slaveCard) == 0 \
            and self.masterCard[0] in [ActionSpace.r, ActionSpace.R] \
            and self.masterCard[1] in [ActionSpace.r, ActionSpace.R]:
                 self.pattern = AllPatterns["x_twoKings"]
            
        else:

            ## process masterCard
            masterValues = self.masterValues2Num
            if len(masterValues) > 0:
                count = masterValues[self.masterCard[0]]
                for c in masterValues:
                    if masterValues[c] != count:    
                        self.pattern = AllPatterns["i_invalid"]


            ## process slave card
            slaveValues = self.slaveValues2Num
            if len(slaveValues) > 0:
                count = slaveValues[self.slaveCard[0]]
                for c in slaveValues:
                    if slaveValues[c] != count: 
                        self.pattern = AllPatterns["i_invalid"]

           
            if self.pattern == None:
                pattern = "p_%d_%d_%d_%d_%d"%(  len(self.masterCard), len(masterValues),\
                                                self.isMasterContinuous,\
                                                len(self.slaveCard),  len(slaveValues))

                if pattern in AllPatterns:
                    self.pattern = AllPatterns[pattern]
                else:
                    self.pattern = AllPatterns["i_invalid"]



        return self

class Phase:
    bid = 0
    play = 1


AllPatterns  = dict();
#p_NumMasterCard_NumMasterValues_isContinous_NumSlaveCard_NumSlaveValues
#(name, ChinesName, NumMasterCard, NumMasterValues, isContinous(0,1), NumSlaveCard, NumSlaveValues,rank)
AllPatterns["i_invalid"]      =  ("i_invalid",      "非法出牌",     0,0,0,0,0,-1) #special process logic
AllPatterns["i_cheat"]        =  ("i_cheat",        "过",           1,1,0,0,0,-1) #special process logic
AllPatterns["i_robLord"]      =  ("i_robLord",      "叫地主",       1,1,0,0,0,-1) #special process logic
AllPatterns["x_twoKings"]     =  ("x_twoKings",     "王炸",         2,2,1,0,0,100) #special process logic
AllPatterns["p_1_1_0_0_0"]    =  ("p_1_1_0_0_0",    "单牌",         1,1,0,0,0,1)
AllPatterns["p_2_1_0_0_0"]    =  ("p_2_1_0_0_0",    "对子",         2,1,0,0,0,1) 
AllPatterns["p_3_1_0_0_0"]    =  ("p_3_1_0_0_0",    "三带",         3,1,0,0,0,1) 
AllPatterns["p_4_1_0_0_0"]    =  ("p_4_1_0_0_0",    "炸弹",         4,1,0,0,0,10) 
AllPatterns["p_3_1_0_1_1"]    =  ("p_3_1_0_1_1",    "三带一",       3,1,0,1,1,1)
AllPatterns["p_5_5_1_0_0"]    =  ("p_5_5_1_0_0",    "顺子5",        5,5,1,0,0,1)
AllPatterns["p_3_1_0_2_1"]    =  ("p_3_1_0_2_1",    "三带对",       3,1,0,2,1,1)
AllPatterns["p_6_6_1_0_0"]    =  ("p_6_6_1_0_0",    "顺子6",        6,6,1,0,0,1)
AllPatterns["p_6_3_1_0_0"]    =  ("p_6_3_1_0_0",    "连对3",        6,3,1,0,0,1)
AllPatterns["p_6_2_1_0_0"]    =  ("p_6_2_1_0_0",    "2飞机",        6,2,1,0,0,1)
AllPatterns["p_4_1_0_2_2"]    =  ("p_4_1_0_2_2",    "四带2单",      4,1,0,2,2,1)
AllPatterns["p_7_7_1_0_0"]    =  ("p_7_7_1_0_0",    "顺子7",        7,7,1,0,0,1)
AllPatterns["p_8_8_1_0_0"]    =  ("p_8_8_1_0_0",    "顺子8",        8,8,1,0,0,1)
AllPatterns["p_8_4_1_0_0"]    =  ("p_8_4_1_0_0",    "连对4",        8,4,1,0,0,1)
AllPatterns["p_6_2_1_2_2"]    =  ("p_6_2_1_2_2",    "飞机带2单",    6,2,1,2,2,1)
AllPatterns["p_4_1_0_4_2"]    =  ("p_4_1_0_4_2",    "四带2对",      4,1,0,4,2,1)
#AllPatterns["p_8_2_1_0_0"]    =  ("p_8_2_1_0_0",    "两个连续炸弹", 8,2,1,0,0,?)
AllPatterns["p_9_9_1_0_0"]    =  ("p_9_9_1_0_0",    "顺子9",        9,9,1,0,0,1)
AllPatterns["p_9_3_1_0_0"]    =  ("p_9_3_1_0_0",    "3飞机",        9,3,1,0,0,1)
AllPatterns["p_10_10_1_0_0"]  =  ("p_10_10_1_0_0",  "顺子10",       10,10,1,0,0,1)
AllPatterns["p_10_5_1_0_0"]   =  ("p_10_5_1_0_0",   "连对5",        10,5,1,0,0,1)
AllPatterns["p_6_2_1_4_2"]    =  ("p_6_2_1_4_2",    "2飞机带2对",   6,2,1,4,2,1)
AllPatterns["p_11_11_1_0_0"]  =  ("p_11_11_1_0_0",  "顺子11",       11,11,1,0,0,1)
AllPatterns["p_12_12_1_0_0"]  =  ("p_12_12_1_0_0",  "顺子12",       12,12,1,0,0,1)
AllPatterns["p_12_6_1_0_0"]   =  ("p_12_6_1_0_0",   "连对6",        12,6,1,0,0,1)
AllPatterns["p_12_4_1_0_0"]   =  ("p_12_4_1_0_0",   "4飞机",        12,4,1,0,0,1)
AllPatterns["p_9_3_1_3_3"]    =  ("p_9_3_1_3_3",    "3飞机带3单",   9,3,1,3,3,1)
#AllPatterns["p_12_3_0_0_0"]   =  ("p_12_3_0_0_0",   "3炸弹",        12,3,0,0,0,?)
#AllPatterns["p_8_2_0_4_4"]    =  ("p_8_2_0_4_4",    "2炸弹带4单",   8,2,0,4,4,?)
AllPatterns["p_14_7_1_0_0"]   =  ("p_14_7_1_0_0",   "连对7",        14,7,1,0,0,1)
AllPatterns["p_15_5_1_0_0"]   =  ("p_15_5_1_0_0",   "5飞机",        15,5,1,0,0,1)
AllPatterns["p_9_3_1_6_3"]    =  ("p_9_3_1_6_3",    "3飞机带3对子", 9,3,1,6,3,1)
AllPatterns["p_16_8_1_0_0"]   =  ("p_16_8_1_0_0",   "连对8",        16,8,1,0,0,1)
AllPatterns["p_12_4_1_4_4"]   =  ("p_12_4_1_4_4",   "4飞机带4单",   12,4,1,4,4,1)
#AllPatterns["p_16_4_0_0_0"]   =  ("p_16_4_0_0_0",   "4炸弹",        16,4,0,0,0,?)
#AllPatterns["p_8_2_0_8_4"]    =  ("p_8_2_0_8_4",    "2炸弹带4对",   8,2,0,8,4,?)
AllPatterns["p_18_9_1_0_0"]   =  ("p_18_9_1_0_0",   "连对9",        18,9,1,0,0,1)
AllPatterns["p_18_6_1_0_0"]   =  ("p_18_6_1_0_0",   "6飞机",        18,6,1,0,0,1)
#AllPatterns["p_12_3_0_6_6"]   =  ("p_12_3_0_6_6",   "3炸弹带6单",   12,3,0,6,6,?)
AllPatterns["p_20_10_1_0_0"]  =  ("p_20_10_1_0_0",  "连对10",       20,10,1,0,0,1)
AllPatterns["p_15_5_1_5_5"]   =  ("p_15_5_1_5_5",   "5飞机带5单",   15,5,1,5,5,1)
#AllPatterns["p_20_5_0_0_0"]   =  ("p_20_5_0_0_0_0", "5炸弹",        20,5,0,0,0,?)
AllPatterns["p_12_4_1_8_4"]   =  ("p_12_4_1_8_4",   "4飞机带4对",   12,4,1,8,4,1)



## ActionCompare (exclude the invalid, cheat and roblord actions)
## return rank(action1) - rank(action2)
def compareActions(action1, action2): 

    if action1.isComplemented() == False:
        action1.complement()
    if action2.isComplemented() == False:
        action2.complement()

    if  action1.pattern[0] in ["i_invalid","i_cheat","i_robLord"] or\
        action2.pattern[0] in ["i_invalid","i_cheat","i_robLord"]:
        raise Exception("We can't compare the invalid and robLord actions' rank")

    
    if action1.pattern[7] != action2.pattern[7]:
        return action1.pattern[7] - action2.pattern[7]

    if action1.pattern[7] == action2.pattern[7]:
        if action1.pattern[0] != action2.pattern[0]:
            raise Exception("We can't compare %s to %s"%(action1pattern[0],action2pattern[0])) 

        return action1.maxMasterCard - action2.maxMasterCard

        return flag   



## check whether is it valid to generate actions from the cards
def isActionGeneratedFromCards(action, hand_cards):
    flag = True;

    if action.isComplemented() == False:
        action.complement()

    for a in action.masterValues2Num:
        flag = flag and (action.masterValues2Num[a] <= hand_cards[a])

    for a in action.slaveValues2Num:
        flag = flag and (action.slaveValues2Num[a] <= hand_cards[a])

    return flag

## check
def removeActionFromCards(action, hands_cards):
    if action.isComplement() == False:
        action.complement()

    for a in action.masterValues2Num:
        hand_cards[a] -= action.masterValues2Num[a]

    for a in action.slaveValues2Num:
        hand_cards[a] -= action.slaveValues2Num[a]

    return hand_cards

