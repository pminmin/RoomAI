
##  Detailed Guidance

Before read detailed guidance, please read [quick guidance](https://github.com/roomai/RoomAI#1-quick-guidance)

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

We define these basic concepts as abstract classes in [roomai/abstract/Abstract.py](https://github.com/roomai/RoomAI/blob/master/roomai/abstract/Abstract.py), and all corresponding classes must extend them.  


#### 1. Info

The info is the information sent by env to player, which is consisted of private_state、 public_state and person_state. 

<pre>

class AbstractPrivateState:
    pass
    
class AbstractPublicState:
    # players[turn] will take a action
    turn              = None 

class AbstractPersonState:
    id                = None 
    # if avilable_actions is non-None, it is a dict with (action_key, action) 
    available_actions = None 

class AbstractInfo:
    def __init__(self, public_state, private_state, person_state):
        self.private_state      = None
        self.public_state       = None
        self.person_state       = None
</pre>

Three propertes:

##### 1.1 If there are n players, env.forward will return n+1 infos. The i-th info is w.r.t the i-th player except the last info. The last info is designed for recording private_state, and only the last info contains non-None private_state. Hence, no player will get private_state

##### 1.2 All infos contain the public_state. 

##### 1.3 All infos contain the person_state. For different players, the person state is different. Only the person_state in the info w.r.t the player who will take a action, contains non-None available_actions dict. non-None available_actions dict is with (action_key, action)

#### 2. Action

A player takes a action, and env forwards with this action.

<pre>
class AbstractAction:
    def toString(self):
        raise NotImplementedError("The toString function hasn't been implemented")
</pre>

The toString function generate the action's key.

#### 3. Player

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


#### 4. Env

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

#### 5. List of different games' info structure and action structure 

The info and action are  important concepts for AI-bot developers, and are very different for different games. We list info and action structures for the games supported by roomai:

##### [KuhnPoker]()
##### [DouDiZhu]()
##### [Texas]()
