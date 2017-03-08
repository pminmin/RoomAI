#!/bin/python
#coding:utf-8

import roomai

#
#0, 1, 2, 3, ..., 7,  8, 9, 10, 11, 12, 13, 14
#^                ^   ^              ^       ^
#|                |   |              |       |
#3,               10, J, Q,  K,  A,  2,  r,  R
#

class PhaseSpace:
    bid  = 0
    play = 1

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
    bid     = 16;

class PrivateState:
    def __init__(self):
        self.hand_cards         = [[],[],[]]
        self.num_hand_cards     = [-1,-1,-1]
        self.additive_cards     = []

class PublicState:

    def __init__(self):

        self.landlord_candidate_id  = -1
        self.landlord_id            = -1
        self.license_playerid       = -1
        self.license_action         = None
        self.is_response            = False

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
        
        
class Action:
    def __init__(self, masterCards, slaveCards):
        self.masterCards        = masterCards
        self.slaveCards         = slaveCards

        self.masterValues2Num   = None
        self.slaveValues2Num    = None
        self.isMasterStraight = None
        self.maxMasterCard      = None
        self.pattern            = None

    def isComplemented(self):

        flag = (action.masterValues2Num != None and \
                action.slaveValues2Num != None and \
                action.isMasterStraight != None and \
                action.maxMasterCard  != None and \
                action.pattern != None)
        return flag

    def complement(self):
        Utils.action2pattern(self)
        


class PrivateState(AbstractPrivateState):
    def __init__(self):
        self.hand_cards         = [[],[],[]]
        self.num_hand_cards     = [-1,-1,-1]
        self.additive_cards     = []

class PublicState(AbstractPublicState):

    def __init__(self):

        self.landlord_candidate_id  = -1
        self.landlord_id            = -1
        self.license_playerid       = -1
        self.license_action         = None
        self.is_response            = False

        self.first_player           = -1
        self.turn                   = -1
        self.phase                  = -1
        self.epoch                  = -1

        self.previous_id            = -1
        self.previous_action        = None


class Info(AbstractInfo):
    def __init__(self):
        ### init
        self.init_id            = -1
        self.init_cards         = []
        self.init_addcards      = []

        self.public_state       = None
        #In the info sent to players, the private info always be None.
        self.private_state      = None

class Utils(AbstractUtils):

    #@override
    def is_action_valid(self,hand_cards, public_state, action):

        if action.isComplemented() == False:
            action.complement()

        if action.pattern[0] == "i_invalid":
            return False
    
        if is_action_from_handcards(hand_cards, action) == False:
            return False

        turn        = public_state.turn
        license_id  = public_state.license_palyerid
        license_act = public_state.license_action
        phase       = public_state.phase

        if phase == PhaseSpace.bid:
            if action.pattern[0] not in ["i_cheat", "i_bid"]:
                return False:
            return True

        if phase == PhaseSpace.play:
            if action.pattern[0] == "i_bid":    return False

            if license_id == turn:
                if action.pattern[0] == "i_cheat": return False
                return True

            else:
                if action.pattern[0] == "i_cheat":  return False

                if action.pattern[6] > license_act.pattern[6]:  return True
                elif action.pattern[6] < license_act.pattern[6]:    return False
                elif action.maxMasterCard - license_act.maxMasterCard > 0:  return True
                else:   return False

    def next_candidate_actions(hand_cards, public_state):

        if ps.is_response == False:
            actions = generate_actions_wrt_patterns(hand_cards, AllPatterns.values)
            return actions    
    
        else:
            patterns   = []
            patterns.append(info.public_state.license_action.pattern)

            if patterns[0][6] == 1:
                patterns.append(AllPatterns["p_4_1_0_0_0"])  #rank = 10
                patterns.append(AllPatterns["x_rocket"])     #rank = 100            

            if pattern[6] == 10:
                patterns.append(AllPatterns["x_rocket"])     #rank = 100

            actions = generate_actions_wrt_patterns(hand_cards, patterns)
            return actions


    def is_action_from_handcards(self, hand_cards, action):
            flag = True
            if action.isComplemented() == False:
            action.complement()

            if action.pattern[0] == "i_cheat":  return True
            if action.pattern[0] == "i_bid":    return True
            if action.pattern[0] == "i_invalid":    return False

            if a in action.masterValues2Num:
                flag = flag and (action.masterValues2Num[a] <= hand_cards[a])
            if a in action.action.slaveValues2Num:
                flag = flag and (action.action.slaveValues2Num[a] <= hand_cards[a])
            return flag

    def remove_action_from_handcards(self,hand_cards, action):
            if action.isComplemented() == False:
                action.complement()

            for a in action.masterValues2Num:
                hand_cards[a] -= action.masterValues2Num[a]
            for a in action.action.slaveValues2Num:
                hand_cards[a] -= actoin.action.slaveValues2Num[a]



    def action2pattern(self, action):

        action.masterValues2Num   = dict()
        for c in action.masterCards:
            if c in action.masterValues2Num:
                action.masterValues2Num[c] += 1
            else:
                action.masterValues2Num[c]  = 1

        action.action.slaveValues2Num    = dict()
        for c in action.slaveCards:
            if c in action.action.slaveValues2Num:
                action.action.slaveValues2Num[c] += 1
            else:
                action.action.slaveValues2Num[c]  = 1

        action.isMasterStraight = 0
        num = 0
        for v in action.masterValues2Num:
            if (v + 1) in action.masterValues2Num and v < ActionSpace.two: 
                num += 1
        if num == len(action.masterValues2Num) -1 and len(action.masterValues2Num) != 1:
            action.isMasterStraight = 1

        action.maxMasterCard = -1
        for c in action.masterValues2Num:
            if action.maxMasterCard < c:
                action.maxMasterCard = c

        
        ########################
        ## action 2 pattern ####
        ########################


        # is cheat?
        if len(action.masterCards) == 1 \
            and len(action.slaveCards) == 0 \
            and action.masterCards[0] == ActionSpace.cheat:
                action.pattern = AllPatterns["i_cheat"]

        # is roblord
        elif len(action.masterCards) == 1 \
            and len(action.slaveCards) == 0 \
            and action.masterCards[0] == ActionSpace.bid:
                action.pattern = AllPatterns["i_bid"] 

        # is twoKings
        elif len(action.masterCards) == 2 \
            and len(action.masterValues2Num) == 2\
            and len(action.slaveCards) == 0 \
            and action.masterCards[0] in [ActionSpace.r, ActionSpace.R] \
            and action.masterCards[1] in [ActionSpace.r, ActionSpace.R]:
                 action.pattern = AllPatterns["x_rocket"]
            
        else:

            ## process masterCards
            masterValues = action.masterValues2Num
            if len(masterValues) > 0:
                count = masterValues[action.masterCards[0]]
                for c in masterValues:
                    if masterValues[c] != count:    
                        action.pattern = AllPatterns["i_invalid"]


            ## process slave card
            action.slaveValues = action.slaveValues2Num
            if len(action.slaveValues) > 0:
                count = action.slaveValues[action.slaveCards[0]]
                for c in action.slaveValues:
                    if action.slaveValues[c] != count: 
                        action.pattern = AllPatterns["i_invalid"]

           
            if action.pattern == None:
                pattern = "p_%d_%d_%d_%d_%d"%(  len(action.masterCards), len(masterValues),\
                                                action.isMasterStraight,\
                                                len(action.slaveCards),  len(action.slaveValues))

                if pattern in AllPatterns:
                    action.pattern = AllPatterns[pattern]
                else:
                    action.pattern = AllPatterns["i_invalid"]



        return self



AllPatterns                     = dict();
file1 = open("patterns.txt")
for line in file1:
    line = line.replace(" ","").strip()
    line = line.split("#")[0]
    if len(line) == 0:  continue
    lines = line.split(",")

    for i in xrange(1,len(lines)):
        lines[i] = int(lines[i])
    AllPatterns[lines[0]] = lines
file1.close()

AllActions                      = []


HandCards2CandidateActions      = dict()
