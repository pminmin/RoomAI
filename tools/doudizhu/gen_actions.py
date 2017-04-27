#!/bin/python
import sys
sys.path.append(".")
from roomai.doudizhu import *

print "start"
actions_file            = open("actions.py","w")

cards = []
for i in xrange(13):
    for j in xrange(4):
       cards.append(i)
cards.append(13)
cards.append(14)
hand_cards = HandCards(cards)

env = DouDiZhuPokerEnv()
env.init()
env.public_state.is_response = False
env.public_state.phase       = PhaseSpace.play

actions = Utils_DouDiZhu.candidate_actions(hand_cards, env.public_state)
line, action = Utils_DouDiZhu.lookup_action([ActionSpace_DouDiZhu.cheat], [])
actions[line] = action
line, action = Utils_DouDiZhu.lookup_action([ActionSpace_DouDiZhu.bid], [])
actions[line] = action

res = dict()

for key in actions:
    a = actions[key]
    if a.pattern[0] != "i_invalid":
        res[key] = a

for key in res:
    a = actions[key]

    mStr = ""
    for c in a.masterCards:
        mStr += "%d,"%(c)
    sStr = ""
    for c in a.slaveCards:
        sStr += "%d,"%(c)
    actions_file.write("%s\t%s\n"%(mStr,sStr))

actions_file.close()
