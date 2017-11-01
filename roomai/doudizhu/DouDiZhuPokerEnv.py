#!/bin/python
#coding:utf-8

import random
import copy
import itertools

from roomai.doudizhu.DouDiZhuPokerInfo   import *
from roomai.doudizhu.DouDiZhuPokerAction import *

class DouDiZhuPokerEnv(roomai.common.AbstractEnv):
    '''
    The DouDiZhuPoker game environment
    '''

    def __init__(self):
        super(DouDiZhuPokerEnv, self).__init__()
        self.public_state  = DouDiZhuPublicState()
        self.private_state = DouDiZhuPrivateState()
        self.person_states = [DouDiZhuPersonState() for i in range(3)]



    def __update_license__(self, turn, action):
        if action.pattern[0] != "i_cheat":
            self.public_state.__license_playerid__ = turn
            self.public_state.__license_action__   = action
            

    def __update_cards__(self, turn, action):
        self.person_states[turn].hand_cards.__remove_action__(action)


    def __update_phase_bid2play__(self):
        self.public_state.__phase__                 = 1
        
        self.public_state.__landlord_id__           = self.public_state.landlord_candidate_id
        self.public_state.__license_playerid__      = self.public_state.turn
        self.public_state.__continuous_cheat_num__  = 0
        self.public_state.__is_response__           = False

        landlord_id = self.public_state.landlord_id
        self.public_state.__keep_cards__ = DouDiZhuPokerHandCards(self.private_state.keep_cards.key)
        self.person_states[landlord_id].hand_cards.__add_cards__(self.private_state.keep_cards)


    #@Overide
    def init(self, params = dict()):
        '''
        Initialize the DouDiZhuPoker game environment with the initialization params.\n
        The initialization is a dict with some options\n
        1) allcards: the order of all poker cards appearing\n
        2) record_history: whether to record all history states. if you need call the backward function, please set it to True. default False\n
        3) start_turn: players[start_turn] is first to take an action\n
        An example of the initialization param is {"start_turn":2,"record_history":True}\n

        :param params: the initialization params
        :return: infos, public_state, person_states, private_state
        '''

        if "allcards" in params:
            self.allcards = [c for c in params["allcards"]]
        else:
            self.cards = []
            for i in range(13):
                for j in range(4):
                    self.cards.append(DouDiZhuActionElement.rank_to_str[i])
            self.cards.append(DouDiZhuActionElement.rank_to_str[13])
            self.cards.append(DouDiZhuActionElement.rank_to_str[14])
            random.shuffle(self.cards)

        if "record_history" in params:
            self.record_history = params["record_history"]
        else:
            self.record_history = False

        if "start_turn" in params:
            self.start_turn = params["start_turn"]
        else:
            self.start_turn = int(random.random() * 2)

        for i in range(3):
            tmp = self.cards[i*17:(i+1)*17]
            tmp.sort()
            self.person_states[i].__hand_cards__ = DouDiZhuPokerHandCards("".join(tmp))
            self.person_states[i].__id__         = i

        keep_cards = DouDiZhuPokerHandCards([self.cards[-1], self.cards[-2], self.cards[-3]])
        self.private_state.__keep_cards__ =  keep_cards;
        
        self.public_state.__first_player__        = self.start_turn
        self.public_state.__turn__                = self.public_state.first_player
        self.public_state.__phase__               = 0
        self.public_state.__epoch__               = 0
        
        self.public_state.__landlord_id           = -1
        self.public_state.__license_playerid__    = self.public_state.turn
        self.public_state.__license_action__      = None
        self.public_state.__is_terminal__         = False
        self.public_state.__scores__              = [0,0,0]

        turn = self.public_state.turn
        self.person_states[turn].__available_actions__ = DouDiZhuPokerEnv.available_actions(self.public_state, self.person_states[turn])

        infos = self.__gen_infos__()
        self.__gen_history__()

        return infos, self.public_state, self.person_states, self.private_state


    ## we need ensure the action is valid
    #@Overide
    def forward(self, action):
        '''
        The game environment steps with the action taken by the current player
        
        :param action: The action taken by the current player
        :return: infos, public_state, person_states, private_state
        '''

        if self.is_action_valid(action, self.public_state, self.person_states[self.public_state.turn]) is False:
            raise  ValueError("%s action is invalid"%(action.key))

        turn = self.public_state.turn
        if self.public_state.phase == 0:
            if action.pattern[0] == "i_bid":
                self.public_state.__landlord_candidate_id__ = turn

            if self.public_state.epoch == 3 and self.public_state.landlord_candidate_id == -1:
                self.public_state.__is_terminal__ = True
                self.public_state.__scores__      = [0.0, 0.0, 0.0]

                self.__gen_history__()
                infos = self.__gen_infos__()
                return infos, self.public_state, self.person_states, self.private_state

            if (self.public_state.epoch == 2 and self.public_state.landlord_candidate_id != -1)\
                or self.public_state.epoch == 3:
                self.__update_phase_bid2play__()


                self.public_state.__previous_id__ = turn
                self.public_state.__previous_action__ = action
                self.public_state.__epoch__ += 1
                self.person_states[self.public_state.turn].__available_actions__ =\
                    DouDiZhuPokerEnv.available_actions(self.public_state, self.person_states[self.public_state.turn])

                self.__gen_history__()
                infos = self.__gen_infos__()

                return infos, self.public_state, self.person_states, self.private_state


        else: #phase == play

            if action.pattern[0] != "i_cheat":
                
                self.__update_cards__(turn, action)
                self.__update_license__(turn, action)
                self.public_state.__continuous_cheat_num__ = 0
    
                num = self.person_states[turn].hand_cards.num_card
                if num == 0:
                    self.public_state.__previous_id__ = turn
                    self.public_state.__previous_action__ = action
                    self.public_state.__epoch__ += 1
                    if turn == self.public_state.landlord_id:
                        self.public_state.__is_terminal__                           = True
                        self.public_state.__scores__                                = [-1,-1,-1]
                        self.public_state.__scores__[self.public_state.landlord_id] = 2
                    else:
                        self.public_state.__is_terminal__                           = True
                        self.public_state.__scores__                                = [1,1,1]
                        self.public_state.__scores__[self.public_state.landlord_id] = -2
                    self.__gen_history__()
                    infos = self.__gen_infos__()
                    return infos, self.public_state, self.person_states, self.private_state
            else:
                self.public_state.__continuous_cheat_num__ += 1


        self.public_state.__turn__   = (turn+1)%3


        if self.public_state.continuous_cheat_num == 2:
            self.public_state.__is_response__          = False
            self.public_state.__continuous_cheat_num__ = 0
        else:
            self.public_state.__is_response__ = True


        self.public_state.__previous_id__         = turn
        self.public_state.__previous_action__     = action
        self.public_state.__epoch__              += 1
        self.person_states[self.public_state.turn].__available_actions__\
            = DouDiZhuPokerEnv.available_actions(self.public_state, self.person_states[self.public_state.turn])
         
        self.__gen_history__()
        infos = self.__gen_infos__()

        return infos, self.public_state, self.person_states, self.private_state


    #@override
    @classmethod
    def compete(cls, env, players):
        '''
        Use the game environment to hold a compete for the players

        :param env: The game environment
        :param players: The players
        :return: scores for the players
        '''
        infos ,public_state, person_states, private_state= env.init()

        for i in range(len(players)):
            players[i].receive_info(infos[i])

        while public_state.is_terminal == False:
            turn = public_state.turn
            action = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)
            for i in range(len(players)):
                players[i].receive_info(infos[i])

        return public_state.scores



    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        Generate all valid action given the public state and the person state
        
        :param public_state: 
        :param person_state: 
        :return: A dict(action_key, action) contains all valid actions
        '''

        patterns = []
        if public_state.phase == 0:
            patterns.append(AllPatterns["i_cheat"])
            patterns.append(AllPatterns["i_bid"])
        else:
            if public_state.is_response == False:
                for p in AllPatterns:
                    if p != "i_cheat" and p != "i_invalid":
                        patterns.append(AllPatterns[p])
            else:
                patterns.append(public_state.license_action.pattern)
                if public_state.license_action.pattern[6] == 1:
                    patterns.append(AllPatterns["p_4_1_0_0_0"])  # rank = 10
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                if public_state.license_action.pattern[6] == 10:
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                patterns.append(AllPatterns["i_cheat"])

        actions = dict()
        for pattern in patterns:
            numMaster = pattern[1]
            numMasterPoint = pattern[2]
            isStraight = pattern[3]
            numSlave = pattern[4]
            MasterCount = -1
            SlaveCount = -1

            if numMaster > 0:
                MasterCount = int(numMaster / numMasterPoint)

            if "i_invalid" == pattern[0]:
                continue

            if "i_cheat" == pattern[0]:
                action_key = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["x"]], [])
                action     = DouDiZhuPokerAction.lookup(action_key)
                if cls.is_action_valid(action,public_state, person_state) == True:
                    actions[action_key] = action
                continue

            if "i_bid" == pattern[0]:
                action_key = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["b"]], [])
                action     = DouDiZhuPokerAction.lookup(action_key)
                if cls.is_action_valid(action, public_state,person_state) == True:
                    actions[action_key] = action
                continue

            if pattern[0] == "x_rocket":
                if person_state.hand_cards.card_pointrank_count[DouDiZhuActionElement.str_to_rank["r"]] == 1 and \
                                person_state.hand_cards.card_pointrank_count[DouDiZhuActionElement.str_to_rank["R"]] == 1:
                    action_key  = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["r"], DouDiZhuActionElement.str_to_rank["R"]], [])
                    action      = DouDiZhuPokerAction.lookup(action_key)
                    if cls.is_action_valid(action,public_state,person_state) == True:
                        actions[action_key] = action
                continue

            if pattern[1] + pattern[4] > person_state.hand_cards.num_card:
                continue
            sum1 = 0

            for count in range(MasterCount, 5, 1):
                sum1 += person_state.hand_cards.count2num[count]
            if sum1 < numMasterPoint:
                continue

            ### action with cards
            mCardss = []
            mCardss = DouDiZhuPokerEnv.__extractMasterCards__(person_state.hand_cards, pattern)

            for mCards in mCardss:
                if numSlave == 0:
                    action_key   = DouDiZhuPokerAction.__master_slave_cards_to_key__(mCards, [])
                    action       = DouDiZhuPokerAction.lookup(action_key)
                    if cls.is_action_valid(action, public_state,person_state) == True:
                        actions[action_key] = action
                    continue

                sCardss = DouDiZhuPokerEnv.__extractSlaveCards__(person_state.hand_cards, mCards, pattern)
                for sCards in sCardss:

                    action_key  = DouDiZhuPokerAction.__master_slave_cards_to_key__(mCards, sCards)
                    action      = DouDiZhuPokerAction.lookup(action_key)
                    if cls.is_action_valid(action, public_state,person_state) == True:
                        actions[action_key] = action
        return actions



    @classmethod
    def is_action_valid(cls,action, public_state, person_state):
        '''
        Is the action is valid given the public state and the person state
        
        :param action: 
        :param public_state: 
        :param person_state: 
        :return: An boolean variable
        '''
        if action.pattern[0] == "i_invalid":
            return False

        if cls.__is_action_from_handcards__(person_state.hand_cards, action) == False:
            return False

        turn        = public_state.turn
        license_id  = public_state.license_playerid
        license_act = public_state.license_action
        phase       = public_state.phase

        if phase == 0:
            if action.pattern[0] not in ["i_cheat", "i_bid"]:
                return False
            return True

        if phase == 1:
            if action.pattern[0] == "i_bid":    return False

            if public_state.is_response == False:
                if action.pattern[0] == "i_cheat": return False
                return True

            else:  # response
                if action.pattern[0] == "i_cheat":  return True
                ## not_cheat
                if action.pattern[6] > license_act.pattern[6]:
                    return True
                elif action.pattern[6] < license_act.pattern[6]:
                    return False
                elif action.maxMasterPoint - license_act.maxMasterPoint > 0:
                    return True
                else:
                    return False

    @classmethod
    def __is_action_from_handcards__(cls, hand_cards, action):
        flag = True
        if action.pattern[0] == "i_cheat":  return True
        if action.pattern[0] == "i_bid":    return True
        if action.pattern[0] == "i_invalid":    return False

        for a in action.masterPoints2Count:
            flag = flag and (action.masterPoints2Count[a] <= hand_cards.card_pointrank_count[a])
        for a in action.slavePoints2Count:
            flag = flag and (action.slavePoints2Count[a] <= hand_cards.card_pointrank_count[a])
        return flag


    @classmethod
    def __extractMasterCards__(cls, hand_cards, pattern):
        is_straight = pattern[3]
        cardss = []
        ss = []

        numPoint = pattern[2]
        if numPoint <= 0:
            return cardss
        count = int(pattern[1]/numPoint)

        if is_straight == 1:
            c = 0
            for i in range(11, -1, -1):
                if hand_cards.card_pointrank_count[i] >= count:
                    c += 1
                else:
                    c = 0

                if c >= numPoint:
                    ss.append(range(i, i + numPoint))
        else:
            candidates = []
            for c in range(len(hand_cards.card_pointrank_count)):
                if hand_cards.card_pointrank_count[c] >= count:
                    candidates.append(c)
            if len(candidates) < numPoint:
                return []
            ss = list(itertools.combinations(candidates, numPoint))

        for set1 in ss:
            s = []
            for c in set1:
                for i in range(count):
                    s.append(c)
            s.sort()
            cardss.append(s)

        return cardss

    @classmethod
    def __extractSlaveCards__(cls, hand_cards, used_cards, pattern):
        used = [0 for i in range(15)]
        for p in used_cards:
            used[p] += 1

        numMaster = pattern[1]
        numMasterPoint = pattern[2]
        numSlave = pattern[4]

        candidates = []
        res1 = []
        res = []

        if numMaster / numMasterPoint == 3:
            if numSlave / numMasterPoint == 1:  # single
                for c in range(len(hand_cards.card_pointrank_count)):
                    if used[c] != 0: continue
                    for i in range(hand_cards.card_pointrank_count[c] - used[c]):
                        candidates.append(c)
                if len(candidates) >= numSlave:
                    res1 = list(set(list(itertools.combinations(candidates, numSlave))))
                for sCard in res1:  res.append([x for x in sCard])

            elif numSlave / numMasterPoint == 2:  # pair
                for c in range(len(hand_cards.card_pointrank_count)):
                    if used[c] != 0: continue
                    for i in range (int((hand_cards.card_pointrank_count[c] - used[c])/2)) :
                        candidates.append(c)
                if len(candidates) >= numSlave / 2:
                    res1 = list(set(list(itertools.combinations(candidates, int(numSlave / 2)))))
                for sCard in res1:
                    tmp = [x for x in sCard]
                    tmp.extend([x for x in sCard])
                    res.append(tmp)

        elif numMaster / numMasterPoint == 4:

            if numSlave / numMasterPoint == 2:  # single
                for c in range(len(hand_cards.card_pointrank_count)):
                    if used[c] != 0: continue
                    for i in range(hand_cards.card_pointrank_count[c] - used[c]):
                        candidates.append(c)
                if len(candidates) >= numSlave:
                    res1 = list(set(list(itertools.combinations(candidates, numSlave))))
                for sCard in res1:  res.append([x for x in sCard])


            elif numSlave / numMasterPoint == 4:  # pair
                for c in range(len(hand_cards.card_pointrank_count)):
                    if used[c] != 0: continue
                    for i in range(int((hand_cards.card_pointrank_count[c] - used[c])/2)):
                        candidates.append(c)
                if len(candidates) >= numSlave / 2:
                    res1 = list(set(list(itertools.combinations(candidates, int(numSlave / 2)))))
                for sCard in res1:
                    tmp = [x for x in sCard]
                    tmp.extend([x for x in sCard])
                    res.append(tmp)

        return res


    @classmethod
    def __action_priority__(cls, action1, action2):
        count1 = action1.pattern[1] / action1.pattern[2]
        count2 = action2.pattern[1] / action2.pattern[2]
        if count1 != count2:
            return count1 - count2

        numMaster1 = action1.pattern[1]
        numMaster2 = action2.pattern[1]
        if numMaster1 != numMaster2:
            return numMaster1  - numMaster2

        if action1.maxMasterPoint != action2.maxMasterPoint:
            return action1.maxMasterPoint - action2.maxMasterPoint

        raise ValueError("can't compare priorities of %s and %s "%(action1.key,action2))


    @classmethod
    def __available_actions_generate_all__(cls):
        public_state = DouDiZhuPublicState()
        person_state = DouDiZhuPersonState()
        public_state.__is_response__    = False
        person_state.__hand_cards__     = DouDiZhuPokerHandCards("")
        for i in range(13):
            for j in range(4):
                person_state.hand_cards.__add_cards__(DouDiZhuActionElement.rank_to_str[i])
        person_state.hand_cards.__add_cards__(DouDiZhuActionElement.rank_to_str[DouDiZhuActionElement.str_to_rank["r"]])
        person_state.hand_cards.__add_cards__(DouDiZhuActionElement.rank_to_str[DouDiZhuActionElement.str_to_rank["R"]])
        actions = dict()


        patterns = []
        if public_state.phase == 0:
            patterns.append(AllPatterns["i_cheat"])
            patterns.append(AllPatterns["i_bid"])
        else:
            if public_state.is_response == False:
                for p in AllPatterns:
                    if p != "i_cheat" and p != "i_invalid":
                        patterns.append(AllPatterns[p])
            else:
                patterns.append(public_state.license_action.pattern)
                if public_state.license_action.pattern[6] == 1:
                    patterns.append(AllPatterns["p_4_1_0_0_0"])  # rank = 10
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                if public_state.license_action.pattern[6] == 10:
                    patterns.append(AllPatterns["x_rocket"])  # rank = 100
                patterns.append(AllPatterns["i_cheat"])


        actions = dict()

        for pattern in patterns:
            numMaster = pattern[1]
            numMasterPoint = pattern[2]
            isStraight = pattern[3]
            numSlave = pattern[4]
            MasterCount = -1
            SlaveCount = -1

            if numMaster > 0:
                MasterCount = int(numMaster / numMasterPoint)

            if "i_invalid" == pattern[0]:
                continue

            if "i_cheat" == pattern[0]:
                action_key = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["x"]], [])
                action     = DouDiZhuPokerAction([DouDiZhuActionElement.str_to_rank["x"]], [])
                if action_key in actions:
                    if cls.__action_priority__(action, actions[action_key]) > 0:
                        actions[action_key] = action
                else:
                    actions[action_key] = action

                continue

            if "i_bid" == pattern[0]:
                action_key = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["b"]], [])
                action = DouDiZhuPokerAction([DouDiZhuActionElement.str_to_rank["b"]], [])
                if action_key in actions:
                    if cls.__action_priority__(action, actions[action_key]) > 0:
                        actions[action_key] = action
                else:
                    actions[action_key] = action
                continue

            if pattern[0] == "x_rocket":
                if person_state.hand_cards.card_pointrank_count[DouDiZhuActionElement.str_to_rank["r"]] == 1 and \
                                person_state.hand_cards.card_pointrank_count[DouDiZhuActionElement.str_to_rank["R"]] == 1:
                    action_key  = DouDiZhuPokerAction.__master_slave_cards_to_key__([DouDiZhuActionElement.str_to_rank["r"], DouDiZhuActionElement.str_to_rank["R"]], [])
                    action = DouDiZhuPokerAction([DouDiZhuActionElement.str_to_rank["r"], DouDiZhuActionElement.str_to_rank["R"]], [])
                    if action_key in actions:
                        if cls.__action_priority__(action, actions[action_key]) > 0:
                            actions[action_key] = action
                    else:
                        actions[action_key] = action
                continue

            if pattern[1] + pattern[4] > person_state.hand_cards.num_card:
                continue
            sum1 = 0

            for count in range(MasterCount, 5, 1):
                sum1 += person_state.hand_cards.count2num[count]
            if sum1 < numMasterPoint:
                continue

            ### action with cards
            mCardss = []
            mCardss = DouDiZhuPokerEnv.__extractMasterCards__(person_state.hand_cards, pattern)

            for mCards in mCardss:
                if numSlave == 0:
                    action_key   = DouDiZhuPokerAction.__master_slave_cards_to_key__(mCards, [])
                    action = DouDiZhuPokerAction(mCards, [])
                    if action_key in actions:
                        if cls.__action_priority__(action, actions[action_key]) > 0:
                            actions[action_key] = action
                    else:
                        actions[action_key] = action
                    continue

                sCardss = DouDiZhuPokerEnv.__extractSlaveCards__(person_state.hand_cards, mCards, pattern)
                for sCards in sCardss:
                    action_key  = DouDiZhuPokerAction.__master_slave_cards_to_key__(mCards, sCards)
                    action = DouDiZhuPokerAction(mCards, sCards)
                    if action_key in actions:
                        if cls.__action_priority__(action, actions[action_key]) > 0:
                            actions[action_key] = action
                    else:
                        actions[action_key] = action
        return actions
