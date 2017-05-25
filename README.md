# RoomAI

RoomAI is a toolkit for developing and comparing AI-bots of imperfect information games.

# Contents

## 1 Quick Guidance


### 1.1 Installation

you can install roomai with pip

<pre>
pip install roomai
</pre>


### 1.2 Developing an AI-bot and Testing It with Enviroments

<pre>
#!/bin/python
from roomai.kuhn import *;
import random

class KuhnPokerExamplePlayer(roomai.abstract.AbstractPlayer):
    #@override
    def receive_info(self, info):
        if info.person_state.available_actions is not None:
            self.available_actions = info.person_state.available_actions

    #@override
    def take_action(self):
        idx = int(random.random() * len(self.available_actions))
        return self.available_actions.values()[idx]

    #@overide
    def reset(self):
        pass


if __name__ == "__main__":
        players = [KuhnPokerExamplePlayer() for i in xrange(2)]
        env = KuhnPokerEnv()

        scores = KuhnPokerEnv.compete(env, players)
        print scores
</pre>

## 2  [Detailed Guidance](https://github.com/roomai/RoomAI/blob/master/docs/Basic/README.md)

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


## 3  Things You Need Know Before Developing AI

The info and action are important concepts for AI-bot developers, and are very different for different games. We list info and action structures for the games supported by roomai:

### 3.1 [Things You Need Know Before Developing an KuhnPoker AI ]

### 3.2 [Things You Need Know Before Developing an FiveCardStud AI ]

### 3.3 [Things You Need Know Before Developing an TexasHoldem AI]

# License

# Contributors

If you would like to contribute to the project, please send me (lili1987mail at gmail.com) an email. We are always happy for more help.
