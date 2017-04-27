
##  Basic Concepts

The basic procedure of a competition is shown as follows. All AI-bot player receive information from env, the current player takes a action, and the env forwards with this action.

<pre>
def round(env, players):
   '''
   :param env: the game environments
   :param players: the array of players
   :return: the final scores of this competition
   '''
   isTerminal, scores, infos = env.init()

   for i in xrange(len(players)):
       players[i].receive_info(infos[i])

   while isTerminal == False:
        turn = infos[-1].public_state.turn
        action = players[turn].take_action()
        isTerminal, scores, infos = env.forward(action)
        for i in xrange(len(players)):
            players[i].receive_info(infos[i])

   return scores                
</pre>

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/docs/game.png).

There are some basic concepts in RoomAI: 

#### 1.Player

A player is an AI-bot;

#### 2.Env

The env is a environment of a game;

#### 3.Info

The info is the information sent by env to player, which is consisted of public states、private states and person state;

#### 4.Action

A player takes a action, and env forwards with this action.



We define Player, Env, and Info as abstract classes in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.py), and all corresponding classes must extend them.  


## Info

<pre>
class AbstractPublicState:
    pass

class AbstractPrivateState:
    pass

class AbstractPersonState:
    id                = None
    available_actions = None

class AbstractInfo:
    def __init__(self, public_state, private_state, person_state):
       
        ## public state information
        ## available for all players
        self.public_state       = None

        ## private state information
        ## unavailable for all players
        self.private_state      = None
        
        ## person state information. 
        ## availabel for all players. 
        ## For different player, the person state information is different.
        ## The personal_state contains available actions
        self.person_state       = None
        

</pre>

If there are n players, env.forward will return n+1 infos. The i-th info is w.r.t the i-th player except the last info.
The last info is designed for recording private_state. 

##### All infos contain public_state. 

##### Only the last info contains private_state.

##### All infos contain personal_state. Only the info w.r.t the player who will take a action, contains available_actions.

## Player
<pre>
class AbstractPlayer:
    def receive_info(self,info):
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")
</pre>

## Env

<pre>
class AbstractEnv:

    def init(self):
        raise NotImplementedError("The init function hasn't been implemented")

    def forward(self, action):
        raise NotImplementedError("The receiveAction hasn't been implemented")

    @classmethod
    def round(cls, env, players):
        raise NotImplementedError("The round function hasn't been implemented")
</pre>

The round function holds a competition for the players, and computes the scores.





