"""Pieces representation

Module Description
===============================

This module contains three constants which are used for representing pieces on the board.

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""

# representation of pieces on the board
EMPTY = '_'
BLACK = 'X'
WHITE = 'O'

# representation of the weights used in the evaluation of PositionalPlayer
BOARD_WEIGHT_8 = [[100, -20, 10, 5, 5, 10, -20, 100],
                  [-20, -50, -2, -2, -2, -2, -50, -20],
                  [10, -2, -1, -1, -1, -1, -2, 10],
                  [5, -2, -1, -1, -1, -1, -2, 5],
                  [5, -2, -1, -1, -1, -1, -2, 5],
                  [10, -2, -1, -1, -1, -1, -2, 10],
                  [-20, -50, -2, -2, -2, -2, -50, -20],
                  [100, -20, 10, 5, 5, 10, -20, 100]]

BOARD_WEIGHT_6 = [[100, -20, 10, 10, -20, 100],
                  [-20, -50, -2, -2, -50, -20],
                  [10,  -2,  -1, -1, -2,  -10],
                  [5,   -2,  -1, -1, -2,  -5],
                  [10, -2, -1, -1, -2, -10],
                  [-20, -50, -2, -2, -50, -20],
                  [100, -20, 10, 10, -20, 100]]

# representation of the initial states of the game in game_tree
START_MOVE = '*'

# Default fps for game display
DEFAULT_FPS = 30
