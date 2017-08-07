
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


#### 2. Action

Player takes a action, and Env forwards with this action.

<pre>
class AbstractAction:
    def key(self):
        raise NotImplementedError("The key function hasn't been implemented")
    def lookup(self, key):
        raise NotImplementedError("The lookup function hasn't been implemented")
</pre>


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

    @classmethod
    def available_actions(cls, public_state, person_state):
        raise NotImplementedError("The available_actions function hasn't been implemented")

    @classmethod
    def is_action_valid(cls,action, public_state, person_state):
        raise NotImplementedError("The is_action_valid function hasn't been implemented")

</pre>



The compete function holds a competition for the players, and computes the scores.

## List of different games

If you want to develop an AI-bot for a particular game, you need to know the structure of Info and action in this game. 
For example,  if you want to deveop an AI for TexasHoldem, you need to know where to find your hand cards.
We list this thing as follows.

- [KuhnPoker](https://github.com/roomai/RoomAI/blob/master/roomai/kuhn/README.md)
- [FiveCardStud](https://github.com/roomai/RoomAI/blob/master/roomai/fivecardstud/README.md)
- [TexasHoldEm](https://github.com/roomai/RoomAI/blob/master/roomai/texas/README.md)
- [SevenKing](https://github.com/roomai/RoomAI/blob/master/roomai/sevenking/README.md)
