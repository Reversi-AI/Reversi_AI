"""Running the game of Reversi

Module Description
===============================

This module contains functions that manipulate classes in other modules to run the game of Reversi

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


def run_games(n: int, white: Player, black: Player) -> None:
    """Run n games using the given Players.

    Preconditions:
        - n >= 1
    """
    stats = {'White': 0, 'Black': 0, 'Draw': 0}
    results = []
    for i in range(0, n):
        white_copy = copy.deepcopy(white)
        black_copy = copy.deepcopy(black)

        winner, _ = run_game(white_copy, black_copy)
        stats[winner] += 1
        results.append(winner)

        print(f'Game {i} winner: {winner}')

    for outcome in stats:
        print(f'{outcome}: {stats[outcome]}/{n} ({100.0 * stats[outcome] / n:.2f}%)')


def run_game(white: Player, black: Player, verbose: bool = False) -> tuple[str, list[str]]:
    """Run a Reversi game between the two given players.

    Return the winner and list of moves made in the game.
    """
    game = ReversiGame()

    move_sequence = []
    previous_move = None
    current_player = white
    while game.get_winner() is None:

        previous_move = current_player.make_move(game, previous_move)
        game.make_move(previous_move)
        move_sequence.append(previous_move)

        if current_player is white:
            current_player = black
        else:
            current_player = white

        if verbose:
            game.print_game_board()

    return game.get_winner(), move_sequence
