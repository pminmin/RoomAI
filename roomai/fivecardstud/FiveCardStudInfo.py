#!/bin/python
import roomai.abstract

class PrivateState_FiveCardStud(roomai.abstract.AbstractPrivateState):
    first_hand_cards  = None
    second_hand_cards = None
    third_hand_cards  = None
    fourth_hand_cards = None
    fifth_hand_cards  = None

class PublicState_FiveCardStud(roomai.abstract.AbstractPublicState):
    second_hand_cards = None
    third_hand_cards  = None
    fourth_hand_cards = None
    fifth_hand_cards  = None
    turn              = None
    round             = None
    num_players       = None
    is_quit           = None
    num_quit          = None


class PersonState_FiveCardStud(roomai.abstract.AbsractPersonState):
    id                = None
    first_hand_card   = None
    available_actions = None


class Info_FiveCardStud(roomai.abstract.AbstractInfo):
    public_state  = None
    private_state = None
    person_state  = None
