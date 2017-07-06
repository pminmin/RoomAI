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
###numCards
AllPatterns["p_0"] = ("p_0",0) ## check
AllPatterns["p_1"] = ("p_1",1)
AllPatterns["p_2"] = ("p_2",2)
AllPatterns["p_3"] = ("p_3",3)
AllPatterns["p_4"] = ("p_4",4)

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
        self.public_state.stage           = 0

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
        pu   = self.public_state
        pr   = self.private_state
        pes  = self.person_states
        turn = pu.turn

        if SevenKingEnv.is_action_valid(action, pu, pes[turn]) == False:
            raise  ValueError("The %s is an invalid action "%(action.get_key()))

        ## the action plays its role
        if action.pattern[0] == "p_0":
            pu.is_check[turn]           = True
            pu.num_check               -= 1
            pes[turn].available_actions = dict()
        else:
            action_key_tmp  = dict([(c.get_key(),None) for c in action.cards])
            cards_tmp       = pr.hand_cards[turn]

            pr.hand_cards[turn] = []
            for c in cards_tmp:
                if c.get_key() not in action_key_tmp:
                    pr.hand_cards[turn].append(c)

            if pu.stage == 0:
                for i in range(5 - len(pr.hand_cards[turn])):
                    c = pr.keep_cards[-1]
                    pr.keep_cards = pr.keep_cards.pop()
                    pr.hand_cards[turn].append(c)

            pes[turn].hand_card         = [c.__deepcopy__() for c in pr.hand_cards[turn]]
            pes[turn].available_actions = dict()

        pu.previous_id     = turn
        pu.previous_action = action.__deepcopy__()


        ## termminal
        if self.public_state.stage == 1 and len(self.private_state.hand_cards[turn]) == 0:
            pu.is_terminal = True
            pu.scores      = self.compute_scores()
            new_turn       = None
            pu.turn        = new_turn

        ## stage 0 to 1
        elif len(self.private_state.keep_cards) < 5:
            new_turn                        = self.choose_player_with_lowest_card()
            pu.turn                         = new_turn
            pu.num_check                    = 0
            pu.is_check                     = [False for i in range(pu.num_players)]
            pes[new_turn].available_actions = SevenKingEnv.available_actions(pu, pes[new_turn])
            pu.stage                        = 1

        ## round next
        elif self.public_state.num_check + 1 == pu.num_players:
            new_turn                        = self.choose_player_with_lowest_card()
            pu.turn                         = new_turn
            pu.num_check                    = 0
            pu.is_check                     = [False for i in range(pu.num_players)]
            pes[new_turn].available_actions = SevenKingEnv.available_actions(pu, pes[new_turn])

        else:
            new_turn                        = (turn + 1) % pu.num_players
            pes[new_turn].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[new_turn])


        self.__gen_history__()
        infos = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def compute_scores(self):
        scores                         = [-1 for i in range(self.num_players)]
        scores[self.public_state.turn] = self.num_players -1
        return scores

    def choose_player_with_lowest_card(self):
        min_cards    = self.private_state.hand_cards[0][0]
        min_playerid = 0
        for playerid in range(self.num_players):
            for c in self.private_state.hand_cards:
                if SevenKingPokerCard.compare(min_cards, c) < 0:
                    min_cards    = c
                    min_playerid = playerid
        return min_playerid

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
        ###numCards
        num_cards  = len(action.cards)
        return AllPatterns["p_%d"%(num_cards)]


    @classmethod
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
        if previous_action.pattern[0] != "p_0" and previous_action.pattern[0] != action.pattern[0]:
            return False

        ## large
        if previous_action.pattern[0] != "p_0":
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
        res = dict()

        if len(hand_cards) < pattern[1]:
            return res
        if pattern[0] == "p_0":
            return res

        point2cards = dict()
        for c in hand_cards:
            point = c.get_point_rank()
            if point not in point2cards:
                point2cards[point] = []
            point2cards[point].append(c.__deepcopy__())

        if pattern[0] == "p_1":
            pass
        elif pattern[0] == "p_2":
            pass
        elif pattern[0] == "p_3":
            pass
        elif pattern[0] == "p_4":
            pass
        else:
            raise ValueError("The %s pattern is invalid"%(pattern[0]))

        return res

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

