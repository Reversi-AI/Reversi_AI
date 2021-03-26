"""Implementation of Reversi and elementary players

Module Description
===============================

This module contains a collection of classes and functions that represents games of Reversi.

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2020.
"""
from __future__ import annotations

import copy
import random
import time
from typing import Optional

import plotly.graph_objects as go
from plotly.subplots import make_subplots


################################################################################
# Representing Reversi
################################################################################
# representation of occupancy of a square on the board
_EMPTY = ''
_BLACK = 'X'
_WHITE = 'O'


class ReversiGame:
    """A class representing a state of a game of Reversi.
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional nested list representing a Reversi board
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _is_black_turn: a boolean representing whether black is the current player
    #   - _num_black_pieces: an integer representing the number of black pieces on the board
    #   - _num_white_pieces: an integer representing the number of white pieces on the board

    # Representation Invariants:
    #   - len(_board) == 8
    #   - all(len(row) == 8 for row in _board)
    #   - all elements in the inner lists of _board is in {_EMPTY, _BLACK, _WHITE}
    _board: list[list[str]]
    _valid_moves: list[str]
    _is_black_turn: bool

    def __init__(self, board: list[list[Optional[str]]] = None,
                 black_turn: bool = True) -> None:
        """Initialize a game with the given state. The board is empty if board is None.

        Representation Invariants:
            - board is None or len(_board) == 8
            - board is None or all(len(row) == 8 for row in _board)
            - board is None or every element in the inner lists of _board is in {_EMPTY,
                                                                                 _BLACK, _WHITE}

        :param board: the given board state of the game. None by default when initializing a new
        game
        :param black_turn: boolean representing whether black is the current active player. True
        by default when initializing a new game
        :return: None
        """
        if board is None:
            # create an empty 8x8 board
            self._board = []
            for _ in range(8):
                self._board.append([_EMPTY] * 8)

            # place 2 black and 2 white pieces on the center
            self._board[3][3], self._board[4][4] = _WHITE, _WHITE
            self._board[3][4], self._board[4][3] = _BLACK, _BLACK

        else:
            self._board = board

        self._is_black_turn = black_turn
        self._valid_moves = self._calculate_valid_moves(self._board, self._is_black_turn)

    def get_valid_moves(self) -> list[str]:
        """Return a list of the valid moves for the active player

        :return: list of valid moves
        """
        return self._valid_moves

    def make_move(self, move: str) -> None:
        """Make the given move and mutate the instance attributes of self such that
        self would represent the updated game state after the move is made.

        If move is not a currently valid move, raise a ValueError.

        :param move: the given move to be made
        :return: None
        """
        # TODO

    def simulate_move(self, move: str) -> ReversiGame:
        """Make the given move in a copy of self, and return the copy after the move is made.

        If move is not a currently valid move, raise a ValueError.
        """
        # TODO

    def is_black_move(self) -> bool:
        """Return whether the black player is to move next.

        :return: whether the black player is to move next
        """
        return self._is_black_turn

    def get_num_pieces(self, piece: str) -> int:
        """Return the number of the given piece on the current board.

        Preconditions:
            - piece in {_BLACK, _WHITE}

        :param piece: the piece to count on the current board
        :return: the number of the given piece on the current board
        """
        num_piece_so_far = 0

        for row in self._board:
            for square in row:
                if square == piece:
                    num_piece_so_far += 1

        return num_piece_so_far

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.

        :return: winner of the game (black or white) or 'draw' if the game ended in a draw.
        None if the game is not over.
        """
        if len(self._valid_moves) == 0:
            if len(self._calculate_valid_moves(self._board, not self._is_black_turn)) == 0:
                num_black_pieces = self.get_num_pieces(_BLACK)
                num_white_pieces = self.get_num_pieces(_WHITE)

                if num_black_pieces > num_white_pieces:
                    return 'black'
                elif num_black_pieces == num_white_pieces:
                    return 'draw'
                else:
                    return 'white'
        else:
            return None

    def _calculate_valid_moves(self, board: list[list[str]], is_black_active: bool) -> list:
        """Return all possible moves on a given board state with a given active player."""
        # TODO


################################################################################
# Player classes
################################################################################
class Player:
    """An abstract class representing a Minichess AI.

    This class can be subclassed to implement different strategies for playing chess.
    """

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        raise NotImplementedError


class ConsoleUserPlayer(Player):
    """A human player using the console as an interface"""

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game by entering the move into the console.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        move = input('Please enter your move here')
        while move not in game.get_valid_moves():
            print('Invalid move.')
            move = input('Please enter your move here')
        return move


class RandomPlayer(Player):
    """A Minichess AI whose strategy is always picking a random move."""

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        possible_moves = game.get_valid_moves()
        return random.choice(possible_moves)
