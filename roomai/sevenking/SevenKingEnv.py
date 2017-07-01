#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPublicState
from roomai.sevenking import SevenKingPrivateState
from roomai.sevenking import SevenKingPersonState
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingPokerCard
from roomai.sevenking import AllSevenKingPokerCards


AllPatterns = dict()
###
###numCards, requireSamePoint, requireStraight
AllPatterns["p_0_0_0"] = ("p_0_0_0",0,0,0) ## check
AllPatterns["p_1_1_0"] = ("p_1_1_0",1,1,0)
AllPatterns["p_2_1_0"] = ("p_1_1_0",2,1,0)
AllPatterns["p_3_1_0"] = ("p_3_1_0",3,1,0)
AllPatterns["p_4_1_0"] = ("p_4_1_0",4,1,0)
AllPatterns["p_3_0_1"] = ("p_3_0_1",3,0,1)
AllPatterns["p_4_0_1"] = ("p_4_0_1",4,0,1)
AllPatterns["p_5_0_1"] = ("p_3_0_1",5,0,1)

class SevenKingEnv(roomai.common.AbstractEnv):
    num_players = 2

    def init(self):
        self.public_state  = SevenKingPublicState()
        self.private_state = SevenKingPrivateState()
        self.person_states = [SevenKingPersonState() for i in range(self.num_players)]

        self.public_state_history  = []
        self.private_state_history = []
        self.person_states_history = []

        ## private_state
        self.private_state.keep_cards = [c.__deepcopy__() for c in AllSevenKingPokerCards]
        self.private_state.hand_cards = [[] for i in range(self.num_players)]
        for i in range(self.num_players):
            for j in range(5):
                c = self.private_state.keep_cards[-1]
                self.private_state.keep_cards = self.private_state.keep_cards.pop()
                self.private_state.hand_cards[i].append(c)

        ## public_state
        self.public_state.turn            = self.choose_player_with_lowest_card(self.private_state.hand_cards)
        self.public_state.is_terminal     = False
        self.public_state.scores          = []
        self.public_state.previous_id     = None
        self.public_state.previous_action = None

        self.public_state.num_players     = self.num_players
        self.public_state.num_keep_cards  = len(self.private_state.keep_cards)
        self.public_state.num_hand_cards  = [len(cards) for cards in self.private_state.hand_cards]

        ## person_state
        for i in range(self.num_players):
            self.person_states[i].id         = i
            self.person_states[i].hand_card  = [c.__deepcopy__() for c in self.private_state.hand_cards[i]]
            if i == self.public_state.turn:
                self.person_states[i].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[i])

        self.__gen_history__()
        infos = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def forward(self, action):
        turn = self.public_state.turn
        if SevenKingEnv.is_action_valid(action, self.public_state) == False:
            raise  ValueError("The %s is an invalid action "%(action.get_key()))

        ## the action plays its role
        if action.pattern[0] == "p_0_0_0":
            self.public_state.is_check[turn] = True
            self.public_state.num_check     -= 1
            self.person_states[turn].available_actions = dict()
        else:
            self.person_states[turn].hand_card = [c.__deepcopy__() for c in self.private_state.hand_cards[turn]]



        ## termminal
        if self.public_state.stage == 1 and len(self.private_state.hand_cards[turn]) == 0:
            self.public_state.is_terminal = True
            self.public_state.scores      = self.compute_scores
        ## stage 0 to 1
        elif len(self.private_state.keep_cards) < 5:
            new_turn                                       = turn
            self.public_state.turn                         = new_turn
            self.public_state.num_check                    = 0
            self.public_state.is_check                     = [False for i in range(self.public_state.num_players)]
            self.person_states[new_turn].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[new_turn])
        ## round next
        elif self.public_state.num_check + 1 == self.public_state.num_players:
            new_turn                                       = self.choose_player_with_lowest_card(self.private_state.hand_cards)
            self.person_states[new_turn].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[new_turn])
        else:
            new_turn                                       = (turn + 1) % self.public_state.num_players
            self.person_states[new_turn].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[new_turn])



        self.__gen_history__()
        infos = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def compute_scores(self):
        return 0
    def choose_player_with_lowest_card(self,hand_cards):
        return 0

    ######################## Utils function ###################
    @classmethod
    def compete(cls, env, players):
        env.num_players = len(players)
        infos, public_state, person_states, private_state = env.init()
        for i in range(env.num_players):
            players[i].receive_info(infos[i])

        while public_state.is_terminal == False:
            turn   = public_state.turn
            action = players[turn].take_action()
            infos, public_state, person_states, private_state = env.forward(action)
            for i in range(env.num_players):
                players[i].receive_info(infos[i])

        return public_state.scores

    @classmethod
    def action2pattern(cls, action):
        ###numCards, isSamePoint, isStraight
        num_cards               = len(action.cards)
        if num_cards == 0:
            return AllPatterns["p_0_0_0"]
        else:
            isSamePoint = 1
            isStraight  = 1
            point  = action.cards[0].get_point_rank()
            for i in range(1,len(action.cards)):
                card = action.cards[i]
                if point != card.get_point_rank():
                    isSamePoint = 0
                if point != card.get_point_rank() - 1:
                    isStraight  = 0
                point = card.get_point_rank()
            return AllPatterns["p_%d_%d_%d"%(num_cards,isSamePoint,isStraight)]

    def is_action_valid(self, action, public_state, person_state):
        ### is action from hand_cards
        hand_keys = dict()
        for c in person_state.hand_cards:
            key = c.get_key()
            if c not in hand_keys:  hand_keys[key] = 1
            else:  hand_keys[c] += 1
        action_keys = dict()
        for c in action.cards:
            key = c.get_key()
            if c not in action_keys: action_keys[key] = 1
            else:action_keys[key] +=1

        for k in action_keys:
            if k not in hand_keys or hand_keys[k] < action_keys[k]:
                return False

        ## pattern
        previous_action = public_state.previous_action
        if previous_action is None:
            previous_action = SevenKingAction("")
        if previous_action.pattern[0] != "p_0_0_0" and previous_action.pattern[0] != action.pattern[0]:
            return False

        ## large
        if previous_action.pattern[0] != "p_0_0_0":
            max_action_card = action.cards[0]
            for c in action.cards:
                if SevenKingPokerCard.compare(max_action_card,c) < 0:
                    max_action_card = c
            max_previous_card = previous_action.cards[0]
            for c in previous_action.cards:
                if SevenKingPokerCard.compare(max_previous_card,c) < 0:
                    max_previous_card = c
            if SevenKingPokerCard.compare(max_action_card, max_previous_card) < 0 :
                return False

        return True



    ########################### about gen_available_actions ########################
    @classmethod
    def __gen_available_actions_with_pattern(cls, hand_cards, pattern):
        pass

    @classmethod
    def available_actions(cls, public_state, person_state):
        available_actions      = dict()
        available_actions[""]  = SevenKingAction("")

        previous_action = public_state.previous_action
        if previous_action is None:
            previous_action = SevenKingAction("")
        hand_cards = person_state.hand_cards

        if previous_action.pattern[0] == "p_0_0_0":
            for pattern in AllPatterns.values():
                actions = cls.__gen_available_actions_with_pattern(hand_cards, pattern)
                for action in actions:
                    if cls.is_action_valid(action, public_state, person_state) == True:
                        available_actions[action.get_key()] = action
        else:
            actions = cls.__gen_available_actions_with_pattern(hand_cards, AllPatterns["p_0_0_0"])
            for action in actions:
                if cls.is_action_valid(action, public_state, person_state) == True:
                    available_actions[action.get_key()] = action


        return available_actions

