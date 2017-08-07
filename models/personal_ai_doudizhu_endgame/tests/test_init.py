#!/bin/python
import doudizhu_endgame

hand_cards, opponent_cards, opponent_player =doudizhu_endgame.build_endgame(datafile="D:/code/RoomAI/models/personal_ai_doudizhu_endgame/data/4.txt")
hand_cards1, opponent_cards1, opponent_player1 =doudizhu_endgame.build_endgame(datafile="D:/code/RoomAI/models/personal_ai_doudizhu_endgame/data/4.txt")
scores = doudizhu_endgame.run_endgame(opponent_player1, opponent_player,hand_cards,opponent_cards)
print scores