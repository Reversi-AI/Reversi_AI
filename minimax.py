"""Greedy minimax player

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
from typing import Optional, Union
import math

from pieces import _BLACK
from reversi import ReversiGame, Player


class GreedyPlayer(Player):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def __init__(self, depth: int) -> None:
        """Initialize this player.

        Preconditions:
            - depth > 0
        """
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
        move, _ = self._minimax(game, piece, self._depth, -math.inf, math.inf, True)
        return move

    def _minimax(self, game: ReversiGame, piece: str,
                 depth: int, alpha: Union[float, int], beta: Union[float, int],
                 find_max: bool) -> tuple[Optional[str], Union[float, int]]:
        """Decide a move with the minimax algorithm. Return a tuple corresponding a decided move
        and the corresponding evaluated value of the game state after the move.

        Return None for the decided move if the game.get_winner() is not None

        Preconditions:
            - depth > 0
            - piece in {_BLACK, _WHITE}

        :param game: the current game state for running minimax
        :param piece: the player of the root
        :param depth: the depth of minimax
        :param alpha: lower bound of value
        :param beta: upper bound of value
        :param find_max: whether to find max evaluation
        """
        if game.get_winner() is not None or depth == 0:
            return None, self._value_eval(game, piece)

        # recursion
        if find_max:
            max_eval_so_far = -math.inf
            best_move = game.get_valid_moves()[0]
            for move in game.get_valid_moves():
                game_after_move = game.simulate_move(move)
                _, move_eval = self._minimax(game_after_move, piece, depth - 1, alpha, beta, False)
                if move_eval > max_eval_so_far:
                    max_eval_so_far = move_eval
                    best_move = move

                # alpha-beta pruning
                alpha = max(alpha, move_eval)
                if beta <= alpha:
                    break
            return best_move, max_eval_so_far
        else:
            min_eval_so_far = math.inf
            worst_move = game.get_valid_moves()[0]
            for move in game.get_valid_moves():
                game_after_move = game.simulate_move(move)
                _, move_eval = self._minimax(game_after_move, piece, depth - 1, alpha, beta, True)
                if move_eval < min_eval_so_far:
                    min_eval_so_far = move_eval
                    worst_move = move

                # alpha-beta pruning
                beta = min(beta, move_eval)
                if beta <= alpha:
                    break
            return worst_move, min_eval_so_far

    def _value_eval(self, game: ReversiGame, piece: str) -> Union[float, int]:
        """The evaluation function for minimax. For GreedMinimax Player,
        the evaluation function will return the number of piece of its side

        Preconditions:
            - winner in {None, _BLACK, _WHITE, "Draw"}
            - piece in {_BLACK, _WHITE}

        :param game: the current game state for evaluation

        """
        if game.get_winner() is not None:
            if game.get_winner() == piece:  # win
                return math.inf
            elif game.get_winner() == 'Draw':  # draw
                return 0
            else:  # lose
                return -math.inf
        else:
            if piece == _BLACK:
                return game.get_num_pieces()[0]
            else:
                return game.get_num_pieces()[1]
