"""ReversiGame class

Module Description
===============================

This module contains a class that represents the game of Reversi.

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

import copy
from typing import Optional

################################################################################
# Representing Reversi
################################################################################
# representation of occupancy of a square on the board
_EMPTY = '_'
_BLACK = 'X'
_WHITE = 'O'

# mapping used for converting move between algebraic and index
_FILE_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
_INDEX_TO_FILE = {i: f for f, i in _FILE_TO_INDEX.items()}
_RANK_TO_INDEX = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
_INDEX_TO_RANK = {i: r for r, i in _RANK_TO_INDEX.items()}


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
    #   - len(self_board) == 8
    #   - all(len(row) == 8 for row in self._board)
    #   - all elements in the inner lists of self._board is in {_EMPTY, _BLACK, _WHITE}
    #   - self._turn in {_BLACK, _WHITE}
    _board: list[list[str]]
    _valid_moves: list[str]
    _turn: str

    def __init__(self, board: list[list[Optional[str]]] = None, turn: str = _BLACK) -> None:
        """Initialize a game with the given state. The board is empty if board is None.

        Representation Invariants:
            - board is None or len(_board) == 8
            - board is None or all(len(row) == 8 for row in _board)
            - board is None or every element in the inner lists of _board is in
            {_EMPTY, _BLACK, _WHITE}
            - turn in {_BLACK, _WHITE}

        :param board: the given board state of the game. None by default when initializing a new
        game
        :param turn: str representing which player should go next
        :return: None
        """
        if board is None:
            # create an empty 8x8 board
            self._board = []
            for _ in range(8):
                self._board.append([_EMPTY] * 8)

            # place 2 black and 2 white pieces on the center
            self._board[3][3], self._board[3][4] = _WHITE, _BLACK
            self._board[4][3], self._board[4][4] = _BLACK, _WHITE

        else:
            self._board = board

        self._turn = turn
        self._update_valid_moves()

    def print_game_board(self) -> None:
        """Return a string representing the state of the board

        :return: None
        """
        print('*' * 26)

        print('   ' + '  '.join([c for c in 'abcdefgh']))

        for i in range(len(self._board)):
            print(f'{i + 1}  ' + '  '.join(self._board[i]))

        print('*' * 26)

    def get_valid_moves(self) -> list[str]:
        """Return a list of the valid moves for the active player

        :return: list of valid moves
        """
        return self._valid_moves

    def _next_player(self) -> None:
        """Mutate self.turn to the next player"""
        if self._turn == _BLACK:
            self._turn = _WHITE
        else:
            self._turn = _BLACK

    def make_move(self, move: str) -> None:
        """Make the given move and mutate the instance attributes of self such that
        self would represent the updated game state after the move is made.

        If move is not a currently valid move, raise a ValueError.

        Preconditions:
            - self.get_winner() is None

        :param move: the move to be made
        :return: None
        """
        if move not in self._valid_moves:
            raise ValueError(f'Move "{move}" is invalid')

        self._update_board(self._turn, move)
        self._next_player()
        self._update_valid_moves()

    def simulate_move(self, move: str) -> ReversiGame:
        """Make the given move in a copy of self, and return the copy after the move is made.

        If move is not a currently valid move, raise a ValueError.

        :param move: the move to be made
        :return: a copy the the game state after the move is made
        """
        copy_state = copy.deepcopy(self)
        copy_state.make_move(move)
        return copy_state

    def get_current_player(self) -> str:
        """Return which player is going to play next

        :return: a string representing which player will play next
        """
        return self._turn

    def get_num_pieces(self) -> tuple[int, int]:
        """Return the number of piece of each color on the board.

        :return: a tuple where the first element represents the number of black pieces
        and the second element represents the number of white pieces
        """
        black_so_far = 0
        white_so_far = 0

        for row in self._board:
            for square in row:
                if square == _BLACK:
                    black_so_far += 1
                if square == _WHITE:
                    white_so_far += 1

        return (black_so_far, white_so_far)

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.

        :return: winner of the game (Black or White) or 'Draw' if the game ended in a draw.
        None if the game is not over.
        """
        if self._is_pass_valid(_BLACK) and self._is_pass_valid(_WHITE):
            black, white = self.get_num_pieces()
            if black > white:
                return 'Black'
            elif black == white:
                return 'Draw'
            else:
                return 'White'
        else:
            return None

    def _update_board(self, turn: str, move: str) -> None:
        """Mutate self._board after the given player made the move. Note that move can be 'pass'

        Preconditions:
            - move is currently a legal move for the active player.

        """
        if move != 'pass':
            y_move, x_move = _algebraic_to_index(move)
            self._board[y_move][x_move] = turn

            flips_so_far = []
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for direction in directions:
                flips_so_far.extend(self._check_flips(turn, move, direction))
            for y, x in flips_so_far:
                self._board[y][x] = turn

    def _update_valid_moves(self) -> None:
        """Mutate self._valid_moves

        :return: None
        """
        self._valid_moves = []
        for y in range(len(self._board)):
            for x in range(len(self._board)):
                move = _index_to_algebraic((y, x))
                if self._is_valid_move(self._turn, move):
                    self._valid_moves.append(move)

        if len(self._valid_moves) == 0:  # no valid moves
            self._valid_moves.append('pass')

    def _is_pass_valid(self, player: str) -> bool:
        """Return whether 'pass' is a valid move for the given player in this game state

        :param player: the player to be tested on pass move
        """
        for y in range(len(self._board)):
            for x in range(len(self._board)):
                move = _index_to_algebraic((y, x))
                if self._is_valid_move(player, move):
                    return False
        return True

    def _is_valid_move(self, player: str, move: str) -> bool:
        """Return whether the given move is valid for the given player.

         Preconditions:
            - player in {_BLACK, _WHITE}
            - move is a coordinate on the board

        :param player: the player making the move
        :param move: the move being made
        :return: whether the given move is valid for the given player
        """
        y, x = _algebraic_to_index(move)
        if self._board[y][x] != _EMPTY:
            return False

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for direction in directions:
            if len(self._check_flips(player, move, direction)) != 0:
                return True
        return False

    def _check_flips(self, player: str, move: str, direction: tuple) -> list[tuple[int, int]]:
        """Assume the player plays a given move, check the given direction for which pieces
        can be flipped.

        direction[0] represents dy which is the proceeding direction of y.
        direction[1] represents dx which is the proceeding direction of x.
        For example, if player = _BLACK, move = 'c4', direction =(0, 1), the function would
        return a list of positions of white pieces that can be flipped on the right of c4

        Preconditions:
            - The square of move is empty
            - player in {_BLACK, _WHITE}
            - direction[0] in {-1, 0, 1}
            - direction[1] in {-1, 0, 1}

        :param player: the player playing the move
        :param move: the move begin played
        :param direction: the direction to be checked for flips
        """
        y, x = _algebraic_to_index(move)
        dy, dx = direction

        if player == _BLACK:
            opponent = _WHITE
        else:
            opponent = _BLACK

        if not self._is_on_board((y + dy, x + dx)):
            return []
        if not self._is_on_board((y + dy + dy, x + dx + dx)):
            return []
        if self._board[y + dy][x + dx] != opponent:
            return []

        y += dy
        x += dx
        # self._board[y][x] now is opponent's color
        flips_so_far = [(y, x)]
        while self._is_on_board((y, x)) and self._board[y][x] == opponent:
            y += dy
            x += dx
            flips_so_far.append((y, x))

        if not self._is_on_board((y, x)):
            return []
        elif self._board[y][x] == player:
            return flips_so_far
        else:
            return []

    def _is_on_board(self, pos: tuple[int, int]) -> bool:
        """Return whether coordinates in array indices pos is a valid position on the game board

        :param pos: coordinates in array indices
        """
        return 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7


def _algebraic_to_index(move: str) -> tuple[int, int]:
    """Convert coordinates in algebraic format ex. 'a2' to array indices (y, x).

    Preconditions:
        - move[0] in _FILE_TO_INDEX
        - move[1] in _RANK_TO_INDEX

    :param move: coordinates in algebraic format
    """
    return (_RANK_TO_INDEX[move[1]], _FILE_TO_INDEX[move[0]])


def _index_to_algebraic(pos: tuple[int, int]) -> str:
    """Convert coordinates in array indices (y, x) to algebraic format.

    Preconditions:
        - pos[0] in _FILE_TO_INDEX
        - pos[1] in _RANK_TO_INDEX

    :param pos: coordinates in array indices
    """
    return _INDEX_TO_FILE[pos[1]] + _INDEX_TO_RANK[pos[0]]
