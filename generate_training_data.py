#!/bin/python
import roomai.doudizhu


def str2action(str1):
     

def handcard2str(hand_card):
    str1 = ""
    for i in xrange(len(hand_card.cards))
        str1 += "%d:%d,"%(i, hand_card.cards[i])
    return str1    

def action2str(action):
    str1 = ""
    for i in action.masterCards:
        str1 += "%d,"%i
    for i in action.slaveCards:
        str1 += "%d,"%i
    return str1

def generate_data(str1, env, actions, num):
    ## num = 3 * n //landlord's turn
    for i in xrange(num):
        action = actions[i]
        env.forward(action)
   
    turn            = env.public_state.turn
    if turn != 0:
        print "error"
        return ""
     
    hand_cards          = env.private_state.hand_cards
    license_action      = env.public_state.license_action
    candidates          = roomai.doudizhu.Utils.candidate_actions(env.private_state.hand_cards[turn]
    choose_action_id    = actions[num].idx     

    
    base_str = ""
    base_str += handcard2str(hand_cards[0]) + "\t"
    base_str += handcard2str(hand_cards[1]) + "\t"
    base_str += handcard2str(hand_cards[2]) + "\t"
    base_str += action2str(license_action) + "\t"

    str1 = ""
    for i in xrange(5):
        str1 += base_str
        str1 += action2str(candidates[int(random.random() * len(candidates))]) + "\t0\n"

    str1 += base_str
    str1 += action2str(actions[num]) + "\t1\n"

    return str1 
 
