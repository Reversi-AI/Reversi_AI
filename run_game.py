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

from constants import BLACK, WHITE
from reversi import ReversiGame, Player, RandomPlayer, ConsoleUserPlayer
from minimax import GreedyPlayer, PositionalPlayer, MobilityPlayer


def run_games_ai(player1: Player, player2: Player, n: int, size: int) -> None:
    """Run n games using the given Players.

    Preconditions:
        - n >= 1
    """
    stats = {'P1': 0, 'P2': 0, 'Draw': 0}
    results = []
    for i in range(0, n):
        # switch black and white every turn
        if i % 2:  # p1 black, p2 white
            black_copy = copy.deepcopy(player1)
            white_copy = copy.deepcopy(player2)
            winner, _ = run_game(black_copy, white_copy, size)
            print(f'Game {i}, P1 as {BLACK}, P2 as {WHITE}, ', end='')

            if winner == BLACK:
                win_player = 'P1'
            elif winner == WHITE:
                win_player = 'P2'
            else:
                win_player = 'Draw'

        else:  # p2 black, p1 white
            black_copy = copy.deepcopy(player2)
            white_copy = copy.deepcopy(player1)
            winner, _ = run_game(black_copy, white_copy, size)
            print(f'Game {i}, P1 as {WHITE}, P2 as {BLACK}, ', end='')

            if winner == BLACK:
                win_player = 'P2'
            elif winner == WHITE:
                win_player = 'P1'
            else:
                win_player = 'Draw'

        stats[win_player] += 1
        results.append(win_player)
        print(f'Winner: {win_player}')

    for outcome in stats:
        print(f'{outcome}: {stats[outcome]}/{n} ({100.0 * stats[outcome] / n:.2f}%)')


def run_game(black: Player, white: Player, size: int,
             verbose: bool = False) -> tuple[str, list[str]]:
    """Run a Reversi game between the two given players.

    Return the winner and list of moves made in the game.
    """
    game = ReversiGame(size)

    move_sequence = []
    previous_move = None
    current_player = black

    if verbose:
        game.print_game()

    while game.get_winner() is None:
        previous_move = current_player.make_move(game, previous_move)

        game.make_move(previous_move)
        move_sequence.append(previous_move)
        if verbose:
            if current_player is black:
                print(f'{BLACK} moved {previous_move}')
            else:
                print(f'{WHITE} moved {previous_move}')
            game.print_game()

        if current_player is black:
            current_player = white
        else:
            current_player = black

    return game.get_winner(), move_sequence


if __name__ == '__main__':
    run_games_ai(player1=PositionalPlayer(3),
                 player2=MobilityPlayer(3),
                 n=100, size=6)
    # result = run_game(MobilityPlayer(5), PositionalPlayer(6), 6, True)
    # print(result)
