#!/bin/python
import roomai.abstract

<<<<<<< HEAD
class PrivateState_FiveCardStud(roomai.abstract.AbstractPrivateState):
=======
class FiveCardStudPrivateState(roomai.abstract.AbstractPrivateState):
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
    first_hand_cards  = None
    second_hand_cards = None
    third_hand_cards  = None
    fourth_hand_cards = None
    fifth_hand_cards  = None

<<<<<<< HEAD
class PublicState_FiveCardStud(roomai.abstract.AbstractPublicState):
=======
class FiveCardStudPublicState(roomai.abstract.AbstractPublicState):
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
    second_hand_cards = None
    third_hand_cards  = None
    fourth_hand_cards = None
    fifth_hand_cards  = None
    turn              = None
    round             = None
    num_players       = None
    is_quit           = None
    num_quit          = None


<<<<<<< HEAD
class PersonState_FiveCardStud(roomai.abstract.AbsractPersonState):
=======
class FiveCardStudPersonState(roomai.abstract.AbsractPersonState):
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
    id                = None
    first_hand_card   = None
    available_actions = None

<<<<<<< HEAD

class Info_FiveCardStud(roomai.abstract.AbstractInfo):
    public_state  = None
    private_state = None
=======
class FiveCardStudInfo(roomai.abstract.AbstractInfo):
    public_state  = None
>>>>>>> ca315bb2f1ad43fbceac353d88f0a6aa37165179
    person_state  = None
