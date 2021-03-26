"""Elementary player classes

Module Description
===============================

This module contains two class that represents a human player integrating with the console 
and a RandomAI player making random moves in the game

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

import random


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
    """A Reversi AI who always picks a random move."""

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
