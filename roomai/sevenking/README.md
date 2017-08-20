### TexasHoldEm Poker


SevenKing_Five_Two_Three is a poker game in the Chinese [Wikipedia](https://zh.wikipedia.org/wiki/7%E9%AC%BC523).


In SevenKing, we use the class roomai.sevenking.SevenKingPokerCard as the poker card. Note: we extend roomai.common.PokerCard by implementing roomai.sevenking.SevenKingPokerCard, since the rank of suit in SevenKing is different from that in general.
The poker card has the point (2, 3, A for example) and suit(Spade, Heart, Club and Diamond). There is a special suit (ForKing) for the r and R point.

The basic usage is as follows:
<pre>
>>> import roomai.sevenking
>>> poker_card = roomai.sevenking.SevenKingPokerCard.lookup("A_Spade")
>>> poker_card.point_str
'A'
>>> poker_card.point_rank
8
>>> poker_card.suit_str
"Spade"
>>> poker_card.suit_rank
3
>>> poker_card.key
"A_Spade"
>>> poker_card1 = roomai.sevenking.SevenKingPokerCard.lookup("r_ForKing")
>>> poker_card1.key
"r_ForKing"
>>> poker_card1.suit_rank
4
</pre>


In SevenKing, the action is consisted of poker cards. The basic usage is as follows:
<pre>
>>> action = roomai.sevenking.SevenKingAction.lookup("3_Spade,3_Heart")
>>> action.key
"3_Spade,3_Heart"
>>> action.pattern
"p_2"
>>> action = roomai.sevenking.SevenKingAction.lookup("")
>>> action.key
""
>>> action.pattern
"p_0"
</pre>
The "" action is special action, since it contains no poker card. This action is considered as "fold" in SevenKing


The structures of Public_State and Person_State in SevenKing are as follows. All attributes in Public_State and Person_State are None by default.

<pre>

class SevenKingPersonState(roomai.common.AbstractPersonState):
    def __init__(self):
        self.available_actions            = None
        ## the available actions for the player, who receives this person state.
        ## for example, available_actions = {}
        ## or availabel_actions = {"A_Spade,A_Heart": roomai.sevenking.SevenKingAction.lookup("A_Spade, A_Heart")}

        self.id                           = None
        ## the id of the player, who receives this person state.
        ## for example, id = 0 means the player receiving this person state is players[0]

        self.hand_cards                   = None
        ## the hand cards of the player
        ## for example, self.hand_cards   = [roomai.sevenking.SevenKingPokerCard.lookup("A_Spade"

class SevenKingPublicState(roomai.common.AbstractPublicState):
    def __init__(self):
        self.previous_id        = None
        self.previous_action    = None
        ## players[previous_id] took the previous_action just before this action
        ## These are history records
        ## In the beginning of the game, previous_id and previous_action = None

        self.is_terminal         = None
        self.scores              = None
        ## is_terminal = true means the game is over. At this time, scores is not None
        ## when is_terminal = true,  scores = [float0, float1, ..., float_n].
        ## when is_terminal = false, scores = None

        self.stage            = None
        ### self.stage = 0 or self.stage = 1
        ### when self.stage = 0, the player throws some cards by taking a action, and will receive the same number of cards
        ### when self.stage = 1, the player

        self.num_players      = None
        ### the num of players, for example self.num_players = 0

        self.showed_cards     = None
        self.num_showed_cards = None
        self.num_keep_cards   = None
        ### When a player throws a card, this card will be public(showed).
        ### For example, self.showed_cards = [roomai.sevenking.SevenKingPokerCard.lookup("A_Spade")], self.num_showed_cards = 1
        ### self.num_keep_cards is the number of cards on the table.

        self.num_hand_cards   = None
        ### The numbers of cards in the different players
        ### self.num_hand_cards = [1,3,5] means that the player0 has 1 card, the player1 has 3 cards and the player2 has 5 cards

        self.is_fold          = None
        ### Is the players fold ?
        ### for example, self.is_fold = [True,False, False]
        self.num_fold         = None
        ### self.num_fold = 1

        self.license_action   = None
        ### for example, self.license_action =  roomai.sevenking.SevenKingAction.lookup("A_Spade")
</pre>

The initilization parameters of SevenKing Env.

<pre>
class KuhnPokerEnv(roomai.common.AbstractEnv)
    def init(self, params=dict()):

        if "record_history" in params:
            self.record_history = params["record_history"]
        else:
            self.record_history = False
        # record_history must be true, when you need call backward


        if "num_players" in params:
            self.num_players = params["num_players"]
        else:
            self.num_players = 3
        # how many players in this game

        if "allcards" in params:
            allcards =  [c.__deepcopy__() for c in params["allcards"]]
        else:
            allcards =  [c.__deepcopy__() for c in AllSevenKingPokerCards.values()]
            random.shuffle(allcards)
        # The poker cards used in this game is from the allcards (from tail to head)
        
        ... ...
</pre>