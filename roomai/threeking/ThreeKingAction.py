#!/bin/python
import roomai.common

class ThreeKingAction(roomai.common.AbstractAction):
	def __init__(self, key):
		if not isinstance(key, str):
			raise TypeError("The key for TreeKingAction is a str, not %s"%type(key))

		if key:
			action_info = key.strip().split("-") # skill, card, targets, other_targets, target_cards
			self.__skill__ = roomai.threeking.ThreeKingSkills.lookup(action_info[0])

			if self.__skill__.name in []: # pattern 1
				self.__key__ = self.__skill__.name

			elif self.__skill__.name in []: # pattern 2
				self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1])
				self.__key__ = self.__skill__.name + "-" + self.__card__.key

			elif self.__skill__.name in []: # pattern 3
				self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1])

				for target in action_info[2].split(","):
					self.__targets__.append(roomai.threeking.players.lookup(target))
				self.__key__ = self.__skill__.name + "-" + self.__card__.key + "-" + ",".join([t.name for t in self.__targets__])

			elif self.__skill__.name in []: # pattern 4
				self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1])

				for target in action_info[2].split(","):
					self.__targets__.append(roomai.threeking.ThreeKingPlayers.lookup(target))

				for o_target in action_info[3].split(","):
					self.__other_targets__.append(roomai.threeking.ThreeKingPlayers.lookup(o_target))

				self.__key__ = self.__skill__.name + "-" + self.__card__.key + "-" + ",".join([t.name for t in self.__targets__]) \
								+ "-" + ",".join([o_t.name for o_t in self.__other_targets__])

			elif self.__skill__.name in []: # pattern 5
				self.__card__ = roomai.threeking.ThreeKingPokerCard.lookup(action_info[1])

				for target in action_info[2].split(","):
					self.__targets__.append(roomai.threeking.ThreeKingPlayers.lookup(target))

				for o_target in action_info[3].split(","):
					self.__other_targets__.append(roomai.threeking.ThreeKingPlayers.lookup(o_target))

				for t_card in action_info[4].split(","):
					self.__target_cards__.append(roomai.threeking.ThreeKingPokerCard.lookup(t_card))

				self.__key__ = self.__skill__.name + "-" + self.__card__.key + "-" + ",".join([t.name for t in self.__targets__]) \
								+ "-" + ",".join([o_t.name for o_t in self.__other_targets__]) + "-" + ",".join([t_card.name for \
									t_card in self.__target_cards__])

		@property
		def skill(self):
			return self.__skill__

		@property
		def card(self):
			return self.__card__

		@property
		def targets(self):
			return self.__targets__

		@property
		def other_targets(self):
			return self.__other_targets__

		@property
		def target_cards(self):
			return self.__target_cards__
			
	@classmethod
	def lookup(cls, key):
		if key not in AllThreeKingActions:
			AllThreeKingActions[key] = ThreeKingAction(key)
		return AllThreeKingActions[key]

	def __deepcopy__(self, newinstance=None, memodict={}):
		if self.__key__ in AllThreeKingActions:
			return AllThreeKingActions[self.__key__]

		if newinstance is None:
			newinstance = ThreeKingAction(self.__key__)
		newinstance = super(ThreeKingAction, self).__deepcopy__(newinstance = newinstance)
		newinstance.__skill__ = self.__skill__
		newinstance.__card__ = self.__card__
		newinstance.__targets__ = self.__targets__
		newinstance.__other_targets__ = self.__other_targets__
		newinstance.__target_cards__ = self.__target_cards__
		AllThreeKingActions[self.__key__] = newinstance
		return newinstance

AllThreeKingActions = dict()
			

			
			
			



