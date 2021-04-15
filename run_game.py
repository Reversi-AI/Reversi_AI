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

import tkinter as tk
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simple_tk_gui import ReversiVisualizer
from constants import BLACK, WHITE, DEFAULT_FPS
from reversi import ReversiGame, Player


def run_game_visual(player1: Player, player2: Player, size: int, fps: int = DEFAULT_FPS) -> None:
    """Run a reversi game using the given players and show a visual"""
    root = tk.Tk()
    gui = ReversiVisualizer(root, size=size)
    gui.run_game(player1, player2, fps)
    root.mainloop()


def run_games_ai(player1: Player, player2: Player, n: int, size: int,
                 show_stats: bool = False) -> None:
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

    if show_stats:
        plot_game_statistics(results)


def run_game(black: Player, white: Player, size: int,
             verbose: bool = False) -> tuple[str, list[str]]:
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


def plot_game_statistics(results: list[str]) -> None:
    """Plot the outcomes and win probabilities for a given list of Reversi game results.
    This function is originally part of CSC111 Assignment 2 and has been adapted for Reversi.
    Preconditions:
        - all(r in {'White', 'Black', 'Draw'} for r in results)
    """
    outcomes_p1 = [1 if result == 'P1' else 0 for result in results]
    outcomes_p2 = [1 if result == 'P2' else 0 for result in results]

    p1_cumulative_win_probability = [sum(outcomes_p1[0:i]) / i for i in range(1,
                                                                              len(outcomes_p1) + 1)]
    p2_cumulative_win_probability = [sum(outcomes_p2[0:i]) / i for i in range(1,
                                                                              len(outcomes_p2) + 1)]

    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Scatter(y=p1_cumulative_win_probability, mode='lines',
                             name='Player1 win percentage (cumulative)'),
                  row=1, col=1)
    fig.add_trace(go.Scatter(y=p2_cumulative_win_probability, mode='lines',
                             name='Player2 win percentage (cumulative)'),
                  row=1, col=1)
    fig.update_yaxes(range=[0.0, 1.0], row=1, col=1)

    fig.update_layout(title='Reversi Game Results', xaxis_title='Game')
    fig.show()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'time', 'old_tk_gui', 'copy', 'plotly', 'minimax_tree',
                          'constants', 'simple_tk_gui', 'plotly.graph_objects', 'plotly.subplots',
                          'reversi'],
        'allowed-io': ['run_game', 'run_games_ai'],
        'max-line-length': 100,
        'disable': ['E1136', 'R0913']
    })
