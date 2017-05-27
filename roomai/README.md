
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

In conventional poker terms, a game of Kuhn poker proceeds as follows:

&nbsp;- Each player antes 1.

&nbsp;- Each player is dealt one of the three cards, and the third is put aside unseen.

&nbsp;- Player one can check or bet 1.

&nbsp;&nbsp;&nbsp;&nbsp;- If player one checks then player two can check or bet 1.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player two checks there is a showdown for the pot of 2 (i.e. the higher card wins 1 from the other player).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player two bets then player one can fold or call.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player one folds then player two takes the pot of 3 (i.e. winning 1 from player 1).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player one calls there is a showdown for the pot of 4 (i.e. the higher card wins 2 from the other player).
&nbsp;&nbsp;&nbsp;&nbsp;If player one bets then player two can fold or call.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player two folds then player one takes the pot of 3 (i.e. winning 1 from player 2).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- If player two calls there is a showdown for the pot of 4 (i.e. the higher card wins 2 from the other player).


#### 2. FiveCardStud

#### 3. TexasHoldEm


