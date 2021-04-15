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

if __name__ == '__main__':
    run_app()
