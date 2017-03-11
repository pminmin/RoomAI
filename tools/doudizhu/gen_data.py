#!/bin/python
import sys
sys.path.append(".")
from roomai.doudizhu import *

print "start"
actions_file            = open("actions.txt","w")

cards = []
for i in xrange(13):
    for j in xrange(4):
       cards.append(i)
cards.append(13)
cards.append(14)
hand_cards = HandCards(cards)

env = DouDiZhuPokerEnv()
env.init([None,None,None])
env.public_state.is_response = False
env.public_state.phase       = PhaseSpace.play

actions = Utils.candidate_actions(hand_cards, env.public_state)
for a in actions:
    print a.masterCards, a.slaveCards
    sys.stdout.flush()

    mStr = ""
    for c in a.masterCards:
        mStr += "%d,"%(c)
    sStr = ""
    for c in a.slaveCards:
        sStr += "%d,"%(c)
    actions_file.write("%s\t%s\n"%(mStr,sStr))

print len(actions)
actions_file.close()
print "end"
