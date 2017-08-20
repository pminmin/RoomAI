### KuhnPoker

Kuhn poker is an extremely simplified form of poker developed by Harold W.
Kuhn as a simple model zero-sum two-player imperfect-information game, amenable to a complete game-theoretic analysis.
In Kuhn poker, the deck includes only three playing cards, for example a King, Queen, and Jack.
One card is dealt to each player, which may place bets similarly to a standard poker.
If both players bet or both players pass, the player with the higher card wins, otherwise, the betting player wins.
You can see details of Kuhn poker in [Wikipedia](https://en.wikipedia.org/wiki/Kuhn_poker).

In Kuhn poker, the player has two actions to choose: roomai.kuhn.KuhnPokerAction("bet") and roomai.kuhn.KuhnPokerAction("check").

<pre>
class KuhnPokerPublicState(roomai.abstract.AbstractPublicState):
        turn                       = None
        ## players[turn] takes a action
        ## turn = 0 or turn = 1 (turn is in [0,1])
        ## Kuhn Poker is a game with two players

        first                      = None
        ## player[first] firstly t a action

        action_list                = None
        ## action history.
        ## for example, action_list = ["bet","check"]
        ## "bet" "check" are keys of KuhnPokerAction


        is_terminal                = None
        ## is_terminal = true means the game is over. At this time, scores is not None
        scores                     = None
        ## when is_terminal = true, scores = [float0, float1].
        ## float0 is the score gained by player[0]
        ## float1 is the score gained by player[1]

class KuhnPokerPersonState(roomai.abstract.AbstractPersonState):
        available_actions          = None
        ## the available actions for the player, who receives this person state.
        ## for example, available_actions = {}
        ## or availabel_actions = {"bet": roomai.kuhn.KuhnPokerAction.lookup("bet")}

        id                         = None
        ## the id of the player, who receives this person state.
        ## for example, id = 0 means the player receiving this person state is players[0]

        card                       = None
        ## the card dealt to the player receving this person state
        ## card = 0 or card = 1 or card = 2. (card is in [0,1,2])

</pre>

The initilization parameters of Kuhn Env.

<pre>
class KuhnPokerEnv(roomai.common.AbstractEnv)
    def init(self, params=dict()):

        if "record_history" in params:
            self.record_history = params["record_history"]
        else:
            self.record_history = False
        # record_history must be true, when you need call backward

        if "start_turn" in params:
            self.start_turn = params["start_turn"]
        else:
            self.start_turn = int(random.random() * 2)
        # players[start_turn] is the first player to take a action
     
        ... ...
</pre>