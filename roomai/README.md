
#  RoomAI Tutorials

## Basic Concepts


There are some basic concepts in RoomAI: Player, Env, Info and DouDiZhuPokerAction. The basic procedure of a competition is shown as follows. All AI-bot players receive information from env, the current player takes a action, and the env forwards with this action.

<pre>
def compete(env, players):
   '''
   :param env: the game environments
   :param players: the array of players
   :return: the final scores of this competition
   '''
   for player in players:
        players.reset()
   
   infos, public_state, person_states, private_state = env.init()
   for i in xrange(len(players)):
       players[i].receive_info(infos[i])

   while public_state.is_terminal == False:
        turn = public_state.turn
        action = players[turn].take_action()
        
        infos, public_state, person_states, private_state = env.forward(action)
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])

   return public_state.scores                
</pre>

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/roomai/game.png)

We define these basic concepts as classes in [roomai/common/common.py](https://github.com/roomai/RoomAI/blob/master/roomai/common/common.py), and all corresponding classes must extend them.  


#### 1. Info

Info is the information sent by env to player. Info is consisted of private_state、 public_state and person_state. 

<pre>

class AbstractPrivateState:
    pass
    
class AbstractPublicState:
    turn            = 0
    previous_id     = 0
    previous_action = None

    is_terminal     = False
    scores          = []

class AbstractPersonState:
    id                = 0 
    # if avilable_actions is non-None, it is a dict with (action_key, action) 
    available_actions = dict() 

class Info:
    public_state       = None
    person_state       = None
</pre>

Infos sent to different players are different. They contain the same public states and different person states. Only the person_state in the Info w.r.t the player who will take a action, contains non-None available_actions dict. 

The private_state isn't in any Info, hence no player can access it.


#### 2. DouDiZhuPokerAction

Player takes a action, and Env forwards with this action.

<pre>
class AbstractAction:
    def __init__(self,key):
        raise NotImplementedError("The __init__ function hasn't been implemented"
    def key(self):
        raise NotImplementedError("The key function hasn't been implemented")
</pre>

The key function returns the action's key.

#### 3. Player

Player is an AI-bot.

<pre>
class AbstractPlayer:
    def receive_info(self,info):
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")
</pre>

To develop an AI-bot, you should extend this AbstractPlayer and implement the receive_info、take_action and reset function.


#### 4. Env

Env is a environment of a game.
<pre>
class AbstractEnv:

    def backward(self):
        '''
        The game goes back to the previous states
        :return:infos, public_state, person_states, private_state 
        '''
        ... // The backward function has been implemented

    def forward(self, action):
        '''
        :return:infos, public_state, person_states, private_state 
        '''
        raise NotImplementedError("The forward function hasn't been implemented")

    @classmethod
    def compete(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")
        
</pre>



The compete function holds a competition for the players, and computes the scores.

## List of different games

If you want to develop an AI-bot for a particular game, you need to know the structure of Info and action in this game. 
For example,  if you want to deveop an AI for TexasHoldem, you need to know where to find your hand cards.
We list this thing as follows.

- [KuhnPoker](https://github.com/roomai/RoomAI/blob/master/roomai/README.md#1-kuhnpoker)
- [FiveCardStud](https://github.com/roomai/RoomAI/blob/master/roomai/README.md#2-five-card-stud)
- [TexasHoldEm](https://github.com/roomai/RoomAI/blob/master/roomai/README.md#3-texasholdem-poker)

#### 1. KuhnPoker

Kuhn poker is an extremely simplified form of poker developed by Harold W.
Kuhn as a simple model zero-sum two-player imperfect-information game, amenable to a complete game-theoretic analysis.
In Kuhn poker, the deck includes only three playing cards, for example a King, Queen, and Jack.
One card is dealt to each player, which may place bets similarly to a standard poker.
If both players bet or both players pass, the player with the higher card wins, otherwise, the betting player wins.
You can see details of Kuhn poker in [Wikipedia](https://en.wikipedia.org/wiki/Kuhn_poker).

In Kuhn poker, the player has two actions to choose: roomai.kuhn.KuhnPokerAction("bet") and roomai.kuhn.KuhnPokerAction("check").

<pre>
class KuhnPokerPublicState(roomai.abstract.AbstractPublicState):
        turn                       = None
        ## players[turn] takes a action
        ## turn = 0 or turn = 1 (turn is in [0,1])
        ## Kuhn Poker is a game with two players

        first                      = None
        ## player[first] firstly t a action

        action_list                = None
        ## action history.
        ## for exampke, action_list = ["bet","check"]
        ## "bet" "check" are keys of KuhnPokerAction


        is_terminal                = None
        ## is_terminal = true means the game is over. At this time, scores is not None
        scores                     = None
        ## when is_terminal = true, scores = [float0, float1].
        ## float0 is the score gained by player[0]
        ## float1 is the score gained by player[1]

class KuhnPokerPersonState(roomai.abstract.AbstractPersonState):
        available_actions          = None
        ## the available actions for the player, who receives this person state.
        ## for example, available_actions = {}
        ## or availabel_actions = {"bet": roomai.kuhn.KuhnPokerAction("bet")}

        id                         = None
        ## the id of the player, who receives this person state.
        ## for example, id = 0 means the player receiving this person state is players[0]

        card                       = None
        ## the card dealt to the player receving this person state
        ## card = 0 or card = 1 or card = 2. (card is in [0,1,2])

</pre>



#### 2. Five Card Stud

Five Card Stud is the earliest form of the card game stud poker, originating during the American Civil War, but is less commonly played today than many other more popular poker games.
It is still a popular game in parts of the world, especially in Finland where a specific variant of five-card stud called Sökö (also known as Canadian stud or Scandinavian stud) is played.
The word sökö is also used for checking in Finland ("I check" = "minä sökötän"). You can see details of Five Card Stud in [Wikipedia](https://en.wikipedia.org/wiki/Five-card_stud).

In Five Card Stud, the action has two parts: option (action type) and price (count of chips). The option has six types: Fold, Check, Call, Raise, Bet
and Showhand. The prices for Fold must be zero. The basic usage is as follows:
<pre>
>> action = roomai.fivecardstud.FiveCardStudAction("Fold_0")
>> action.option
"Fold"
>> action.price
0
>> action.key()
"Fold_0"
</pre>

In Five Card Stud, we use the class roomai.fivecardstud.FiveCardStudPokerCard as the poker card. The poker card has the point (2, 3, A for example) and suit(Spade, Heart, Club and Diamond).
The basic usage is as follows:
<pre>
>>> import roomai.fivecardstud
>>> poker_card = roomai.fivecardstud.FiveCardStudPoker("A_Spade")
>>> poker_card.point_str
'A'
>>> poker_card.suit_str
"Spade"
>>> poker_card.key()
"A_Spade"
>>>
</pre>


The structure of Info in Five Card Stud.

<pre>


class FiveCardStudPrivateState(roomai.abstract.AbstractPrivateState):
    all_hand_cards    = None

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


</pre>

#### 3. TexasHoldEm Poker


Texas hold 'em (also known as Texas holdem, hold 'em, and holdem) is a variation of the card game of poker. Two cards, known as the hole cards, are dealt face down to each player, and then five community cards are dealt face up in three stages. The stages consist of a series of three cards ("the flop"), later an additional single card ("the turn" or "fourth street") and a final card ("the river" or "fifth street"). Each player seeks the best five card poker hand from the combination of the community cards and their own hole cards. If a player's best five card poker hand consists only of the five community cards and none of the player's hole cards, it is called "playing the board". Players have betting options to check, call, raise or fold. Rounds of betting take place before the flop is dealt, and after each subsequent deal.
You can see details of TexasHoldEm Poker in [Wikipedia](https://en.wikipedia.org/wiki/Texas_hold_%27em).

In TexasHoldEm Poker, the action has two parts: option (action type) and price (count of chips). 
The option has five types: Fold,Check,Call,Raise and Allin. The prices for Fold must be zero. The basic usage is as follows:
<pre>
>> action = roomai.texas.TexasHoldemAction("Fold_0")
>> action.option
"Fold"
>> action.price
0
>> action.key()
"Fold_0"
</pre>

In TexasHoldEm, we use the class roomai.abstract.PokerCard as the poker card. The poker card has the point (2, 3, A for example) and suit(Spade, Heart, Club and Diamond).
The basic usage is as follows:
<pre>
>>> import roomai.abstract
>>> poker_card = roomai.abstract.PokerCard("A_Spade")
>>> poker_card.point_str
'A'
>>> poker_card.suit_str
"Spade"
>>> poker_card.key()
"A_Spade"
>>>
</pre>


The structure of Info in TexasHoldEm.

<pre>
class TexasHoldemPublicState(roomai.abstract.AbstractPublicState):
    def __init__(self):
        self.stage              = None
        self.num_players        = None
        self.dealer_id          = None
        self.public_cards       = None
        self.num_players        = None
        self.big_blind_bet      = None


        self.is_quit                        = None
        self.num_quit                       = None
        #for example, is_quit = [False, True, False] (3 players)
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