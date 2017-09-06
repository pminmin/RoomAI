#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPublicState
from roomai.sevenking import SevenKingPrivateState
from roomai.sevenking import SevenKingPersonState
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingPokerCard
from roomai.sevenking import AllSevenKingPatterns
from roomai.sevenking import AllSevenKingPokerCards
import random

import roomai.sevenking

logger = roomai.get_logger()

class SevenKingEnv(roomai.common.AbstractEnv):
    """
    """

    def init(self, params = dict()):
        """

        Args:
            params:

        Returns:

        """

        if "num_players" in params:
            self.num_players = params["num_players"]
        else:
            self.num_players = 3

        if "allcards" in params:
            allcards =  [c.__deepcopy__() for c in params["allcards"]]
        else:
            allcards =  [c.__deepcopy__() for c in AllSevenKingPokerCards.values()]
            random.shuffle(allcards)

        if "record_history" in params:
            self.record_history = params["record_history"]
        else:
            self.record_history = False




        self.public_state  = SevenKingPublicState()
        self.private_state = SevenKingPrivateState()
        self.person_states = [SevenKingPersonState() for i in range(self.num_players)]

        self.public_state_history  = []
        self.private_state_history = []
        self.person_states_history = []

        ## private_state
        self.private_state._SevenKingPrivateState__keep_cards = allcards

        for i in range(self.num_players):
            tmp = []
            for j in range(5):
                c = self.private_state._SevenKingPrivateState__keep_cards.pop()
                tmp.append(c)
            self.person_states[i]._SevenKingPersonState__add_cards(tmp)

        ## public_state
        self.public_state.turn,_          = self.choose_player_with_lowest_card()
        self.public_state.is_terminal     = False
        self.public_state.scores          = []
        self.public_state.previous_id     = None
        self.public_state.previous_action = None
        self.public_state._SevenKingPublicState__license_action  = SevenKingAction.lookup("")
        self.public_state._SevenKingPublicState__stage           = 0

        self.public_state._SevenKingPublicState__num_players     = self.num_players
        self.public_state._SevenKingPublicState__num_keep_cards  = len(self.private_state.keep_cards)
        self.public_state._SevenKingPublicState__num_hand_cards  = [len(person_state.hand_cards) for person_state in self.person_states]
        self.public_state._SevenKingPublicState__is_fold         = [False for i in range(self.public_state.num_players)]
        self.public_state._SevenKingPublicState__num_fold        = 0

        ## person_state
        for i in range(self.num_players):
            self.person_states[i].id         = i
            if i == self.public_state.turn:
                self.person_states[i].available_actions = SevenKingEnv.available_actions(self.public_state, self.person_states[i])

        self.__gen_history__()
        infos = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def forward(self, action):
        """

        Args:
            action:

        Returns:

        """
        pu   = self.public_state
        pr   = self.private_state
        pes  = self.person_states
        turn = pu.turn

        if self.is_action_valid(action,pu, pes[turn]) == False:
            raise  ValueError("The (%s) is an invalid action " % (action.key))

        ## the action plays its role
        if action.pattern[0] == "p_0":
            pu._SevenKingPublicState__is_fold[turn]           = True
            pu._SevenKingPublicState__num_fold               += 1
            pes[turn].available_actions = dict()
        else:
            pes[turn]._SevenKingPersonState__del_cards(action.cards)

            if pu.stage == 0:
                tmp = []
                for i in range(5 - len(pes[turn].hand_cards)):
                    c = pr._SevenKingPrivateState__keep_cards.pop()
                    tmp.append(c)
                pes[turn]._SevenKingPersonState__add_cards(tmp)
            elif pu.stage == 1:
                pu._SevenKingPublicState__num_hand_cards[turn] = len(pes[turn]._SevenKingPersonState__hand_cards)

            pes[turn].available_actions = dict()

        pu.previous_id     = turn
        pu.previous_action = action
        if action.pattern[0] != "p_0":
            pu._SevenKingPublicState__license_action = action



        #print (turn, "len_of_hand_card=",len(self.private_state.hand_cards[turn]), " len_of_keep_card=", len(self.private_state.keep_cards), " action = (%s)" %action.key,\
       #        " handcard1=%s"%(",".join([a.key for a in self.private_state.hand_cards[0]]))," handcard2=%s"%(",".join([a.key for a in self.private_state.hand_cards[1]])),\
         #      " num_fold =%d"%(self.public_state.num_fold),"fold=%s"%(",".join([str(s) for s in pu.is_fold])))
        ## termminal
        if self.public_state.stage == 1 and len(self.person_states[turn].hand_cards) == 0:
            pu.is_terminal    = True
            pu.scores         = self.compute_scores()
            new_turn          = None
            pu.turn           = new_turn
            pu._SevenKingPublicState__license_action = SevenKingAction.lookup("")

        ## stage 0 to 1
        elif len(self.private_state.keep_cards) < 5 and pu.stage == 0:
            new_turn, min_card              = self.choose_player_with_lowest_card()
            pu.turn                         = new_turn
            pu._SevenKingPublicState__num_fold                     = 0
            pu._SevenKingPublicState__is_fold                      = [False for i in range(pu.num_players)]
            pu._SevenKingPublicState__license_action               = SevenKingAction.lookup("")
            pes[new_turn].available_actions = SevenKingEnv.available_actions(pu, pes[new_turn])
            keys = pes[new_turn].available_actions.keys()
            for key in keys:
                if min_card.key not in key:
                    del pes[new_turn].available_actions[key]
            pu._SevenKingPublicState__stage                        = 1


        ## round next
        elif self.public_state.num_fold + 1 == pu.num_players:
            new_turn                                               = self.choose_player_with_nofold()
            pu.turn                                                = new_turn
            pu._SevenKingPublicState__num_fold                     = 0
            pu._SevenKingPublicState__is_fold                      = [False for i in range(pu.num_players)]
            pu._SevenKingPublicState__license_action               = SevenKingAction.lookup("")
            pes[new_turn].available_actions = SevenKingEnv.available_actions(pu, pes[new_turn])


        else:
            new_turn                        = (turn + 1) % pu.num_players
            pu.turn                         = new_turn
            pes[new_turn].available_actions = SevenKingEnv.available_actions(pu, pes[new_turn])



        self.__gen_history__()
        infos = self.__gen_infos__()
        return infos, self.public_state, self.person_states, self.private_state

    def compute_scores(self):
        """

        Returns:

        """
        scores                         = [-1 for i in range(self.num_players)]
        scores[self.public_state.turn] = self.num_players -1
        return scores

    def choose_player_with_nofold(self):
        """

        Returns:

        """
        for player_id in range(self.public_state.num_players):
            if self.public_state.is_fold[player_id]== False:
                return player_id



    def choose_player_with_lowest_card(self):
        """

        Returns:

        """
        min_card    = self.person_states[0].hand_cards[0]
        min_playerid = 0
        for playerid in range(self.num_players):
            for c in self.person_states[playerid].hand_cards:
                if SevenKingPokerCard.compare(min_card, c) > 0:
                    min_card     = c
                    min_playerid = playerid
        return min_playerid, min_card

    ######################## Utils function ###################
    @classmethod
    def compete(cls, env, players):
        """

        Args:
            env:
            players:

        Returns:

        """

        num_players = len(players)
        infos, public_state, person_states, private_state = env.init({"num_players":num_players})
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
    def is_action_valid(self, action, public_state, person_state):
        """

        Args:
            action:
            public_state:
            person_state:

        Returns:

        """
        return action.key in person_state.available_actions



    ########################### about gen_available_actions ########################

    @classmethod
    def available_actions(cls, public_state, person_state):
        """

        Args:
            public_state:
            person_state:

        Returns:

        """
        available_actions = dict()

        license_action = public_state.license_action
        if license_action is None:
            license_action = SevenKingAction("")
        hand_cards = person_state.hand_cards


        patterns = set()
        if license_action.pattern[0] == "p_0":
            for p in AllSevenKingPatterns.values():
                if p[0] != "p_0":
                    patterns.add(p)
        else:
            patterns.add(license_action.pattern)
            patterns.add(AllSevenKingPatterns["p_0"])

        for pattern in patterns:

                if pattern[1] >= 2:
                    point2cards = person_state._SevenKingPersonState__gen_pointrank2cards()

                if len(person_state.hand_cards) < pattern[1]:
                    continue

                elif pattern[0] == "p_0":
                    available_actions[""] = SevenKingAction.lookup("")


                elif pattern[0] == "p_1":
                    for c in person_state.hand_cards:
                        available_actions[c.key] = (SevenKingAction.lookup(c.key))

                elif pattern[0] == "p_2":
                    for p in point2cards:

                        license_pattern = license_action.pattern
                        license_card    = None
                        if license_pattern[0] != "p_0":
                            #print license_action.key, license_action.pattern, license_pattern[0] != "p_0"
                            license_card    = license_action.cards[-1]
                        len1 = len(point2cards[p])

                        if len1 == 2:
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][1],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][1].key)
                                available_actions[str] = SevenKingAction.lookup(str)

                        if len1 == 3:
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][1],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][1].key)
                                available_actions[str] = (SevenKingAction.lookup(str))

                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][2],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                                str = "%s,%s" % (point2cards[p][1].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))

                        if len1 == 4:
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][1],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][1].key)
                                available_actions[str] = (SevenKingAction.lookup(str))

                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][2],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                                str = "%s,%s" % (point2cards[p][1].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][3],
                                                                                      license_card) > 0:
                                str = "%s,%s" % (point2cards[p][0].key, point2cards[p][3].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                                str = "%s,%s" % (point2cards[p][1].key, point2cards[p][3].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                                str = "%s,%s" % (point2cards[p][2].key, point2cards[p][3].key)
                                available_actions[str] = (SevenKingAction.lookup(str))


                elif pattern[0] == "p_3":
                    for p in point2cards:

                        license_pattern = license_action.pattern
                        license_card    = None
                        if license_pattern[0] != "p_0" :
                            license_card    = license_action.cards[-1]
                        len1 = len(point2cards[p])

                        if len1 == 3:
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][2],
                                                                                      license_card) > 0:
                                str = "%s,%s,%s" % (point2cards[p][0].key, point2cards[p][1].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                        if len1 == 4:

                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][2],
                                                                                      license_card) > 0:
                                str = "%s,%s,%s" % (point2cards[p][0].key, point2cards[p][1].key, point2cards[p][2].key)
                                available_actions[str] = (SevenKingAction.lookup(str))
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][3],
                                                                                      license_card) > 0:
                                str = "%s,%s,%s" % (point2cards[p][0].key, point2cards[p][1].key, point2cards[p][3].key)
                                available_actions[str]=(SevenKingAction.lookup(str))
                                str = "%s,%s,%s" % (point2cards[p][0].key, point2cards[p][2].key, point2cards[p][3].key)
                                available_actions[str]=(SevenKingAction.lookup(str))
                                str = "%s,%s,%s" % (point2cards[p][1].key, point2cards[p][2].key, point2cards[p][3].key)
                                available_actions[str]=(SevenKingAction.lookup(str))

                elif pattern[0] == "p_4":
                    for p in point2cards:
                        license_pattern = license_action.pattern
                        license_card    = None
                        if license_pattern[0] != "p_0" :
                            license_card    = license_action.cards[-1]
                        len1 = len(point2cards[p])

                        if len1 >= 4:
                            if license_pattern[0] == "p_0" or SevenKingPokerCard.compare(point2cards[p][3],
                                                                                  license_card) > 0:
                                str = "%s,%s,%s,%s" % (
                                    point2cards[p][0].key,
                                    point2cards[p][1].key,
                                    point2cards[p][2].key,
                                    point2cards[p][3].key
                                )
                                available_actions[str]=(SevenKingAction.lookup(str))

                if pattern[0] != "p_0" and pattern[0] != "p_1" and\
                   pattern[0] != "p_2" and pattern[0] != "p_3" and pattern[0] != "p_4":
                    raise ValueError("The %s pattern is invalid" % (pattern[0]))


        #for a in available_actions.values():
        #    if SevenKingEnv.__is_action_valid__(a,public_state,person_state) == False:
        #        del available_actions[a.key]

        return available_actions

