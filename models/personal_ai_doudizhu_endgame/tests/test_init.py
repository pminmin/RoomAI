#!/bin/python
import doudizhu_endgame
import unittest

class TestIO(unittest.TestCase):

    def testIO(self):
        for i in xrange(1,101):
            f = open("data/endgame.txt")
            for line in f:
                lines = line.strip().split("\t")
                if int(lines[0]) == i:
                    cards = lines[1]
                    break
            f.close()

            f = open("data/%d_give_hand.txt"%(i))
            responses = []
            for line in f:
                responses.append(line.strip())
            f.close()
            hand_cards, opponent_cards, opponent_player =doudizhu_endgame.build_endgame(cards=cards, responses = responses)
            hand_cards1, opponent_cards1, opponent_player1 =doudizhu_endgame.build_endgame(cards=cards, responses = responses)
            scores = doudizhu_endgame.run_endgame(opponent_player1, opponent_player,hand_cards,opponent_cards)
            print scores
