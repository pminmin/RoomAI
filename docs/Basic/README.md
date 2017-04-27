
##  Basic Concepts

There are some basic concepts in RoomAI: Player, Env, Info and Action. The basic procedure of a competition is shown as follows. All AI-bot player receive information from env, the current player takes a action, and the env forwards with this action.

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

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/docs/game.png)

We define Player, Env, and Info as abstract classes in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.py), and all corresponding classes must extend them.  


#### 1.Info

The info is the information sent by env to player, which is consisted of public states、private states and person state.

<pre>
class AbstractPublicState:
    # players[turn] will take a action
    turn              = None 

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
        self.person_state       = None
</pre>

If there are n players, env.forward will return n+1 infos. The i-th info is w.r.t the i-th player except the last info.
The last info is designed for recording private_state. 

##### All infos contain the public_state. 

##### Only the last info contains the private_state.

##### All infos contain the person_state. For different player, the person state is different. Only the person_state in the info w.r.t the player who will take a action, contains non-None available_actions.

The info is the most important concept for AI-bot developers, and is very different for different games. We list all info structures for the games supported by roomai. 

##### [KuhnPoker]()
##### [DouDiZhu]()
##### [Texas]()

#### 2.Player

A player is an AI-bot.

<pre>
class AbstractPlayer:
    def receive_info(self,info):
        raise NotImplementedError("The receiveInfo function hasn't been implemented") 

    def take_action(self):
        raise NotImplementedError("The takeAction function hasn't been implemented") 

    def reset(self):
        raise NotImplementedError("The reset function hasn't been implemented")
</pre>


#### 3.Env

The env is a environment of a game.
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

#### 4.Action

A player takes a action, and env forwards with this action.














