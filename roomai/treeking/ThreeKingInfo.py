import roomai.common

class ThreeKingPublicState(roomai.common.AbstractPublicState):
	def __init__(self):
		self.__state__ = None			# state of game
		self.__stage__ = None			# stage of current player
		self.__lord_id__ = None			# id of lord
		self.__num_players__ = None		# number of players
		self.__previous_id__ = None		# previous player of proactive action
		self.__previous_action__ = None # previous action
		self.__turn__ = None			# turn

		self.__players__ = None			# hero name of each player
		self.__blood__ = None			# remaining blood of each player
		self.__distance__ = None		# distances from other players
		self.__equipment_cards__ = None	# list = [], equipment cards of each player
		self.__fate_zone_cards__ = None # list = [], fate zone cards of each player

		@property
		def state(self):
			return self._state

		@property
		def stage(self):
			return self._stage

		@property
		def lord_id(self):
			return self._lord_id

		@property
		def num_players(self):
			return self._num_players

		@property
		def previous_id(self):
			return self._previous_id

		@property
		def previous_action(self):
			return self._previous_action

		@property
		def turn(self):
			return self._turn

		@property
		def players(self):
			return self._players

		@property
		def blood(self):
			return self._blood

		@property
		def distance(self):
			return self._distance

		@property
		def equipment_cards(self):
			return self._equipment_cards

		@property
		def fate_zone_cards(self):
			return self._fate_zone_cards

	def __deepcopy__(self, newinstance=None, memodict={}):
		if newinstance is None:
			newinstance = ThreeKingPublicState()
		newinstance   = super(ThreeKingPublicState,self).__deepcopy__(newinstance = newinstance)

		newinstance.__state__ = self.state
		newinstance.__stage__ = self.stage
		newinstance.__turn__ = self.turn
		newinstance.__lord_id__ = self.lord_id
		newinstance.__previous_id__ = self.previous_id

		newinstance.__players__ = self.players
		newinstance.__blood__ = self.blood
		newinstance.__distance__ = self.distance

		if self.previous_action is None:
			newinstance.__previous_action__ = None
		else:
			newinstance.__previous_action__ = self.previous_action

		if self.equipment_cards is None:
			newinstance.__equipment_cards__ = None
		else:
			newinstance.__equipment_cards__ = [self.equipment_cards[i] for i in xrange(len(self.num_players))]

		if self.fate_zone_cards is None:
			newinstance.__fate_zone_cards__ = None
		else:
			newinstance.__fate_zone_cards__ = [self.fate_zone_cards[i] for i in xrange(len(self.num_players))]
		return newinstance

class ThreeKingPrivateState(roomai.common.AbstractPrivateState):
	def __init__(self):
		super(ThreeKingPrivateState, self).__init__()
		self.__keep_cards__ = []

	@property
	def keep_cards(self):
		return tuple(self._keep_cards)

	def __deepcopy__(self, newinstance=None, memodict={}):
		if newinstance is None:
			newinstance = ThreeKingPrivateState()
		if self.keep_cards == None:
			newinstance.__keep_cards__ = None
		else:
			newinstance.__keep_cards__ = [self.keep_cards[i].__deepcopy__() for i in xrange(len(self.keep_cards))]
		return newinstance
	
class ThreeKingPersonState(roomai.common.AbstractPersonState):
	def __init__(self):
		super(ThreeKingPersonState, self).__init__()
		self.__hand_cards__ = None
		self.__role_id__ = None

		@property
		def hand_cards(self):
			return self._hand_cards

		@property
		def role_id(self):
			return self._role_id

	def __add_cards__(self, cards):
		for c in cards:
			self.__hand_cards__.append(c)

	def __del_cards__(self, cards):
		for c in cards:
			self.__hand_cards__.remove(c)

	def __deepcopy__(self, newinstance=None, memodict={}):
		if newinstance is None:
			newinstance = ThreeKingPersonState()
		if self.hand_cards is None:
			newinstance.__hand_cards__ = None
		else:
			newinstance.__hand_cards__ = [self.hand_cards[i].__deepcopy__() for i in xrange(len(self.hand_cards))]

		newinstance.__role_id__ = self.role_id
		return newinstance
		
		
		
		
		
		
		
		
		
		
		
		
		
		

