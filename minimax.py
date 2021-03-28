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
import random

from pieces import _BLACK, _WHITE
from reversi import ReversiGame, Player


class GreedyPlayer(Player):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def __init__(self, depth: int = 1) -> None:
        """Initialize this player with the given depth of minimax. Default depth = 1

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
        valid_moves = game.get_valid_moves()
        random.shuffle(valid_moves)

        if find_max:
            max_eval_so_far = -math.inf
            best_move = valid_moves[0]
            for move in valid_moves:
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
            worst_move = valid_moves[0]
            for move in valid_moves:
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
            - piece in {_BLACK, _WHITE}

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
            if piece == _BLACK:
                return game.get_num_pieces()[_BLACK] / game.get_num_pieces()[_WHITE]
            else:
                return game.get_num_pieces()[_WHITE] / game.get_num_pieces()[_BLACK]


class PositionalPlayer(Player):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def __init__(self, depth: int = 1) -> None:
        """Initialize this player with the given depth of minimax. Default depth = 1

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
        :return: (selected_move, corresponding value)
        """
        if game.get_winner() is not None or depth == 0:
            return None, self._value_eval(game, piece)

        # recursion
        valid_moves = game.get_valid_moves()
        random.shuffle(valid_moves)

        if find_max:
            max_eval_so_far = -math.inf
            best_move = valid_moves[0]
            for move in valid_moves:
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
            worst_move = valid_moves[0]
            for move in valid_moves:
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
        """The evaluation function for minimax. For Positional Player, the evaluation function
        will evaluate the positional advantage of the pieces on the board.

        Preconditions:
            - piece in {_BLACK, _WHITE}

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
            num_black, num_white = game.get_num_pieces()[_BLACK], game.get_num_pieces()[_WHITE]
            weights = [[100, -20, 10, 5,  5, 10, -20, 100],
                       [-20, -50, -2, -2, -2, -2, -50, -20],
                       [10, -2, -1, -1, -1, -1, -2, 10],
                       [5, -2, -1, -1, -1, -1, -2, 5],
                       [5, -2, -1, -1, -1, -1, -2, 5],
                       [10, -2, -1, -1, -1, -1, -2, 10],
                       [-20, -50, -2, -2, -2, -2, -50, -20],
                       [100, -20, 10, 5, 5, 10, -20, 100]]
            if piece == _BLACK:
                if num_black + num_white < 40:  # early to middle game
                    eval_so_far = 0
                    board = game.get_game_board()
                    for i in range(8):
                        for j in range(8):
                            if board[i][j] == _BLACK:
                                eval_so_far += weights[i][j]
                            elif board[i][j] == _WHITE:
                                eval_so_far -= weights[i][j]
                    return eval_so_far
                else:  # end game
                    return num_black / num_white
            else:
                if num_black + num_white < 40:  # early to middle game
                    eval_so_far = 0
                    board = game.get_game_board()
                    for i in range(8):
                        for j in range(8):
                            if board[i][j] == _WHITE:
                                eval_so_far += weights[i][j]
                            elif board[i][j] == _BLACK:
                                eval_so_far -= weights[i][j]
                    return eval_so_far
                else:  # end game
                    return num_white / num_white


class MobilityPlayer(Player):
    """A Reversi AI player who aims for the maximum piece of its own
    using the minimax algorithm."""
    # Private Instance Attributes:
    #     - _depth: the depth parameter for the minimax algorithm for each decision
    _depth: int

    def __init__(self, depth: int = 1) -> None:
        """Initialize this player with the given minimax depth. Default depth = 1

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
        :return: (selected_move, corresponding value)
        """
        if game.get_winner() is not None or depth == 0:
            return None, self._value_eval(game, piece)

        # recursion
        valid_moves = game.get_valid_moves()
        random.shuffle(valid_moves)

        if find_max:
            max_eval_so_far = -math.inf
            best_move = valid_moves[0]
            for move in valid_moves:
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
            worst_move = valid_moves[0]
            for move in valid_moves:
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
        """The evaluation function for minimax. For Positional Player, the evaluation function
        will evaluate the positional advantage of the pieces on the board.

        Preconditions:
            - piece in {_BLACK, _WHITE}

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
            num_black, num_white = game.get_num_pieces()[_BLACK], game.get_num_pieces()[_WHITE]
            corner_black, corner_white = self._check_corners(game)

            if piece == _BLACK:
                if num_black + num_white < 40:  # early to middle game
                    return 10 * (corner_black - corner_white) + len(game.get_valid_moves())
                else:  # end game
                    return num_black / num_white
            else:
                if num_black + num_white < 40:  # early to middle game
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
        for i in [0, 7]:
            for j in [0, 7]:
                if board[i][j] == _BLACK:
                    corner_black += 1
                elif board[i][j] == _WHITE:
                    corner_white += 1
        return corner_black, corner_white
