"""Pieces representation

Module Description
===============================

This module contains constants which are used for representing pieces on the board.

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
                  [10, -2, -1, -1, -2, -10],
                  [-20, -50, -2, -2, -50, -20],
                  [100, -20, 10, 10, -20, 100]]

# representation of positions on the game board
BOARD_POSITION_8 = {'corners': {'a1', 'a8', 'h1', 'h8'},
                    'edges': {'a3', 'a4', 'a5', 'a6',
                              'c1', 'd1', 'e1', 'f1',
                              'c8', 'd8', 'e8', 'f8',
                              'h3', 'h4', 'h5', 'h6'},
                    'buffers': {'b1', 'b2', 'a2', 'g1', 'g2', 'h2',
                                'b7', 'b8', 'a7', 'g7', 'g8', 'h7'}}

BOARD_POSITION_6 = {'corners': {'a1', 'a6', 'f1', 'f6'},
                    'edges': {'a3', 'a4', 'c1', 'd1', 'c6', 'd6', 'f3', 'f4'},
                    'buffers': {'b1', 'b2', 'a2', 'e1', 'e2', 'f2',
                                'b5', 'b6', 'a5', 'e5', 'e6', 'f5'}}

# representation of the initial states of the game in game_tree
START_MOVE = '*'

# Default fps for game display
DEFAULT_FPS = 30
