### Five Card Stud

Five Card Stud is the earliest form of the card game stud poker, originating during the American Civil War, but is less commonly played today than many other more popular poker games.
It is still a popular game in parts of the world, especially in Finland where a specific variant of five-card stud called Sökö (also known as Canadian stud or Scandinavian stud) is played.
The word sökö is also used for checking in Finland ("I check" = "minä sökötän"). You can see details of Five Card Stud in [Wikipedia](https://en.wikipedia.org/wiki/Five-card_stud).

In Five Card Stud, the action has two parts: option (action type) and price (count of chips). The option has six types: Fold, Check, Call, Raise, Bet
and Showhand. The prices for Fold must be zero. The basic usage is as follows:
<pre>
>> action = roomai.fivecardstud.FiveCardStudAction.lookup("Fold_0")
>> action.option
"Fold"
>> action.price
0
>> action.key()
"Fold_0"
</pre>

In SevenKing, we use the class roomai.fivecardstud.FiveCardStudPokerCard as the poker card. Note: we extend roomai.common.PokerCard by implementing roomai.fivecardstud.FiveCardStudPokerCard, since the rank of suit in FiveCardStud is different from that in general.
The poker card has the point (2, 3, A for example) and suit(Spade, Heart, Club and Diamond). There is a special suit (ForKing) for the r and R point.
The basic usage is as follows:
<pre>
>>> import roomai.fivecardstud
>>> poker_card = roomai.fivecardstud.FiveCardStudPoker("A_Spade")
>>> poker_card.point_str
'A'
>>> poker_card.point_rank
8
>>> poker_card.suit_str
"Spade"
>>> poker_card.suit_rank
0
>>> poker_card.key()
"A_Spade"
>>>
</pre>


The structures of Public_State and Person_State in Five Card Stud are as follows. All attributes in Public_State and Person_State are None by default.

<pre>


class FiveCardStudPublicState(roomai.abstract.AbstractPublicState):
    second_hand_cards     = None
    third_hand_cards      = None
    fourth_hand_cards     = None
    fifth_hand_cards      = None

    is_quit               = None
    num_quit              = None
    ## for example, is_quit = [False, True, False] (3 players)
    ## for example, num_quit = 1

    is_raise              = None
    num_raise             = None
    ## have the players raise the bet in the current round
    ## for example, is_raise = [False, True, False] (3 players)
    ## for example, num_raise = 1

    is_needed_to_action   = None
    num_needed_to_action  = None
    ## for is_needed_to_action =[False, True, Flase] (3 players)
    ## for example, num_needed_to_action = 1


    chips              = None
    ## the chips the players have now
    ## for example, chips = [100,110, 30] (if 3 players)

    bets               = None
    ## the bets the players bet so far
    ## for exaple, bets = [0,100,20] (if 3 players)

    upper_bet              = None
    floor_bet              = None
    max_bet_sofar          = None

    turn                   = None
    round                  = None
    num_players            = None

    previous_id            = None
    previous_action        = None
    previous_round         = None
    ## players[previous_id] took the previous_action, and the round was previous_round before this action.
    ## if previous_round != round (previous_round +1 = round) means the round changes
    ## These are history records
    ## At first, previous_id, previous_action and previous_round = None

    is_terminal                = None
    scores                     = None
    ## is_terminal = true means the game is over. At this time, scores is not None
    ## when is_terminal = true,  scores = [float0, float1, ..., float_n].
    ## when is_terminal = false, scores = None


class FiveCardStudPersonState(roomai.abstract.AbstractPersonState):
    available_actions          = None
    ## the available actions for the player, who receives this person state.
    ## for example, available_actions = {}
    ## or availabel_actions = {"bet": roomai.kuhn.KuhnPokerAction("bet")}

    id                         = None
    ## the id of the player, who receives this person state.
    ## for example, id = 0 means the player receiving this person state is players[0]


    first_hand_card   = None
    second_hand_card  = None
    third_hand_card   = None
    fourth_hand_card  = None
    fifth_hand_card   = None
    ## for example, first_hand_card = roomai.fivecardstud.FiveCardStudPokerCard.lookup("A_Spade")


</pre>

