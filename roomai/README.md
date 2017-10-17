
#  RoomAI Tutorials

## Summary


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
   params = dict()
   
   infos, public_state, person_states, private_state = env.init(params)
   for i in range(len(players)):
       players[i].receive_info(infos[i])

   while public_state.is_terminal == False:
        turn = public_state.turn
        action = players[turn].take_action()
        
        infos, public_state, person_states, private_state = env.forward(action)
        for i in range(len(players)):
            players[i].receive_info(infos[i])

   return public_state.scores                
</pre>

![the basic procedure of roomai](https://github.com/roomai/RoomAI/blob/master/roomai/game.png)

We define these basic concepts as classes in [roomai/common/common.py](https://github.com/roomai/RoomAI/blob/master/roomai/common/common.py), and all corresponding classes must extend them.  


#### 1. Info

Info is the information sent by env to Player. Info is consisted of Public_State and Person_State.  Private_State contains information, which is hidden from all players.
There are same Person_States, each one corresponding to a player. Person_State contains information, which is available for the corresponding player and hidden from other players. Public_State contains information, which is
available for all players.

<pre>

class AbstractPrivateState:
    pass
    
class AbstractPublicState:
    turn            = None
    ## players[turn] is expected to take an action
    ## for example, turn = 0 means the player0 is expected to take an action

    self.previous_id        = None
    self.previous_action    = None
    ## players[previous_id] took the previous_action just before this action
    ## These are history records
    ## In the beginning of the game, previous_id and previous_action = None

    self.is_terminal         = None
    self.scores              = None
    ## is_terminal = true means the game is over. At this time, scores is not None
    ## when is_terminal = true,  scores = [float0, float1, ..., float_n].
    ## when is_terminal = false, scores = None



class AbstractPersonState:
    id                = None
    ## id = 0 means the player receiving this Person_State is players[0]

    available_actions = None
    ## If the corresponding player is expected to take a action,
    ## then available_actions is a dict with (action_key, action)
    ## Otherwise, available_actions is None

class Info:
    public_state       = None
    person_state       = None
</pre>

Infos sent to different players are different. They contain the same public states and different person states. 
Only the person_state in the Info w.r.t the player who will take a action, contains non-None available_actions dict.

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
        ... 
        # The backward function has been implemented in this abstract Env

    def init(self, params = dict()):
        '''
        :return: infos, public_state, person_states, private_state
        '''
        raise NotImplementedError("The init function hasn't been implemented")
        #params is the parameter for the game
        
    def forward(self, action):
        '''
        :return:infos, public_state, person_states, private_state 
        '''
        raise NotImplementedError("The forward function hasn't been implemented")


    #########  Some Utils Function
    @classmethod
    def compete(cls, env, players):
        '''
        holds a competition for the players, and computes the scores.
        '''
        raise NotImplementedError("The round function hasn't been implemented")

    @classmethod
    def available_actions(cls, public_state, person_state):
        '''
        :return all available_actions
        '''
        raise NotImplementedError("The available_actions function hasn't been implemented")

    @classmethod
    def is_action_valid(cls,action, public_state, person_state):
        raise NotImplementedError("The is_action_valid function hasn't been implemented")

</pre>




## Details of different games

If you want to develop an AI-bot for a particular game, you need to know the details of this game.
For example,  if you want to deveop an AI for TexasHoldem, you need to know where to find your hand cards.
You can find these information in the [API doc](http://roomai.readthedocs.io/en/latest/?badge=latest).

