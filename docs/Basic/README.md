
##  Basic Concepts
There are some basic concepts in RoomAI: Player 、Env、 Info、 Public_State, Private_State and Action. Player is an AI-player, Env is a game environment. Player receives Info consisted of Public_State、 Private_State and available Actions, and takes a action. Env forwards with this action.

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/docs/game.png)

### Info

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

    def get_public_state(self):
        return self.public_state

    def get_private_state(self):
        return self.private_state

    def get_available_actions(self):
        return self.available_actions
</pre>

### Player
Player is 

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


### Env

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

The round function holds a competition for the players, and computes the scores. A typical implementation of this function is shown as follows.

<pre>
def round(cls, env, players):
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

All above concepts are defined as abstract classes in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.py)



