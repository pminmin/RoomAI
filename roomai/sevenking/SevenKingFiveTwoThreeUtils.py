#!/bin/python
import roomai.common

point_str_to_rank  = {'7':14, 'R':13, 'r':12, '5':11,  '2':10,  '3':9,  '1':8,  'K':7,\
                      'Q':6,  'J':5,   'T':4,   '9':3,   '8':2,   '6':1,   '4':0}
point_rank_to_str  = {14:'7', 13:'R', 12:'r',  11:'5', 10:'2',  9:'3',  8:'1',   7:'K',\
                       6:'Q',  5:'J',   4:'T',   3:'9',   2:'8',   1:'6',  0:'4'}
suit_str_to_rank   = {'Spade':0, 'Heart':1, 'Diamond':2, 'Club':3,  'ForKing':4}
suit_rank_to_str   = {0:'Spade', 1: 'Heart', 2: 'Diamond', 3:'Club', 4:'ForKing'}

class SevenKingFiveTwoThreePokerCard(roomai.common.PokerCard):

    def get_point_rank(self):
        return point_str_to_rank[self.point_str]

    def get_suit_rank(self):
        return suit_str_to_rank[self.suit_str]

    def __deepcopy__(self, memodict={}):
        copyinstance = SevenKingFiveTwoThreePokerCard(self.point_str, self.suit_str)
        return copyinstance
