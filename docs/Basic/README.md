
##  Basic Concepts

There are some basic concepts in RoomAI: 

#### 1.Player

A player is an AI-bot;

#### 2.Env

The env is a environment of a game;

#### 3.Info

The info is the information sent by env to player, which is consisted of public states、private states and available actions;

#### 4.Action

A Player takes a action, and env forwards with this action.



We define these basic concepts as abstract class in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.    py), and all corresponding classes must extends them.  

The basic procedure of a competition is shown as follows. All AI-bot player receive information from env, and the current player takes a action. Env forwards with this action.

<pre>
def round(env, players):
   '''
   :param env: the game environments
   :param players: the array of players
   :return: the final scores of this competition
   '''
   isTerminal, scores, infos = env.init()

   for i in xrange(len(players)):
       players[i].receiveInfo(infos[i])

   while isTerminal == False:
        turn = infos[-1].public_state.turn
        action = players[turn].takeAction()
        isTerminal, scores, infos = env.forward(action)
        for i in xrange(len(players)):
            players[i].receiveInfo(infos[i])

   return scores                
</pre>

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/docs/game.png).

## Info

<pre>
class AbstractPublicState:
    pass

class AbstractPrivateState:
    pass

class AbstractInfo:
    def __init__(self, public_state, private_state):

        ## public state information, which is available for all players
        self.public_state       = None

        ## private state information, which is unavailable for all players
        self.private_state      = None
        
        ## all available_actions for the current player
        self.available_actions  = None

</pre>

If there are n players, env.forward will return n+1 infos. The i-th info is w.r.t the i-th player except the last info.
The last info is designed for recording private_state. All infos contain public_state. Only the info w.r.t the player
who will take a action, contains available_actions. Only the last info contain private_state.

## Player
<pre>
class AbstractPlayer:

    def receiveInfo(self,info):
        '''
        :param:
            info: the information produced by a game environments 
        :raises:
            NotImplementedError: An error occurred when we doesn't implement this function
        '''
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def takeAction(self):
        '''
        :return: A Action produced by this player
        '''
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")


</pre>


## Env

Env is the game environment.

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





