### 1. The Action Space of DouDiZhu

The action space of DouDiZhu is a array of integers, which are between 0 and 16. The meaning of each integer is showed in the following figure.

![The meaning of each integer](https://raw.githubusercontent.com/algorithmdog/RoomAI/master/doc/DouDiZhuPoker/doudizhu.png)

For example, a player's action is [0,0,0,8], it is 3,3,3,J (三带一)。

### 2. Information of DouDiZhu

At each epoch of the DouDiZhu game,  information is sent to each player. The information is stored in a dictory, listed as followed. 

about init

* 2.6 info["init_id"] 

  A player knows its own id by this information.

* 2.7 info["init_cards"] 

  The information is the initial cards.
  
* 2.8 info["add_cards"]


about timing

* 2.4 info["turn"]
 
* 2.3 info["epoch"]

* 2.5 info["phase"].

  The information is the phase of DouDiZhu. The value range is {"rob_lord","play"}.
  
about previous

* 2.7 info["previousTurn"]

* 2.8 info["previousAction"]

* 2.9 info["previousIsActionValid"]


about license

* 2. info["linceseId"]

* 2  info["linceseAction"]




### 3. inner states

* 3.1 about cards: HandCards, addCards

* 3.2 about licensee: licenseeId, licenseeAction

* 3.3 about timming: firstPlayer, turn, phase, epoc


### 3. logic of forward

1. check whether is the action valid

2. the action exerts the influence

3. change timming. check whether is a new round begining
