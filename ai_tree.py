"""This file implements simple trees for testing writing tree into file.

"""
from __future__ import annotations

from typing import Any, Optional, TextIO

GAME_START_MOVE = '*'


class AIGameTree:
    """This game tree class has special functions that can write tree into file or load a tree
    from file.

    attributes:
        - move: a move is a string like 'a2' or 'pass' that corresponds to a coordinate on chess
        board or a pass.
        - white_move: true for white is going to make the next move, false for black is going to
        make the next move.
        - white_win_probability: the statistic probability for white to win this game.

    """
    move: str
    is_white_move: bool
    _subtrees: list[AIGameTree]
    white_win_probability: float

    def __init__(self, move: str = GAME_START_MOVE,
                 is_white_move: bool = True, white_win_probability: Optional[float] = 0) -> None:
        """Initialize a new game tree.

        """
        self.move = move
        self.is_white_move = is_white_move
        self._subtrees = []
        self.white_win_probability = white_win_probability

    def get_subtrees(self) -> list[AIGameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def add_subtree(self, subtree: AIGameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)
        # self._update_white_win_probability()

    def is_empty(self) -> bool:
        """Return whether this tree object is empty (move is None)."""
        if self.move is None:
            return True
        else:
            return False

    def get_height(self) -> int:
        """Return the height of this tree object."""
        if self.is_empty():
            return 0
        max_h = 0
        for sub in self._subtrees:
            sub_h = sub.get_height()
            if max_h < sub_h:
                max_h = sub_h
        return 1 + max_h

    def get_trees_from_level(self, level: int) -> list[AIGameTree]:
        """This function returns all subtrees of a specific level of the tree.
        This corresponds to the game steps (level = number of moves)
        Level: the root is considered level 0;
        """
        subtrees = []
        if level == 0:
            return [self]
        for sub in self._subtrees:
            subtrees.extend(sub.get_trees_from_level(level - 1))
        return subtrees

    def write_tree_to_file(self, file_name: str) -> None:
        """This writes the tree object in specific format into a file which can then be loaded.
        This function creates the file if the file does not exist yet.
        Note that this overrides any previous content in the given file, if existed.
        Rules:
            - trees of the same level are writen on one line.
            - each line (not extension) has format "<level>:<previous1>[<tree1>;<tree2>;<tree3>;
            <...>;],<previous2>[<tree1>;<tree2>;<tree3>;<...>;]\n"
            - each tree has format "<move>,<win_probability>(subtree1,subtree2,...)".
        """
        output_file = open(file_name, mode='w')

        start_line = '0:' + GAME_START_MOVE + ',('
        for i in range(0, len(self._subtrees)):
            if i == len(self._subtrees) - 1:
                start_line += self._subtrees[i].move
            else:
                start_line += self._subtrees[i].move + ','
        start_line += ');\n'
        output_file.write(start_line)

        height = self.get_height()
        for i in range(1, height):
            output_file.write(str(i) + ':')
            all_previous = self.get_trees_from_level(i - 1)
            for previous in range(0, len(all_previous)):
                output_file.write(all_previous[previous].move + '[')
                for sub in range(0, len(all_previous[previous]._subtrees)):
                    all_previous[previous]._subtrees[sub]._write_a_tree(output_file)
                    if sub != len(all_previous[previous]._subtrees) - 1:
                        output_file.write(';')
                if previous == len(all_previous) - 1:
                    output_file.write(']')
                else:
                    output_file.write('],')
            output_file.write('\n')
        return

    def _write_a_tree(self, file_pointer: TextIO) -> None:
        """Write a tree in format specified above."""
        line = self.move + ',('
        for i in range(0, len(self._subtrees)):
            if i == len(self._subtrees) - 1:
                line += self._subtrees[i].move
            else:
                line += self._subtrees[i].move + ','
        line += ')'
        file_pointer.write(line)
        return

    # def add_move_to_file(self, tree()):
    #     """"""
    @staticmethod
    def substring_by_notation(line: str, notation: str, front: bool) -> str:
        """Function to separate words from a line of using certain notation, if front is true, get the
        part before the first appearance of that notation, if false, get the later part (both not
        including the notation itself).
        This raise ValueError if notation is not in the string.
        """
        index = line.index(notation)
        if front:
            return line[:index]
        elif line[-1] == '\n':
            return line[index + 1: len(line) - 1]
        else:
            return line[index + 1:]

