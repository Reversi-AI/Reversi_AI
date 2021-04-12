"""Minimax players

Module Description
===============================

This module contains a collection of classes representing AI Reversi players
using the minimax algorithm to make their decision. The strategy of each player
is represented by the evaluation function of the minimax algorithm

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""
from __future__ import annotations
from typing import Optional, Union
import math
import random

from constants import BLACK, WHITE, BOARD_WEIGHT_8, BOARD_WEIGHT_6
from reversi import ReversiGame, Player


class MinimaxTree:
    """A tree representing a state of a Reversi Game"""
    move: str
    eval: float
    max: bool
    alpha: float
    beta: float
    _subtrees: list[MinimaxTree]
    game: ReversiGame

    def __init__(self, move: str, max: bool, game: ReversiGame, eval: float = 0.0, alpha=-math.inf,
                 beta=math.inf) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.
        """
        self.move = move
        self.alpha = alpha
        self.beta = beta
        self.max = max
        self._subtrees = []
        self.eval = eval

    def get_subtrees(self):
        """Get the subtrees of the tree"""
        return self._subtrees

    def evaluate(self) -> float:
        """Get the evaluation of the Tree"""
        return self.eval

    def add_subtree(self, subtree: MinimaxTree):
        """Append a new tree to this trees subtrees and update it's evaluation"""
        self._subtrees.append(subtree)
        self.update_evalutation()

    def update_evalutation(self):
        """Update the Tree's evaluation"""
        if self.max:
            self.eval = max(tree.evaluate() for tree in self._subtrees)
            self.alpha = max(self.eval, self.alpha)
        else:
            self.eval = min(tree.evaluate() for tree in self._subtrees)
            self.beta = min(self.beta, self.eval)

    def get_best(self):

        best_tree = self._subtrees[0]
        for tree in self._subtrees:
            if tree.evaluate() > best_tree.evaluate():
                best_tree = tree

        return best_tree.move

class TreePlayer(Player):

    def __init__(self, depth: int):
        self._depth = depth


    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state
            - len(game.get_valid_moves) > 0

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        piece = game.get_current_player()
        tree = self.build_minimax_tree(game, piece, depth=self._depth, find_max=True,
                                       previous_move=previous_move)
        return tree.get_best()

    def build_minimax_tree(self, game: ReversiGame, piece: str,
                           depth: int, find_max: bool, previous_move: str) -> MinimaxTree:
        """Construct a tree with a height of depth, prune branches based on the Tree's
        evaluate function"""
        game_tree = MinimaxTree(previous_move, find_max, game)

        if depth == 0:
            game_tree.eval = self._value_eval(game, piece)
        else:
            for move in game.get_valid_moves():
                subtree = self.build_minimax_tree(game.simulate_move(move), piece, depth - 1,
                                                  not find_max, move)
                game_tree.add_subtree(subtree)

                if game_tree.beta < game_tree.alpha:
                    break

        return game_tree

    def _value_eval(self, game: ReversiGame, piece: str):
        raise NotImplementedError


class GreedyTreePlayer(TreePlayer):

    def _value_eval(self, game: ReversiGame, piece: str) -> Union[float, int]:
        """The evaluation function for minimax. For GreedMinimax Player,
        the evaluation function will return the number of piece of its side

        Preconditions:
            - piece in {BLACK, WHITE}

        :param game: the current game state for evaluation
        :return: the evaluated value of the current state
        """
        if game.get_winner() is not None:
            if game.get_winner() == piece:  # win
                return math.inf
            elif game.get_winner() == 'Draw':  # draw
                return 0
            else:  # lose
                return -math.inf
        else:
            if piece == BLACK:
                return game.get_num_pieces()[BLACK] / game.get_num_pieces()[WHITE]
            else:
                return game.get_num_pieces()[WHITE] / game.get_num_pieces()[BLACK]


class PositionalTreePlayer(TreePlayer):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def _value_eval(self, game: ReversiGame, piece: str) -> Union[float, int]:
        """The evaluation function for minimax. For Positional Player, the evaluation function
        will evaluate the positional advantage of the pieces on the board.

        Preconditions:
            - piece in {BLACK, WHITE}

        :param game: the current game state for evaluation
        :return: value evaluated from the current game state
        """
        if game.get_winner() is not None:
            if game.get_winner() == piece:  # win
                return math.inf
            elif game.get_winner() == 'Draw':  # draw
                return 0
            else:  # lose
                return -math.inf
        else:
            num_black, num_white = game.get_num_pieces()[BLACK], game.get_num_pieces()[WHITE]
            board_filled = (num_black + num_white) / (game.get_size() ** 2)
            if game.get_size() == 8:
                selected_board_weight = BOARD_WEIGHT_8
            else:
                selected_board_weight = BOARD_WEIGHT_6

            if piece == BLACK:
                if board_filled < 0.80:  # early to middle game
                    eval_so_far = 0
                    board = game.get_game_board()
                    for i in range(game.get_size() - 1):
                        for j in range(game.get_size() - 1):
                            if board[i][j] == BLACK:
                                eval_so_far += selected_board_weight[i][j]
                            elif board[i][j] == WHITE:
                                eval_so_far -= selected_board_weight[i][j]
                    return eval_so_far
                else:  # end game
                    return num_black / num_white
            else:
                if board_filled < 0.80:  # early to middle game
                    eval_so_far = 0
                    board = game.get_game_board()
                    for i in range(game.get_size()):
                        for j in range(game.get_size()):
                            if board[i][j] == WHITE:
                                eval_so_far += selected_board_weight[i][j]
                            elif board[i][j] == BLACK:
                                eval_so_far -= selected_board_weight[i][j]
                    return eval_so_far
                else:  # end game
                    return num_white / num_white


class MobilityTreePlayer(TreePlayer):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def _value_eval(self, game: ReversiGame, piece: str) -> Union[float, int]:
        """The evaluation function for minimax. For Positional Player, the evaluation function
        will evaluate the positional advantage of the pieces on the board.

        Preconditions:
            - piece in {BLACK, WHITE}

        :param game: the current game state for evaluation
        :return: value evaluated from the current game state
        """
        if game.get_winner() is not None:
            if game.get_winner() == piece:  # win
                return math.inf
            elif game.get_winner() == 'Draw':  # draw
                return 0
            else:  # lose
                return -math.inf
        else:
            num_black, num_white = game.get_num_pieces()[BLACK], game.get_num_pieces()[WHITE]
            corner_black, corner_white = self._check_corners(game)
            board_filled = (num_black + num_white) / (game.get_size() ** 2)

            if piece == BLACK:
                if board_filled < 0.80:  # early to middle game
                    return 10 * (corner_black - corner_white) + len(game.get_valid_moves())
                else:  # end game
                    return num_black / num_white
            else:
                if board_filled < 0.80:  # early to middle game
                    return 10 * (corner_white - corner_black) + len(game.get_valid_moves())
                else:  # end game
                    return num_white / num_black

    def _check_corners(self, game: ReversiGame) -> tuple[int, int]:
        """Return a tuple representing the number of corner taken by each side

        :param game: the game state to be checked
        :return: (corner taken by black, corner taken by white)
        """
        board = game.get_game_board()
        corner_black, corner_white = 0, 0
        for i in [0, game.get_size() - 1]:
            for j in [0, game.get_size() - 1]:
                if board[i][j] == BLACK:
                    corner_black += 1
                elif board[i][j] == WHITE:
                    corner_white += 1
        return corner_black, corner_white
