### Info
<pre>
class PersonState_DouDiZhu(roomai.abstract.AbsractPersonState):
    id                = None
    cards             = None
    add_cards         = None
    available_actions = None

class PrivateState_DouDiZhu(roomai.abstract.AbstractPrivateState):
    def __init__(self):
        self.hand_cards     = [[],[],[]]
        self.keep_cards     = []

class PublicState_DouDiZhu(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.landlord_candidate_id  = -1
        self.landlord_id            = -1
        self.license_playerid       = -1
        self.license_action         = None
        self.is_response            = False

        self.first_player           = -1
        self.turn                   = -1
        self.phase                  = -1
        self.epoch                  = -1

        self.previous_id            = -1
        self.previous_action        = None


class Info_DouDiZhu(roomai.abstract.AbstractInfo):
    def __init__(self):
        self.public_state       = None
        self.private_state      = None
        self.person_state       = None
</pre>

### Action
<pre>
class Action_DouDiZhu(roomai.abstract.AbstractAction):
    def __init__(self, masterCards, slaveCards):
        self.masterCards        = copy.deepcopy(masterCards)
        self.slaveCards         = copy.deepcopy(slaveCards)
    def toString(self):
        
</pre>
