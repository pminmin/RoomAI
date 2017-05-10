#!/bin/python
import roomai.abstract
import copy
import logging
import random


from FiveCardStudUtils import FiveCardStudPokerCard
from FiveCardStudInfo import FiveCardStudPublicState
from FiveCardStudInfo import FiveCardStudPersonState
from FiveCardStudInfo import FiveCardStudPrivateState
from FiveCardStudInfo import FiveCardStudInfo
from FiveCardStudAction import FiveCardStudAction

class FiveCardStudEnv(roomai.abstract.AbstractEnv):
    def __init__(self):
        self.logger         = roomai.get_logger()
        self.num_players    = 3
        self.chips          = [1000 for i in xrange(self.num_players)]
        self.min_bet        = 10

    def gen_infos(self):
        infos = [FiveCardStudInfo() for i in xrange(self.public_state.num_players)]
        for i in xrange(self.public_state.num_players):
            infos[i].person_state = copy.deepcopy(self.person_states[i])
            infos[i].public_state = copy.deepcopy(self.public_state)

        return infos

    #@override
    def init(self):
        self.public_state   = FiveCardStudPublicState()
        self.private_state  = FiveCardStudPrivateState()
        self.person_states  = [FiveCardStudPersonState for i in xrange(3)]
        for i in xrange(self.num_players):
            self.person_states[i].id = i

        ## initialize the cards
        allcards = []
        for i in xrange(13):
            for j in xrange(4):
                allcards.append(FiveCardStudPokerCard(i, j))
        random.shuffle(allcards)

        ## private_state
        self.private_state.all_hand_cards    = allcards

        ## public_state
        self.public_state.num_players        = self.num_players
        self.public_state.second_hand_cards  = self.private_state.all_hand_cards[1*self.num_players]
        self.public_state.turn               = int(random.random() * self.public_state.num_players)


        ## person_state
        for i in xrange(self.num_players):
            self.person_states[i].first_hand_card  = self.private_state.all_hand_cards[i]
        turn = self.public_state.turn
        self.person_states[turn].available_actions = FiveCardStudEnv.available_actions(self.public_state)


        return False,[],self.gen_infos(), self.public_state, self.person_states, self.private_state



    #@override
    def forward(self, action):
        '''
        :param action: 
        :except: throw ValueError when the action is invalid at this time 
        '''

        if not FiveCardStudEnv.is_action_valid(self.public_state, action):
            self.logger.critical("action=%s is invalid" % (action.get_key()))
            raise ValueError("action=%s is invalid" % (action.get_key()))

        isTerminal = False
        scores = []
        infos = []
        pu = self.public_state
        pe = self.person_states
        pr = self.private_state

        if action.option == FiveCardStudAction.Fold:
            self.action_fold(action)
        elif action.option == FiveCardStudAction.Check:
            self.action_check(action)
        elif action.option == FiveCardStudAction.Call:
            self.action_call(action)
        elif action.option == FiveCardStudAction.Raise:
            self.action_raise(action)
        elif action.option == FiveCardStudAction.AllIn:
            self.action_allin(action)
        else:
            raise Exception("action.option(%s) not in [Fold, Check, Call, Raise, AllIn]" % (action.option))
        pu.previous_id = pu.turn
        pu.previous_action = action
        pu.turn = self.next_player(pu.turn)

        # computing_score
        if FiveCardStudEnv.is_compute_score(self.public_state):
            isTerminal = True
            scores = self.compute_score()
            ## need showdown
            if pu.num_quit + 1 < pu.num_players:
                pu.public_cards = pr.keep_cards[0:5]

        # enter into the next stage
        elif FiveCardStudEnv.is_nextround(self.public_state):
            add_cards = []
            if pu.round == 1:   add_cards = pr.keep_cards[0:3]
            if pu.round == 2:   add_cards = [pr.keep_cards[3]]
            if pu.round == 3:   add_cards = [pr.keep_cards[4]]


            pu.public_cards.extend(add_cards)
            pu.round = pu.round + 1
            pu.turn  = FiveCardStudEnv.choose_player_at_begining_of_round(pu)
            pu.is_needed_to_action = [True for i in xrange(pu.num_players)]
            pu.num_needed_to_action = self.public_state.num_players

        self.person_states[self.public_state.previous_id].available_actions = None
        self.person_states[self.public_state.turn].available_actions = self.available_actions(self.public_state)
        infos = self.gen_infos()

        if self.logger.level <= logging.DEBUG:
            self.logger.debug("FiveCardStudEnv.forward: num_quit+num_allin = %d+%d = %d, action = %s, stage = %d" % ( \
                self.public_state.num_quit, \
                self.public_state.num_allin, \
                self.public_state.num_quit + self.public_state.num_allin, \
                action.get_key(), \
                self.public_state.stage \
                ))

        return isTerminal, scores, infos, self.public_state, self.person_states, self.private_state

    #@override
    def compete(cls, env, players):
        total_scores = [0 for i in xrange(len(players))]
        count = 0

        ## the first match
        env.chips = [5000 for i in xrange(len(players))]
        env.num_players = len(players)
        env.dealer_id = int(random.random * len(players))
        env.big_blind_bet = 100

        isTerminal, _, infos, public, persons, private = env.init()
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])
        while isTerminal == False:
            turn = public.turn
            action = players[turn].take_action()
            isTerminal, scores, infos, public, persons, private = env.forward(action)
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

        for i in xrange(len(players)):  total_scores[i] += scores[i]
        count += 1

        ## the following matches
        while True:
            dealer = (env.public_state.dealer_id + 1) % len(players)
            while env.public_state.chips[dealer] == 0:
                dealer = (env.public_state.dealer_id + 1) % len(players)
            next_players_id = []  ## the available players (who still have bets) for the next match
            next_chips = []
            next_dealer_id = -1
            for i in xrange(len(env.public_state.chips)):
                if env.public_state.chips[i] > 0:
                    next_players_id.append(i)
                    next_chips.append(env.public_state.chips[i])
                    if i == dealer: next_dealer_id = len(next_players_id) - 1

            if len(next_players_id) == 1: break;

            if count % 10 == 0:
                env.big_blind_bet = env.big_blind_bet + 100
            env.chips = next_chips
            env.dealer_id = next_dealer_id
            env.num_players = len(next_players_id)

            isTerminal, scores, infos, public, persons, private = env.init()
            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                players[idx].receive_info(infos[i])
            while isTerminal == False:
                turn = public.turn
                idx = next_players_id[turn]
                action = players[idx].take_action()
                isTerminal, scores, infos, public, persons, private = env.forward(action)
                for i in xrange(len(next_players_id)):
                    idx = next_players_id[i]
                    players[idx].receive_info(infos[i])

            for i in xrange(len(next_players_id)):
                idx = next_players_id[i]
                total_scores[idx] += scores[i]
            count += 1

        for i in xrange(len(players)): total_scores[i] /= count * 1.0
        return total_scores;


    def action_fold(self, action):
        pu = self.public_state
        pu.is_quit[pu.turn] = True
        pu.num_quit += 1

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_check(self, action):
        pu = self.public_state
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_call(self, action):
        pu = self.public_state
        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1

    def action_raise(self, action):
        pu = self.public_state

        pu.raise_account   = action.price + pu.bets[pu.turn] - pu.max_bet
        pu.chips[pu.turn] -= action.price
        pu.bets[pu.turn]  += action.price
        pu.max_bet         = pu.bets[pu.turn]

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        p = (pu.turn + 1)%pu.num_players
        while p != pu.turn:
            if pu.is_allin[p] == False and pu.is_quit[p] == False and pu.is_needed_to_action[p] == False:
                pu.num_needed_to_action   += 1
                pu.is_needed_to_action[p]  = True
            p = (p + 1) % pu.num_players


    def action_allin(self, action):
        pu = self.public_state

        pu.is_allin[pu.turn]   = True
        pu.num_allin          += 1

        pu.bets[pu.turn]      += action.price
        pu.chips[pu.turn]      = 0

        pu.is_needed_to_action[pu.turn] = False
        pu.num_needed_to_action        -= 1
        if pu.bets[pu.turn] > pu.max_bet:
            pu.max_bet = pu.bets[pu.turn]
            p = (pu.turn + 1) % pu.num_players
            while p != pu.turn:
                if pu.is_allin[p] == False and pu.is_quit[p] == False and pu.is_needed_to_action[p] == False:
                    pu.num_needed_to_action  += 1
                    pu.is_needed_to_action[p] = True
                p = (p + 1) % pu.num_players

############################################# Utils Function ######################################################
    @classmethod
    def choose_player_at_begining_of_round(cls, public_state):
        pass

    @classmethod
    def next_player(self, pu):
        i = pu.turn
        if pu.num_needed_to_action == 0:
            return -1

        p = (i+1)%pu.num_players
        while pu.is_needed_to_action[p] == False:
            p = (p+1)%pu.num_players
        return p

    @classmethod
    def is_action_valid(cls, public_state, action):
        pass

    @classmethod
    def available_actions(cls, public_state):
        pass

    @classmethod
    def is_nextround(self, public_state):
        '''
        :return: 
        A boolean variable indicates whether is it time to enter the next stage
        '''
        return public_state.num_needed_to_action == 0

    @classmethod
    def compare_cards(cls, cards1, cards2):
        if len(cards1) == len(cards2) and len(cards1) == 4:
            pattern1 = cls.fourcards2pattern(cards1)
            pattern2 = cls.fourcards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(FiveCardStudPokerCard.compare)
                cards2.sort(FiveCardStudPokerCard.compare)
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        elif len(cards1) == len(cards2) and len(cards1) == 5:
            pattern1 = cls.cards2pattern(cards1)
            pattern2 = cls.cards2pattern(cards2)
            if pattern1[5] != pattern2[5]:
                return pattern1[5] - pattern2[5]
            else:
                cards1.sort(FiveCardStudPokerCard.compare)
                cards2.sort(FiveCardStudPokerCard.compare)
                return FiveCardStudPokerCard.compare(cards1[-1], cards2[-1])

        else:
            raise  ValueError("len(cards1)%d, and len(cards2)%d are invalid "%(len(cards1),len(cards2)))

    @classmethod
    def cards2pattern(cls, cards):
        pointrank2cards = dict()
        for c in cards:
            if c.get_point_rank() in pointrank2cards:
                pointrank2cards[c.get_point_rank()].append(c)
            else:
                pointrank2cards[c.get_point_rank()] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(FiveCardStudPokerCard.compare_cards)

        suitrank2cards = dict()
        for c in cards:
            if c.get_suit_rank() in suitrank2cards:
                suitrank2cards[c.get_suit_rank()].append(c)
            else:
                suitrank2cards[c.get_suit_rank()] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(FiveCardStudPokerCard.compare_cards)

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in xrange(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point == suitrank2cards[s][i + 1].point - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) ==1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["4_1"]
            return pattern

        ##3_2
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_pointrank[p]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern =  roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return  roomai.fivecardstud.AllCardsPattern_FiveCardStud["1_1_1_1_1"]

    @classmethod
    def fourcards2pattern(cls, cards):
        pointrank2cards = dict()
        for c in cards:
            if c.get_point_rank() in pointrank2cards:
                pointrank2cards[c.get_point_rank()].append(c)
            else:
                pointrank2cards[c.get_point_rank()] = [c]
        for p in pointrank2cards:
            pointrank2cards[p].sort(FiveCardStudPokerCard.compare_cards)

        suitrank2cards = dict()
        for c in cards:
            if c.get_suit_rank() in suitrank2cards:
                suitrank2cards[c.get_suit_rank()].append(c)
            else:
                suitrank2cards[c.get_suit_rank()] = [c]
        for s in suitrank2cards:
            suitrank2cards[s].sort(FiveCardStudPokerCard.compare_cards)

        num2pointrank = [[], [], [], [], []]
        for p in pointrank2cards:
            num = len(pointrank2cards[p])
            num2pointrank[num].append(p)
        for i in xrange(5):
            num2pointrank[num].sort()

        sorted_pointrank = []
        for p in pointrank2cards:
            sorted_pointrank.append(p)
        sorted_pointrank.sort()

        ##straight_samesuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suitrank2cards[s]) - 2, -1, -1):
                    if suitrank2cards[s][i].point == suitrank2cards[s][i + 1].point - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2pointrank[4]) == 1:
            pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["4_1"]
            return pattern

        ##3_2
        if len(num2pointrank[3]) == 1 and len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_2"]
            return pattern

        ##SameSuit
        for s in suitrank2cards:
            if len(suitrank2cards[s]) >= 5:
                pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_pointrank) - 2, -1, -1):
            if sorted_pointrank[idx] + 1 == sorted_pointrank[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_pointrank[p]
                return pattern

        ##3_1_1
        if len(num2pointrank[3]) == 1:
            pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2pointrank[2]) >= 2:
            pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2pointrank[2]) == 1:
            pattern = roomai.fivecardstud.AllCardsPattern_FiveCardStud["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return roomai.fivecardstud.AllCardsPattern_FiveCardStud["1_1_1_1_1"]