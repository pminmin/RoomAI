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

## 3  Info and Action Structures

The info and action are important concepts for AI-bot developers, and are very different for different games. We list info and action structures for the games supported by roomai:

### 3.1 [Info and Action Structures for KuhnPoker ]



### 3.3 [Info and Action Structures for Texas]

# License

# Contributors

If you would like to contribute to the project, please send me (lili1987mail at gmail.com) an email. We are always happy for more help.
