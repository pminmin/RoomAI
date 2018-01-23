#!/bin/python
import roomai.common

def Pass(pu, pr, pes, action): #p1
  turn = pu.__turn__
  previous_action = pu.__previous_action__
  if previous_action.skill.skill_name in ["Slash","JueDou","NanManRuQin","WanJianQiFa"]:
    pu.__state__[turn]['hp'] -= 1
    if pu.__state__[turn]['hp'] == 0:
      pu.__state__[turn]['alive'] = 0 # if another has a Dodge ?
  return pu, pr, pes

def Slash(pu, pr, pes, action): #p3
  turn = pu.__turn__
  pes[turn].__del_cards__(action.card)

  pu.__previous_id__ = turn
  pu.__previous_action__ = action
  pu.__num_hand_cards__ = pu.__num_hand_cards__ - 1

  pu.__turn__ = action.targets[0]
  return pu, pr, pes



