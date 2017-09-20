### TexasHoldEm Poker


Texas hold 'em (also known as Texas holdem, hold 'em, and holdem) is a variation of the card game of poker. Two cards, known as the hole cards, are dealt face down to each player, and then five community cards are dealt face up in three stages. The stages consist of a series of three cards ("the flop"), later an additional single card ("the turn" or "fourth street") and a final card ("the river" or "fifth street"). Each player seeks the best five card poker hand from the combination of the community cards and their own hole cards. If a player's best five card poker hand consists only of the five community cards and none of the player's hole cards, it is called "playing the board". Players have betting options to check, call, raise or fold. Rounds of betting take place before the flop is dealt, and after each subsequent deal.
You can see details of TexasHoldEm Poker in [Wikipedia](https://en.wikipedia.org/wiki/Texas_hold_%27em).


#### Action and Action Related Concepts

In TexasHoldEm Poker, the action has two parts: option (action type) and price (count of chips).
The option has five types: Fold,Check,Call,Raise and Allin. The prices for Fold must be zero. The basic usage is as follows:
<pre>
>> action = roomai.texas.TexasHoldemAction.lookup("Fold_0")
>> action.option
"Fold"
>> action.price
0
>> action.key()
"Fold_0"
</pre>

In TexasHoldEm, we use the class roomai.common.PokerCard as the poker card. The poker card has the point (2, 3, A for example) and suit(Spade, Heart, Club and Diamond).
The basic usage is as follows:
<pre>
>>> import roomai.abstract
>>> poker_card = roomai.abstract.PokerCard("A_Spade")
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



#### The structure of Info in TexasHoldEm.

<pre>
class TexasHoldemPublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.num_players        = None
        self.big_blind_bet      = None


        self.is_fold                        = None
        self.num_quit                       = None
        #for example, is_fold = [False, True, False] (3 players)
        #for example, num_quit = 1

        self.is_allin                       = None
        self.num_allin                      = None
        #for example, is_allin = [False, True, False] (3 players)
        #for example, num_allin = 1

        self.is_needed_to_action            = None
        self.num_needed_to_action           = None
        #for is_needed_to_action =[False, True, Flase] (3 players)
        #for example, num_needed_to_action = 1

        self.turn               = None
        ## players[turn] takes a action
        ## for example turn = 0, turn in [0,1,..,num_players-1]

        self.chips              = None
        ## the chips the players have now
        ## for example, chips = [100,110, 30] (if 3 players)

        self.bets               = None
        ## the bets the players bet so far
        ## for exaple, bets = [0,100,20] (if 3 players)

        self.max_bet_sofar      = None

        self.raise_account      = None
        ## If a player want to raise the bet, he/she raises at least raise_account
        ## for example, max_bet_sofar = 100, raise_account = 200,
        ## the current player's bet = 60, a player raises at least (max_bet_sofar-current_bet) + raise_account = 240
        ## because a player makes his bet == max_bet_sofar firstly, and then raise


        self.previous_id        = None
        self.previous_action    = None
        ## players[previous_id] took the previous_action just before this action
        ## These are history records
        ## At first, previous_id and previous_action = None

        self.is_terminal         = None
        self.scores              = None
        ## is_terminal = true means the game is over. At this time, scores is not None
        ## when is_terminal = true,  scores = [float0, float1, ..., float_n].
        ## when is_terminal = false, scores = None




class TexasHoldemPersonState(roomai.abstract.AbstractPersonState):
    available_actions          = None
    ## the available actions for the player, who receives this person state.
    ## for example, available_actions = {}
    ## or availabel_actions = {"bet": roomai.kuhn.KuhnPokerAction("bet")}

    id                         = None
    ## the id of the player, who receives this person state.
    ## for example, id = 0 means the player receiving this person state is players[0]

    hand_cards                 =    None
    ## the hand cards of the player
    ## len(hand_cards) = 2
    ## for example, hand_cards = [PokerCard("A_Spade"), PokerCard("2_Club")]



</pre>

#### initilization parameters

The Env can be initilizated with parameters with env.init(params). The meanings of 
initilization parameters are showed as follows.

<pre>
class TexasHoldemEnv(roomai.common.AbstractEnv):
    def init(self, params = dict()):
        self.logger         = roomai.get_logger()

        if "num_players" in params:
            self.num_players = params["num_players"]
        else:
            self.num_players = 3

        if "dealer_id" in params:
            self.dealer_id = params["dealer_id"]
        else:
            self.dealer_id = int(random.random() * self.num_players)

        if "chips" in params:
            self.chips     = params["chips"]
        else:
            self.chips     = [1000 for i in range(self.num_players)]

        if "big_blind_bet" in params:
            self.big_blind_bet = params["big_blind_bet"]
        else:
            self.big_blind_bet = 10

        if "allcards" in params:
            self.allcards = [c.__deepcopy__() for c in params["allcards"]]
        else:
            self.allcards = []
            for i in range(13):
                for j in range(4):
                    self.allcards.append(roomai.common.PokerCard(i, j))
            random.shuffle(self.allcards)

        if "record_history" in params:
            self.record_history = params["record_history"]
        else:
            self.record_history = False
            
        ...
</pre>
