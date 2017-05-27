
#  RoomAI Tutorials

## Basic Concepts

Before read detailed guidance, please read [quick guidance](https://github.com/roomai/RoomAI#1-quick-guidance)

There are some basic concepts in RoomAI: Player, Env, Info and Action. The basic procedure of a competition is shown as follows. All AI-bot players receive information from env, the current player takes a action, and the env forwards with this action.

<pre>
def compete(env, players):
   '''
   :param env: the game environments
   :param players: the array of players
   :return: the final scores of this competition
   '''
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

We define these basic concepts as abstract classes in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.py), and all corresponding classes must extend them.  


#### 1. Info

Info is the information sent by env to player. Info is consisted of private_state、 public_state and person_state. 

<pre>

class AbstractPrivateState:
    pass
    
class AbstractPublicState:
    turn            = None
    previous_id     = None
    previous_action = None

    is_terminal     = False
    scores          = None

class AbstractPersonState:
    id                = None 
    # if avilable_actions is non-None, it is a dict with (action_key, action) 
    available_actions = None 

class AbstractInfo:
    public_state       = None
    person_state       = None
</pre>


All Infos contain the same public state. 

All Infos contain the person state, and the person state is different for different players. Only the person_state in the Info w.r.t the player who will take a action, contains non-None available_actions dict. 

The private_state won't be in any Info, hence no player can access it.
#### 2. Action

A player takes a action, and env forwards with this action.

<pre>
class AbstractAction:
    def __init__(self,key):
        raise NotImplementedError("The __init__ function hasn't been implemented"
    def get_key(self):
        raise NotImplementedError("The get_key function hasn't been implemented")
</pre>

The get_key function generate the action's key.

#### 3. Player

A Player is an AI-bot.

<pre>
class AbstractPlayer:
    def receive_info(self,info):
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")
</pre>


#### 4. Env

Env is a environment of a game.
<pre>
class AbstractEnv:

    def init(self):
        raise NotImplementedError("The init function hasn't been implemented")

    def forward(self, action):
        raise NotImplementedError("The receiveAction hasn't been implemented")

    @classmethod
    def compete(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")
</pre>

The compete function holds a competition for the players, and computes the scores.

## List of different games

If you want to develop an AI-bot for a particular game, you need to know the structure of Info and action in this game. 
For example,  if you want to deveop an AI for TexasHoldem, you need to know where to find your hand cards.
We list this thing as follows.

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

        first                      = None
        ## player[first] firstly t a action

        action_list                = None
        ## action history.
        ## for exampke, action_list = ["bet","check"]


        is_terminal                = None
        ## is_terminal = true means the game is over. At this time, scores is not None
        scores                     = None
        ## when is_terminal = true, scores = [float0, float1].
        ## float0 is the score gained by player[0]
        ## float1 is the score gained by player[1]

class KuhnPokerPersonState(roomai.abstract.AbsractPersonState):
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


class KuhnPokerInfo(roomai.abstract.AbstractInfo):
        public_state               = None
        person_state               = None
</pre>



#### 2. Five Card Stud

Five Card Stud is the earliest form of the card game stud poker, originating during the American Civil War, but is less commonly played today than many other more popular poker games.
It is still a popular game in parts of the world, especially in Finland where a specific variant of five-card stud called Sökö (also known as Canadian stud or Scandinavian stud) is played.
The word sökö is also used for checking in Finland ("I check" = "minä sökötän"). You can see details of Five Card Stud in [Wikipedia](https://en.wikipedia.org/wiki/Five-card_stud).

In Five Card Stud, the action has two parts: option (action type) and price (count of chips). The option has six types: Fold, Check, Call, Raise, Bet
and Showhand. The prices for Fold and Check must be zero. Some action examples:
<pre>
roomai.fivecardstud.FiveCardStudAction("Fold_0"),
roomai.fivecardstud.FiveCardStudAction("Check_0"),
roomai.fivecardstud.FiveCardStudAction("Call_15"),
roomai.fivecardstud.FiveCardStudAction("Raise_15"),
roomai.fivecardstud.FiveCardStudAction("Bet_15"),
roomai.fivecardstud.FiveCardStudAction("Showhand_15")
</pre>

#### 3. TexasHoldEm


