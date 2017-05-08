#!/bin/python
import roomai.abstract


                                                    #0     1           2       3           4                                    5
                                                    #name, isStraight, isSameSuit, isNumRelated, [SizeOfPair1, SizeOfPair2,..](desc), rank
AllCardsPattern_FiveCardStud = dict()
AllCardsPattern_FiveCardStud["Straight_SameSuit"] = ["Straight_SameSuit", True, True, False, [], 100]
AllCardsPattern_FiveCardStud["4_1"]               = ["4_1", False, False, True, [4, 1], 98]
AllCardsPattern_FiveCardStud["3_2"]               = ["3_2", False, False, True, [3, 2], 97]
AllCardsPattern_FiveCardStud["SameSuit"]          = ["SameSuit", False, True, False, [], 96]
AllCardsPattern_FiveCardStud["Straight_DiffSuit"] = ["Straight_DiffSuit", True, False, False, [], 95]
AllCardsPattern_FiveCardStud["3_1_1"]             = ["3_1_1", False, False, True, [3, 1, 1], 94]
AllCardsPattern_FiveCardStud["2_2_1"]             = ["2_2_1", False, False, True, [2, 2, 1], 93]
AllCardsPattern_FiveCardStud["2_1_1_1"]           = ["2_1_1_1", False, False, True, [2, 1, 1, 1], 92]
AllCardsPattern_FiveCardStud["1_1_1_1_1"]         = ["1_1_1_1_1", False, False, True, [1, 1, 1, 1, 1], 91]

point_str_to_key_fivecardstud  = {'2':0, '3':1, '4':2, '5':3, '6':4, '7':5, '8':6, '9':7, 'T':8, 'J':9, 'Q':10, 'K':11, 'A':12}
point_key_to_str_fivecardstud  = {0: '2', 1: '3', 2: '4', 3: '5', 4: '6', 5: '7', 6: '8', 7: '9', 8: 'T', 9: 'J', 10: 'Q', 11: 'K', 12: 'A'}
suit_key_to_str_fivecardstud   = {0: 'Spade', 1: 'Heart', 2: 'Diamond', 3: 'Club'}
suit_str_to_key_fivecardstud   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3}
class Card_FiveCardStud:
    def __init__(self, point, suit):
        point1 = point
        if isinstance(point, str):
            point1 = point_str_to_key_fivecardstud[point]
        suit1  = suit
        if isinstance(suit, str):
            suit1 = suit_str_to_key_fivecardstud[suit]

        self.point  = point1
        self.suit   = suit1
        self.String = "%s_%s"%(point_key_to_str_fivecardstud[point1], suit_key_to_str_fivecardstud[suit1])

    def toString(self):
        return self.String

class Utils_FiveCardStud:
    @classmethod
    def available_actions(cls, public_state):
        pass

    @classmethod
    def compare_cards(cls, c1, c2):
        if c1.point != c2.point:
            return c1.point - c2.point
        else:
            return c1.suit  - c2.suit

    @classmethod
    def cards2pattern(cls, cards):
        point2cards = dict()
        for c in cards:
            if c.point in point2cards:
                point2cards[c.point].append(c)
            else:
                point2cards[c.point] = [c]
        for p in point2cards:
            point2cards[p].sort(Utils_FiveCardStud.compare_cards)

        suit2cards = dict()
        for c in cards:
            if c.suit in suit2cards:
                suit2cards[c.suit].append(c)
            else:
                suit2cards[c.suit] = [c]
        for s in suit2cards:
            suit2cards[s].sort(Utils_FiveCardStud.compare_cards)

        num2point = [[], [], [], [], []]
        for p in point2cards:
            num = len(point2cards[p])
            num2point[num].append(p)
        for i in xrange(5):
            num2point[num].sort()

        sorted_point = []
        for p in point2cards:
            sorted_point.append(p)
        sorted_point.sort()

        ##straight_samesuit
        for s in suit2cards:
            if len(suit2cards[s]) >= 5:
                numStraight = 1
                for i in xrange(len(suit2cards[s]) - 2, -1, -1):
                    if suit2cards[s][i].point == suit2cards[s][i + 1].point - 1:
                        numStraight += 1
                    else:
                        numStraight = 1

                    if numStraight == 5:
                        pattern = AllCardsPattern_FiveCardStud["Straight_SameSuit"]
                        return pattern

        ##4_1
        if len(num2point[4]) ==1:
            pattern = AllCardsPattern_FiveCardStud["4_1"]
            return pattern

        ##3_2
        if len(num2point[3]) == 1 and len(num2point[2]) == 1:
            pattern = AllCardsPattern_FiveCardStud["3_2"]
            return pattern

        ##SameSuit
        for s in suit2cards:
            if len(suit2cards[s]) >= 5:
                pattern = AllCardsPattern_FiveCardStud["SameSuit"]
                return pattern

        ##Straight_DiffSuit
        numStraight = 1
        for idx in xrange(len(sorted_point) - 2, -1, -1):
            if sorted_point[idx] + 1 == sorted_point[idx]:
                numStraight += 1
            else:
                numStraight = 1

            if numStraight == 5:
                pattern = AllCardsPattern_FiveCardStud["Straight_DiffSuit"]
                for p in xrange(idx, idx + 5):
                    point = sorted_point[p]
                return pattern

        ##3_1_1
        if len(num2point[3]) == 1:
            pattern = AllCardsPattern_FiveCardStud["3_1_1"]
            return pattern

        ##2_2_1
        if len(num2point[2]) >= 2:
            pattern = AllCardsPattern_FiveCardStud["2_2_1"]
            return pattern

        ##2_1_1_1
        if len(num2point[2]) == 1:
            pattern = AllCardsPattern_FiveCardStud["2_1_1_1"]
            return pattern

        ##1_1_1_1_1
        return AllCardsPattern_FiveCardStud["1_1_1_1_1"]





