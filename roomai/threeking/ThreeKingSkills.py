#!/bin/python
import roomai.common

class ThreeKingSkills():
  def __init__(self, pu, pr, pes, action):
    self.pu = pu
    self.pr = pr
    self.pes = pes
    self.action = action

    self.turn = self.pu.__turn__
    self.previous_action = self.pu.__previous_action__
    self.previous_id = self.pu.__previous_id__

    #【过牌】
    def Pass(): #p1 
      if self.previous_action.skill.skill_name in ["Slash","JueDou","NanManRuQin","WanJianQiFa"]:
        targets = self.previous_action.targets
        # 黑色杀对装备有【仁王盾】的玩家无效
        if self.previous_action.skill.skill_name == "Slash" and self.previous_action.card.suit == "spade" \
        and "RenWangDun" in self.pu.__equipment_cards__[targets[0]]:
          return self.pu, self.pr, self.pes
        self.pu.__state__[self.turn]['hp'] -= 1
        self.pu.turn = self.previous_id
        if self.pu.__state__[self.turn]['hp'] == 0:
          self.pu.__state__[self.turn]['alive'] = 0 # if another has a Peach ?

      return self.pu, self.pr, self.pes

    # 【摸牌】
    def Get():
      card = self.action.card # number=2
      tmp = []
      for c in card.split(','):
        self.pr.pop(c)
        tmp.append(c)

        if c.type == "ZhuangBei":
          self.pu.equipment_cards[self.turn].append(c)

      self.pes[self.turn].__add_cards__(tmp)

      return self.pu, self.pr, self.pes

    #【闪】
    def Dodge():
      return self.pu, self.pr, self.pes

    #【出装备】
    def Equip():
      card = self.action.card
      self.pu.__equipment_cards__.append(card)
      self.pu.__num_equipment_cards__ += 1
      if card in ["JueYing","DiLu","ZhuaHuangFeiDian"]:
        self.pu.__state__[self.turn]["attack"] += 1
      elif card in ["ChiTu","ZiXin","DaWan"]:
        self.pu.__state__[self.turn]["attack"] -= 1
      return self.pu, self.pr, self.pes

    #【杀】
    def Slash(attack=True): #p3 
      pes[self.turn].__del_cards__(self.action.card)

      self.pu.__previous_id__ = self.turn
      self.pu.__previous_action__ = self.action
      self.pu.__num_hand_cards__ = self.pu.__num_hand_cards__ - 1
      target = self.action.targets[0]

      # 若装备有【寒冰剑】，可防止杀造成伤害而改为弃对方两张非判定区的牌
      equip_cards = self.pu.equipment_cards[self.turn]
      if "HanBingJian" in equip_cards:
          if attack == False:
            for i in range(2):
              self.pes[target].hand_cards.pop()

      self.pu.__turn__ = target
      return self.pu, self.pr, self.pes

    #【无懈可击】
    def WuXieKeJi():
      return self.pu, self.pr, self.pes









