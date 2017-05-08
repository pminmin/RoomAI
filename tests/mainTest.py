#!/bin/python
from EnvPlayer import *

if __name__ == "__main__":
   env = createEnv("KuhnPokerEnv");
   players = [0,0];
   players[0] = createPlayer("KuhnPokerAlwaysBetPlayer");
   players[1] = createPlayer("KuhnPokerAlwaysBetPlayer");
   env.init(players)

   s = [0,0];
   for i in xrange(1000000):
    _, scores = env.compete(players);
    s[0] = s[0] + scores[0]
    s[1] = s[1] + scores[1]
    
   s[0] = s[0] * 1.0 / 1000000
   s[1] = s[1] * 1.0 / 1000000
   print s;

   '''
   env = createEnv("RockPaperScissorsEnv");
   players = [0,0];
   #players[0] = createPlayer("RockPaperScissorsAlwaysRockPlayer");
   players[0] = createPlayer("RockPaperScissorsRegretMatchPlayer");
   players[1] = createPlayer("RockPaperScissorsRegretMatchPlayer");
   env.init(players);

   s = [0,0];
   for i in xrange(10000000):
    _,_,a = env.round(players);
    s[0] = s[0] + a[0]
    s[1] = s[1] + a[1]
    
   s[0] = s[0] * 1.0 / 10000000
   s[1] = s[1] * 1.0 / 10000000
   print s;
   '''
