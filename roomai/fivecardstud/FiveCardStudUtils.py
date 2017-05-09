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


class FiveCardStudPokerCard(roomai.abstract.PokerCard):
    def get_point_rank(self):
        return self.point
    def get_suit_rank(self):
        suit_str_to_rank = {'Spade': 3, 'Heart': 2, 'Club': 1, 'Diamond':0}
        return suit_str_to_rank[self.suit_str]

    @classmethod
    def compare(cls, pokercard1, pokercard2):
        pr1 = pokercard1.get_point_rank()
        pr2 = pokercard1.get_point_rank()
        if pr1 != pr2:
            return pr1-pr2
        else:
            return pokercard1.get_suit_rank() - pokercard2.get_suit_rank()






