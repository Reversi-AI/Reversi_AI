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
import time

from constants import BLACK, WHITE
from reversi import ReversiGame, Player, RandomPlayer, ConsoleUserPlayer
from minimax import GreedyPlayer, PositionalPlayer, MobilityPlayer
import tkinter as tk
from visualize import ReversiApplication


def run_games_visual(player1: Player, player2: Player, n: int, size: int) -> None:
    """Run n reversi games using the given players and show a visual"""
    root = tk.Tk()
    window = ReversiApplication(master=root)
    # window.after(1000, run_games_ai(player1, player2, 1, size, window))
    window.mainloop()


def run_games_ai(player1: Player, player2: Player, n: int, size: int, visualizer=None) -> None:
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
            winner, _ = run_game(black_copy, white_copy, size, visualizer=visualizer)
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
             verbose: bool = False, visualizer=None) -> tuple[str, list[str]]:
    """Run a Reversi game between the two given players.

    Return the winner and list of moves made in the game.
    """
    game = ReversiGame(size)

    move_sequence = []
    previous_move = None
    timer = {BLACK: 0, WHITE: 0}
    current_player = black

    if verbose:
        game.print_game()

    while game.get_winner() is None:
        t0 = time.time()  # record time before player make move
        previous_move = current_player.make_move(game, previous_move)
        t = time.time()  # record time after player make move

        if visualizer is not None:
            visualizer.draw_game_state(game, 500, 500)

        game.make_move(previous_move)
        move_sequence.append(previous_move)
        if verbose:
            if current_player is black:
                print(f'{BLACK} moved {previous_move}. Used {t - t0:.2f}s')
            else:
                print(f'{WHITE} moved {previous_move}. Used {t - t0:.2f}s')
            game.print_game()

        if current_player is black:
            timer[BLACK] += t - t0
            current_player = white
        else:
            timer[WHITE] += t - t0
            current_player = black

    # print winner
    if verbose:
        print(f'Winner: {game.get_winner()}')
        print(f'{BLACK}: {game.get_num_pieces()[BLACK]}, {WHITE}: {game.get_num_pieces()[WHITE]}')
        print(f'{BLACK} used {timer[BLACK]:.2f}s, {WHITE} used {timer[WHITE]:.2f}s')

    return game.get_winner(), move_sequence


if __name__ == '__main__':
    # run_games_ai(player1=MobilityPlayer(3),
    #              player2=PositionalPlayer(3),
    #              n=100, size=8)
    # result = run_game(MobilityPlayer(4), PositionalPlayer(4), 8, True)
    run_games_visual(MobilityPlayer(4), PositionalPlayer(4), n=1, size=8)
