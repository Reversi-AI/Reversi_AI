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

# mapping used for converting move between algebraic and index
COL_TO_INDEX = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
INDEX_TO_COL = {i: f for f, i in COL_TO_INDEX.items()}
ROW_TO_INDEX = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
INDEX_TO_ROW = {i: r for r, i in ROW_TO_INDEX.items()}


# functions used for converting move between algebraic and index
def algebraic_to_index(move: str) -> tuple[int, int]:
    """Convert coordinates in algebraic format ex. 'a2' to array indices (y, x).

    Preconditions:
        - move[0] in _COL_TO_INDEX
        - move[1] in _ROW_TO_INDEX

    :param move: coordinates in algebraic format
    """
    return (ROW_TO_INDEX[move[1]], COL_TO_INDEX[move[0]])


def index_to_algebraic(pos: tuple[int, int]) -> str:
    """Convert coordinates in array indices (y, x) to algebraic format.

    Preconditions:
        - pos[0] in _COL_TO_INDEX
        - pos[1] in _ROW_TO_INDEX

    :param pos: coordinates in array indices
    """
    return INDEX_TO_COL[pos[1]] + INDEX_TO_ROW[pos[0]]


# representation of the weights used in the evaluation of PositionalPlayer
BOARD_WEIGHT_8 = [[10, -5, 5, 5, 5, 5, -5, 10],
                  [-5, -8, -2, -2, -2, -2, -8, -5],
                  [5, -2, -1, -1, -1, -1, -2, 5],
                  [5, -2, -1, 0, 0, -1, -2, 5],
                  [5, -2, -1, 0, 0, -1, -2, 5],
                  [5, -2, -1, -1, -1, -1, -2, 5],
                  [-5, -8, -2, -2, -2, -2, -8, -5],
                  [10, -5, 5, 5, 5, 5, -5, 10]]

BOARD_WEIGHT_6 = [[10, -5, 5, 5, -5, 10],
                  [-5, -8, -2, -2, -8, -5],
                  [5, -2, 0, 0, -2, 5],
                  [5, -2, 0, 0, -2, 5],
                  [-5, -8, -2, -2, -8, -5],
                  [10, -5, 5, 5, -5, 10]]

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

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
