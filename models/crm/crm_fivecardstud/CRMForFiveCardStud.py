#!/bin/python

import numpy as np
import tensorflow as tf

import algorithms


class KuhnPokerCRMPlayer(algorithms.CRMPlayer):
    """
    """
    def __init__(self, num_players=2):
        """

        Args:
            num_players:
        """

        self.graph       = tf.Graph()
        self.num_players = num_players

        with self.graph.as_default() as graph:

            self.chips_variables = tf.placeholder(tf.float32, [None, self.num_players], "chips_variables")
            self.bets_variables = tf.placeholder(tf.float32, [None, self.num_players], "bets_variables")
            self.handcards_variables = tf.placeholder(tf.float32, [None, 13, 4, 1], "handcards_variables")
            self.opponent_handcards_variables = tf.placeholder(tf.float32, [None, 13, 4, self.num_players],
                                                           "opponent_handcards_variables")

            ########### chips and bets ###
            self.chips_w = tf.Variable(tf.float32, [self.num_players, 50])
            self.bets_w = tf.Variable(tf.float32, [self.num_players, 50])

            self.chips_vector = tf.matmul(self.chips_variables, self.chips_w)
            self.bets_vector = tf.matmul(self.bets_variables, self.bets_w)

            ########### hand cards ######
            self.handcards_w = dict()
            self.handcards_w["conv_w1"] = tf.Variable(tf.float32, (1, 5, 4, 5))
            self.handcards_w["conv_w2"] = tf.Variable(tf.float32, (5, 2, 2, 10))

            self.handcards_conv1 = tf.nn.conv2d(self.handcards_variables, self.handcards_w["conv_w1"], [1, 1, 1, 1],
                                            padding="VALID")
            self.handcards_pool1 = tf.nn.max_pool(self.handcards_conv1, [1, 2, 2, 1], [1, 1, 1, 1], padding="VALID")
            self.handcards_conv2 = tf.nn.conv2d(self.handcards_pool1, self.handcards_w["conv_w2"], [1, 1, 1, 1],
                                            padding="VALID")
            self.handcards_pool2 = tf.nn.max_pool(self.handcards_conv2, [1, 2, 2, 1], [1, 1, 1, 1], padding="VALID")
            self.handcards_vector = tf.nn.relu(self.handcards_pool1.reshape())

            ########### opponent hand cards #####
            self.opponent_handcards_w = dict()
            self.opponent_handcards_w["conv_w1"] = tf.Variable(tf.float32, [self.num_players, 5, 4, 5 * self.num_players])
            self.opponent_handcards_w["conv_w2"] = tf.Variable(tf.float32,
                                                               [5 * self.num_players, 2, 2, 10 * self.num_players])

            self.opponent_handcards_conv1 = tf.nn.conv2d(self.opponent_handcards_variables,
                                                     self.opponent_handcards_w["conv_w1"], \
                                                     [1, 1, 1, 1], padding="VALID")
            self.opponent_handcards_pool1 = tf.nn.max_pool(self.opponent_handcards_conv1, [1, 2, 2, 1], [1, 1, 1, 1],
                                                       padding="VALID")
            self.opponent_handcards_conv2 = tf.nn.conv2d(self.opponent_handcards_conv1,
                                                     self.opponent_handcards_w["conv_w2"], \
                                                     [1, 1, 1, 1], padding="VALID")
            self.opponent_handcards_pool2 = tf.nn.max_pool(self.opponent_handcards_conv2, [1, 2, 2, 1], [1, 1, 1, 1],
                                                       padding="VALID")
            self.opponent_handcards_vector = tf.nn.relu(self.opponent_handcards_pool2.reshape)

            ### output ####
            self.total_w1 = tf.Variable(tf.float32, [158, 100])
            self.total_bias1 = tf.Variable(tf.float32, [100])
            self.total_w2 = tf.Variable(tf.float32, [158, 1])
            self.total_bias2 = tf.Variable(tf.float32, [1])

            self.total_vector = tf.concat(1, [self.chips_vector, self.bets_vector, self.handcards_vector,
                                          self.opponent_handcards_vector])
            self.output1 = tf.nn.tanh(
                tf.add(tf.matmul(self.total_vector, self.total_w1), self.total_bias1)
            )
            self.output2 = tf.add(tf.matmul(self.output1, self.total_w2), self.total_bias2)

            ### init ###

            self.init = tf.global_variables_initializer()
            self.sess = tf.Session()
            self.sess.run(self.init)

    # @take a action
    def take_action(self):
        """

        """
        pass


    def reset(self):
        """

        """
        pass

    # @receive_info
    def receive_info(self, info):
        """

        Args:
            info:

        Returns:

        """
        pu = info.public_state
        pe = info.person_state

        if pu.turn != pe.id:    return

        floor_bet = pu.floor_bet
        self.chips = np.asarray(pu.chips) / floor_bet
        self.bets = np.asarray(pu.bets) / floor_bet

        self.hand_cards = parseCards(pu, pe.id).reshape([1, 13, 4, 1])
        self.opponent_hand_cards = []
        for i in range(pu.num_players):
            if i != pe.id:
                self.opponent_hand_cards.append(parseCards(pu, i))
        self.opponent_hand_cards = np.asarray(self.opponent_hand_cards).reshape([1, 13, 4, pu.num_players])

    def __del__(self):
        """

        """
        self.sess.close()


def parseCards(public_state, player_id):
    """

    Args:
        public_state:
        player_id:

    Returns:

    """
    pu = public_state
    cards = np.asarray([[0 for j in range(4)] for i in range(13)])

    hand_cards_set = [pu.second_hand_cards, pu.third_hand_cards, pu.fourth_hand_cards, pu.fifth_hand_cards]
    for hand_cards in hand_cards_set:
        if hand_cards is not None:
            card = hand_cards[player_id]
            cards[card.get_point_rank(), card.get_suit_rank()]

    return cards
