"""Run Reversi game

Module Description
===============================

This module contains a collection of functions which conduct game plays of Reversi.

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""
import copy

from pieces import _BLACK, _WHITE
from reversi import ReversiGame, Player, RandomPlayer
from minimax import GreedyPlayer


def run_games_ai(black: Player, white: Player, n: int) -> None:
    """Run n games using the given Players.

    Preconditions:
        - n >= 1
    """
    stats = {_BLACK: 0, _WHITE: 0, 'Draw': 0}
    results = []
    for i in range(0, n):
        black_copy = copy.deepcopy(black)
        white_copy = copy.deepcopy(white)

        winner, _ = run_game_ai(black_copy, white_copy)
        stats[winner] += 1
        results.append(winner)

        print(f'Game {i} winner: {winner}')

    for outcome in stats:
        print(f'{outcome}: {stats[outcome]}/{n} ({100.0 * stats[outcome] / n:.2f}%)')


def run_game_ai(black: Player, white: Player, verbose: bool = False) -> tuple[str, list[str]]:
    """Run a Reversi game between the two given players.

    Return the winner and list of moves made in the game.
    """
    game = ReversiGame()

    move_sequence = []
    previous_move = None
    current_player = black

    while game.get_winner() is None:
        previous_move = current_player.make_move(game, previous_move)
        game.make_move(previous_move)
        move_sequence.append(previous_move)

        if current_player is black:
            current_player = white
        else:
            current_player = black

        if verbose:
            game.print_game()

    return game.get_winner(), move_sequence


if __name__ == '__main__':
    black_player = GreedyPlayer(3)
    white_player = RandomPlayer()

    run_games_ai(black_player, white_player, 100)