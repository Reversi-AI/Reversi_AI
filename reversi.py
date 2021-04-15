"""ReversiGame class

Module Description
===============================

This module is an object oriented implementation of Reversi.
It contains a collection of classes that represents the game of Reversi.

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

from typing import Optional
import copy
import random

from constants import BLACK, WHITE, EMPTY, algebraic_to_index, index_to_algebraic

################################################################################
# Class representing Reversi
################################################################################
# mapping used for converting move between algebraic and index
_COL_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
_INDEX_TO_COL = {i: f for f, i in _COL_TO_INDEX.items()}
_ROW_TO_INDEX = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
_INDEX_TO_ROW = {i: r for r, i in _ROW_TO_INDEX.items()}


class ReversiGame:
    """A class representing a state of a game of Reversi.
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional nested list representing a Reversi board
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _turn: a str representing which piece is going to play next
    #   - _num_pieces: a dictionary representing the number of pieces of either side

    # Representation Invariants:
    #   - len(self_board) == 8 or len(self_board) == 8
    #   - all(len(row) == 8 for row in self._board)
    #   - all elements in the inner lists of self._board is in {EMPTY, BLACK, WHITE}
    #   - self._turn in {BLACK, WHITE}
    _board: list[list[str]]
    _valid_moves: list[str]
    _turn: str
    _num_pieces: dict[str, int]
    _size: int

    def __init__(self, size: int) -> None:
        """Initialize a game with the given state. The board is empty if board is None.

        Representation Invariants:
            - board is None or len(_board) == 8 or len(_board) == 6
            - board is None or all(len(row) == 8 for row in _board)
            - board is None or every element in the inner lists of _board is in
            {EMPTY, BLACK, WHITE}
            - turn in {BLACK, WHITE}

        Precondition:
            - size in {6, 8}    # ValueError if this is not met
        """
        self._size = size
        self._board = []

        if size in (8, 6):
            # create an empty size * size board
            for _ in range(size):
                self._board.append([EMPTY] * size)

            # calculate center coordinates
            top_left_y, top_left_x = size // 2 - 1, size // 2 - 1
            top_right_y, top_right_x = top_left_y, top_left_x + 1
            bottom_left_y, bottom_left_x = top_left_y + 1, top_left_x
            bottom_right_y, bottom_right_x = top_left_y + 1, top_left_x + 1

            # place 2 black and 2 white pieces on the center
            self._board[top_left_y][top_left_x] = WHITE
            self._board[top_right_y][top_right_x] = BLACK
            self._board[bottom_left_y][bottom_left_x] = BLACK
            self._board[bottom_right_y][bottom_right_x] = WHITE

            # update other attributes
            self._turn = BLACK
            self._num_pieces = {BLACK: 2, WHITE: 2}
            self._valid_moves = self._calculate_valid_moves(self._turn)

        else:
            raise ValueError

    def get_game_board(self) -> list[list[str]]:
        """Return the nested list representing the current board state

        :return: a nested list representing the current board state
        """
        return self._board

    def get_board_size(self) -> int:
        """return the size of the board

        :return: the size of the board
        """
        return self._size

    def get_valid_moves(self) -> list[str]:
        """Return a list of the valid moves for the active player

        :return: list of valid moves
        """
        return self._valid_moves

    def get_current_player(self) -> str:
        """Return which player is going to play next

        :return: a string representing which player will play next
        """
        return self._turn

    def print_game(self) -> None:
        """Output the current game state on the console

        :return: None
        """
        print('*' * 26)

        print(f'{BLACK}: {self._num_pieces[BLACK]}, {WHITE}: {self._num_pieces[WHITE]}')
        print(f"{self._turn}'s turn")

        if self._size == 8:
            header = 'abcdefgh'
        else:
            header = 'abcdef'
        print('   ' + '  '.join(list(header)))

        for i in range(len(self._board)):
            print(f'{i + 1}  ' + '  '.join(self._board[i]))

        print('*' * 26)

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
        self._valid_moves = self._calculate_valid_moves(self._turn)

    def _next_player(self) -> None:
        """Mutate self.turn to the next player"""
        if self._turn == BLACK:
            self._turn = WHITE
        else:
            self._turn = BLACK

    def simulate_move(self, move: str) -> ReversiGame:
        """Make the given move in a copy of self, and return the copy after the move is made.
        This method does not mutate the current instance.
        If move is not a currently valid move, raise a ValueError.

        :param move: the move to be made
        :return: a copy of the game state after the move is made
        """
        copy_state = copy.deepcopy(self)
        copy_state.make_move(move)
        return copy_state

    def get_num_pieces(self) -> dict[str, int]:
        """Return the number of piece of each color on the board.

        :return: a dictionary representing the number of pieces on each side
        """
        return self._num_pieces

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.

        :return: winner of the game (Black or White) or 'Draw' if the game ended in a draw.
        None if the game is not over.
        """
        if self._calculate_valid_moves(BLACK) == ['pass'] \
                and self._calculate_valid_moves(WHITE) == ['pass']:
            num_black, num_white = self._num_pieces[BLACK], self._num_pieces[WHITE]
            if num_black > num_white:
                return BLACK
            elif num_white == num_black:
                return 'Draw'
            else:
                return WHITE
        else:
            return None

    def get_size(self) -> int:
        """getter method for self._size"""
        return self._size

    def _update_board(self, turn: str, move: str) -> None:
        """Mutate self._board after the given player made the move. Note that move can be 'pass'

        Preconditions:
            - move is currently a legal move for the active player.

        """
        if move != 'pass':
            # replace move position to the active player's piece
            y_move, x_move = algebraic_to_index(move)
            self._board[y_move][x_move] = turn

            # flip all the pieces that could be flipped
            flips_so_far = []
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for direction in directions:
                flips_so_far.extend(self._check_flips(turn, move, direction))
            for y, x in flips_so_far:
                self._board[y][x] = turn

            # update num pieces attribute
            if turn == BLACK:
                self._num_pieces[BLACK] += 1  # newly placed
                self._num_pieces[BLACK] += len(flips_so_far)  # pieces gained from flip
                self._num_pieces[WHITE] -= len(flips_so_far)  # pieces lost from flip
            else:
                self._num_pieces[WHITE] += 1
                self._num_pieces[WHITE] += len(flips_so_far)
                self._num_pieces[BLACK] -= len(flips_so_far)

    def _calculate_valid_moves(self, turn: str) -> list[str]:
        """Return all valid moves for the current board state for a given active player

        Preconditions:
            - turn in {BLACK, WHITE}

        :param turn: the active player making the move
        :return: None
        """
        valid_moves_so_far = []

        # check every position for valid move
        for y in range(len(self._board)):
            for x in range(len(self._board)):
                move = index_to_algebraic((y, x))
                if self._is_valid_move(turn, move):
                    valid_moves_so_far.append(move)

        # valid move is only pass when no valid moves
        if len(valid_moves_so_far) == 0:  # no valid moves
            valid_moves_so_far.append('pass')

        return valid_moves_so_far

    def _is_valid_move(self, player: str, move: str) -> bool:
        """Return whether the given move is valid for the given player.

         Preconditions:
            - player in {BLACK, WHITE}
            - move is a coordinate on the board

        :param player: the player making the move
        :param move: the move being made
        :return: whether the given move is valid for the given player
        """
        # turn algebraic coordinate to array index
        y, x = algebraic_to_index(move)

        # when that position is occupied, the move is invalid
        if self._board[y][x] != EMPTY:
            return False

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (-1, 1), (1, -1), (-1, -1)]

        # check all directions, if there is a flip, it is a valid move
        for direction in directions:
            if len(self._check_flips(player, move, direction)) != 0:
                return True

        # no flips if the function reaches this point, so the move is invalid
        return False

    def _check_flips(self, player: str, move: str, direction: tuple) -> list[tuple[int, int]]:
        """Assume the player plays a given move, check the given direction for which pieces
        can be flipped.

        direction[0] represents dy which is the proceeding direction of y.
        direction[1] represents dx which is the proceeding direction of x.
        For example, if player = BLACK, move = 'c4', direction =(0, 1), the function would
        return a list of positions of white pieces that can be flipped on the right of c4

        Preconditions:
            - The square of move is empty
            - player in {BLACK, WHITE}
            - direction[0] in {-1, 0, 1}
            - direction[1] in {-1, 0, 1}

        :param player: the player playing the move
        :param move: the move begin played
        :param direction: the direction to be checked for flips
        """
        # process input
        y, x = algebraic_to_index(move)
        dy, dx = direction

        # identify player pieces and opponent pieces
        if player == BLACK:
            opponent = WHITE
        else:
            opponent = BLACK

        # check for special cases
        if not self._is_on_board((y + dy, x + dx)):  # reach boarder in one step
            return []
        if not self._is_on_board((y + dy + dy, x + dx + dx)):  # reach boarder in two steps
            return []
        if self._board[y + dy][x + dx] != opponent:  # adjacent to player pieces in that direction
            return []

        assert 0 <= y + dy + dy <= self._size - 1
        assert 0 <= x + dx + dx <= self._size - 1

        y += dy
        x += dx
        assert self._board[y][x] == opponent

        flips_so_far = []
        while self._is_on_board((y, x)) and self._board[y][x] == opponent:
            flips_so_far.append((y, x))
            y += dy
            x += dx

        # determine what terminates the loop
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
        return 0 <= pos[0] <= self._size - 1 and 0 <= pos[1] <= self._size - 1


################################################################################
# Player classes
################################################################################
class Player:
    """An abstract class representing a Reversi player.

    This class can be subclassed to implement different strategies for playing Reversi.
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
    """A human player using the console for interaction."""

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> Optional[str]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return:
            - 'quit' if player wants to quit the game
            - a valid move in algebraic coordinate
        """
        move = None
        while move not in game.get_valid_moves():
            if move == 'quit':
                return 'quit'
            if move == 'view':
                view_valid_moves(game)
            print('Enter "quit" if you want to quit')
            print('Enter "view" if you want to view valid moves')
            move = input('Please enter your move')
        return move


def view_valid_moves(game: ReversiGame) -> None:
    """Output all valid moves for the current game state in the console

    Preconditions:
        - There is at least one valid move for the given game state

    :param game: the current game state
    """
    print(f'Valid moves are/is {str(game.get_valid_moves())[1: -1]}')


class RandomPlayer(Player):
    """A Reversi AI player who always picks a random move."""

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        possible_moves = game.get_valid_moves()
        return random.choice(possible_moves)


class GUIPlayer(Player):
    """A human player interacting with a GUI"""

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Tells the game to use the mouse position on the board"""
        moves = game.get_valid_moves()
        if moves == ['pass']:  # the only move is pass
            return 'pass'
        return 'mouse_pos'


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.check_all_contracts()
    python_ta.check_all(config={
        'extra-imports': ['typing', 'copy', 'random', 'constants'],
        'allowed-io': ['view_valid_moves', 'print_game', 'view_valid_moves', 'make_move'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
