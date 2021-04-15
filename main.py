"""main.py

Module Description
===============================
This module is the main file of our project. Running the original
version of the file would open the GUI of Reversi which includes
players vs player, player vs computer and computer vs computer mode.

Simulations between AIs of a given number of games can be viewed by
uncommented lines of code in the main branch.
===============================
Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway
This file is Copyright (c) 2021.
"""
from tk_gui import run_app
from run_game import run_games_ai
from minimax_tree import GreedyTreePlayer, PositionalTreePlayer, MobilityTreePlayer
from mcts import MCTSTimeSavingPlayer

if __name__ == '__main__':
    # creates interactive reversi GUI in which
    # the depth of the minimax AI is 3 and
    # MCTS player takes 100 rounds of mcts and a time limit of 1 second per turn
    run_app(minimax_depth=3, mcts_param=(100, 1))

    ###########################################################
    # AI performance evaluation
    # comment out the previous function call of the app and
    # uncomment one of the following function call to view AI simulation

    # You can change the parameter of the minimax players to change the depth of the algorithm.

    # You can change the first parameter of the MCTS player to change the number of mcts calls
    # performed for each move. You can also change the second parameter of the MCTS player to
    # change the time limit per move.

    # You can change the value of n to change the number of game being played
    # You can change the value of size to switch between 6x6 and 8x8

    # minimax players
    # run_games_ai(GreedyTreePlayer(3), PositionalTreePlayer(3), n=100, size=6, show_stats=True)
    # run_games_ai(GreedyTreePlayer(3), MobilityTreePlayer(3), n=100, size=6, show_stats=True)
    # run_games_ai(PositionalTreePlayer(3), MobilityTreePlayer(3), n=100, size=6, show_stats=True)

    # mcts vs minimax
    # run_games_ai(MCTSTimeSavingPlayer(100, 1), GreedyTreePlayer(3), n=100, size=6, show_stats=True)
    # run_games_ai(MCTSTimeSavingPlayer(100, 1), PositionalTreePlayer(3), n=100, size=6, show_stats=True)
    # run_games_ai(MCTSTimeSavingPlayer(100, 1), MobilityTreePlayer(3), n=100, size=6, show_stats=True)
