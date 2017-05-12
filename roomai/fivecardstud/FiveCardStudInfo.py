#!/bin/python
import roomai.abstract


class FiveCardStudPrivateState(roomai.abstract.AbstractPrivateState):
    all_hand_cards    = None

class FiveCardStudPublicState(roomai.abstract.AbstractPublicState):
    public_cards          = None
    is_quit               = None
    num_quit              = None
    is_raise              = None
    num_raise             = None
    is_needed_to_action   = None
    num_needed_to_action  = None

    # chips is array which contains the chips of all players
    chips = None

    # bets is array which contains the bets from all players
    bets = None

    upper_bet              = None
    floor_bet              = None
    max_bet_sofar          = None

    turn                   = None
    round                  = None
    num_players            = None

    previous_id            = None
    previous_action        = None
    previous_round         = None


class FiveCardStudPersonState(roomai.abstract.AbsractPersonState):
    id                = None
    first_hand_card   = None
    available_actions = None


class FiveCardStudInfo(roomai.abstract.AbstractInfo):
    public_state  = None
    person_state  = None
