"""Game tree class

Module Description
===============================

This module contains a collection of classes representing a game tree of Reversi

Copyright and Usage Information
===============================

Authors:
    - Haoze Deng
    - Peifeng Zhang
    - Man Chon Ho
    - Alexander Nicholas Conway

This file is Copyright (c) 2021.
"""
from __future__ import annotations
from typing import Optional, Union
import copy
import random
import math
import pickle
import time

from constants import BLACK, WHITE, START_MOVE
from reversi import ReversiGame, Player


class MCTSTree:
    """A decision tree generated with MCTS for Reversi

    Instance Attributes:
        - move: a valid move from the previous game state, or START_MOVE if the node
                represents the start of the game
        - simulations: the winner of the simulations run on the node


    Representation Invariants:
        - self.move == START_MOVE or self.move is a valid move in Reversi
        - self.move != START_MOVE or self.game_after_move.get_current_player() == BLACK
    """
    move: str
    simulations: dict[str, int]

    # Private Instance Attributes:
    #   - _game_after_move: a ReversiGame class representing the game state after the move
    #   - _children: the child nodes of the current node"""
    _game_after_move: ReversiGame
    _subtrees: list[MCTSTree]

    def __init__(self, move: str, game_after_move: ReversiGame) -> None:
        self.move = move
        self._game_after_move = game_after_move
        self.simulations = {BLACK: 0, WHITE: 0, 'Draw': 0}
        self._subtrees = []

    def get_game_after_move(self) -> ReversiGame:
        """Getter method of _game_after_move"""
        return self._game_after_move

    def get_subtrees(self) -> list[MCTSTree]:
        """Getter method of _subtrees"""
        return self._subtrees

    def find_subtree_by_move(self, move: str) -> Optional[MCTSTree]:
        """Return the subtree corresponding to the given move.

        Raise ValueError if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree
        raise ValueError

    def get_most_confident_move(self) -> str:
        """Return the move of the subtree that has been simulated for the most number of time

        Return the leftmost one if tie
        """
        most_simulated = max(self._subtrees, key=lambda subtree: sum(subtree.simulations.values()))
        return most_simulated.move

    def get_total_simulation_number(self) -> int:
        """Return the number of simulation run on this node"""
        return sum(self.simulations.values())

    def mcts_round(self, c: Union[int, float]) -> None:
        """Perform one round of MCTS with the given exploration parameter

        :param c: the exploration parameter
        """
        side = self._game_after_move.get_current_player()

        # selection
        selected_leaf, path = self.select(side, c, [self])
        assert len(selected_leaf._subtrees) == 0

        # check if the selected node is terminal
        if selected_leaf._game_after_move.get_winner() is None:
            # do expansion before rollout if the selected node is revisited
            if sum(selected_leaf.simulations.values()) != 0:
                selected_leaf.expand()
                assert len(selected_leaf._subtrees) > 0
                selected_leaf = selected_leaf._subtrees[0]
                path.append(selected_leaf)

            # rollout on the selected node and update the path with the result
            rollout_winner = selected_leaf.rollout()
            self.update(rollout_winner, path)
        else:  # update the path directly when the node is terminal
            self.update(selected_leaf._game_after_move.get_winner(), path)

    def select(self, side: str, c: Union[int, float], path: list) \
            -> tuple[MCTSTree, list[MCTSTree]]:
        """Selection process of the MCTS. Return the selected leaf and
        the path to the leaf

        Preconditions:
            - side in {BLACK, WHITE}

        :param side: the piece played by the player
        :param c: the exploration parameter
        :param path: the path from root to the current node
        """
        if self._subtrees == []:
            return (self, path)
        else:
            n_total = self.get_total_simulation_number()

            max_ucb_value_so_far = -math.inf
            max_ucb_subtree_so_far = None
            for subtree in self._subtrees:
                if subtree.get_total_simulation_number() == 0:
                    max_ucb_subtree_so_far = subtree
                    break
                else:
                    if subtree._uct(side, c, n_total) > max_ucb_value_so_far:
                        max_ucb_subtree_so_far = subtree
                        max_ucb_value_so_far = subtree._uct(side, c, n_total)

            path.append(max_ucb_subtree_so_far)
            return max_ucb_subtree_so_far.select(side, c, path)

    def _uct(self, side: str, c: Union[int, float], n_total: int) -> float:
        """Return the value calculated by UCB1 formula of the node.

        Precondition:
            - self.get_total_simulation_number != 0

        Preconditions:
            - side in {BLACK, WHITE}

        :param side: the piece played by the player
        :param c: the exploration parameter
        :param n_total: the total number of simulations run by the parent node
        """
        w = self.simulations[side] + 0.5 * self.simulations['Draw']
        n = self.get_total_simulation_number()
        return w / n + c * math.sqrt(math.log(n_total) / n)

    def expand(self) -> None:
        """Expansion process of the MCTS".

        Preconditions:
            - self._game_after_move.get_winner() is None
            - self._subtree == []
        """
        valid_moves = self._game_after_move.get_valid_moves()
        for move in valid_moves:
            new_game_state = self._game_after_move.simulate_move(move)
            new_subtree = MCTSTree(move, new_game_state)
            self._subtrees.append(new_subtree)

    def rollout(self) -> str:
        """Rollout process of the MCTS. Return the winner of the rollout"""
        game_copy = copy.deepcopy(self._game_after_move)
        while game_copy.get_winner() is None:
            random_move = random.choice(game_copy.get_valid_moves())
            game_copy.make_move(random_move)
        return game_copy.get_winner()

    def update(self, winner: str, path: list[MCTSTree]) -> None:
        """Back propagation process of the MCTS

        Preconditions:
            - winner in {BLACK, WHITE, 'Draw'}
        Raise ValueError if the preconditions are not met
        """
        if winner not in {BLACK, WHITE, 'Draw'}:
            raise ValueError

        for node in path:
            node.simulations[winner] += 1

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self._game_after_move.get_current_player() == BLACK:
            turn_display = f"{BLACK}'s move"
        else:
            turn_display = f"{WHITE}'s move"
        move_display = f'{self.move} -> {turn_display} {self.simulations}\n'
        s = '  ' * depth + move_display
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s


def export_tree(tree: MCTSTree, path: str) -> None:
    """Export the given tree to an external writable file

    :param tree: the tree to be saved
    :param path: the path to the export file
    """
    with open(path, 'wb') as f:
        pickle.dump(tree, f)


def load_tree(path: str) -> MCTSTree:
    """Load the given byte encoded file to a MCTSTree object

    :param path: the path to the loaded file
    """
    with open(path, 'rb') as f:
        tree = pickle.load(f)
    return tree


class MCTSRoundPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS"""
    # Private Instance Attributes:
    #     - _round: The number of round of MCTS performed on each move
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    _n: int
    _tree: Optional[MCTSTree]
    _c: Union[float, int]

    def __init__(self, n: Union[int, float], tree: Optional[MCTSTree] = None,
                 c: Union[float, int] = math.sqrt(2)) -> None:
        """Initialize this player with the time limit per move and exploration parameter

        :param n: round of MCTS run per move
        :param tree: the MCTSTree used for making decisions
        :param c: exploration parameter
        """
        self._n = n
        self._tree = tree
        self._c = c

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state
            - len(game.get_valid_moves) > 0

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        if self._tree is None:  # initialize a tree if there is no tree
            if previous_move is None:
                self._tree = MCTSTree(START_MOVE, game)
            else:
                self._tree = MCTSTree(previous_move, game)
        else:  # update tree with previous move if there is a tree
            if len(self._tree.get_subtrees()) == 0:
                self._tree.expand()
            self._tree = self._tree.find_subtree_by_move(previous_move)

        # assert self._tree.get_game_after_move().get_game_board() == game.get_game_board()
        # assert self._tree.get_game_after_move().get_current_player() == game.get_current_player()

        for _ in range(self._n):
            self._tree.mcts_round(self._c)

        # update tree with the decided move
        move = self._tree.get_most_confident_move()
        self._tree = self._tree.find_subtree_by_move(move)
        return move


class MCTSTimerPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS with limited time"""
    # Private Instance Attributes:
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    #     - _time_limit: The time limit for each move
    _tree: Optional[MCTSTree]
    _c: Union[float, int]
    _time_limit: Union[int, float]

    def __init__(self, time_limit: Union[int, float], tree: Optional[MCTSTree] = None,
                 c: Union[float, int] = math.sqrt(2)) -> None:
        """Initialize this player with the time limit per move and exploration parameter

        :param time_limit: time limit per move in seconds
        :param tree: the MCTSTree used for making decisions
        :param c: exploration parameter
        """
        self._time_limit = time_limit
        self._tree = tree
        self._c = c

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state
            - len(game.get_valid_moves) > 0

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        if self._tree is None:  # initialize a tree if there is no tree
            if previous_move is None:
                self._tree = MCTSTree(START_MOVE, game)
            else:
                self._tree = MCTSTree(previous_move, game)
        else:  # update tree with previous move if there is a tree
            if len(self._tree.get_subtrees()) == 0:
                self._tree.expand()
            self._tree = self._tree.find_subtree_by_move(previous_move)

        # assert self._tree.get_game_after_move().get_game_board() == game.get_game_board()
        # assert self._tree.get_game_after_move().get_current_player() == game.get_current_player()

        time_start = time.time()
        while time.time() - time_start < self._time_limit:
            self._tree.mcts_round(self._c)

        # update tree with the decided move
        move = self._tree.get_most_confident_move()
        self._tree = self._tree.find_subtree_by_move(move)
        return move


class MCTSTimeSavingPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS. The decision time is based
    on the number of valid moves. The calculation for decision time is
    t = min(t_0^(num_valid_moves) - b, time_limit) where t_0, b is a given constant

    Instance Attributes:
        - time_limit: the time limit for each move
        - time_decision_constant: the time decision constant for each move
    """
    time_limit: Union[int, float]
    time_decision_base: Union[int, float]
    time_decision_intercept: Union[int, float]

    # Private Instance Attributes:
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    #     - _time_limit: The time limit for each move
    _tree: Optional[MCTSTree]
    _c: Union[float, int]

    def __init__(self, time_limit: Union[int, float],
                 time_decision_base: Union[int, float] = 1.3,
                 time_decision_intercept: Union[int, float] = 0,
                 tree: Optional[MCTSTree] = None, c: Union[float, int] = math.sqrt(2)) -> None:
        """Initialize this player with the time limit per move and exploration parameter

        Preconditions:
            - time_decision_base > 1.0
            - time_decision_intercept < time_decision_base

        :param time_limit: time limit per move in seconds
        :param tree: the MCTSTree used for making decisions
        :param c: exploration parameter
        """
        if time_decision_base <= 1 or time_decision_intercept >= time_decision_base:
            raise ValueError

        self.time_limit = time_limit
        self.time_decision_base = time_decision_base
        self.time_decision_intercept = time_decision_intercept
        self._tree = tree
        self._c = c

    def make_move(self, game: ReversiGame, previous_move: Optional[str]) -> str:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game state
            - len(game.get_valid_moves) > 0

        :param game: the current game state
        :param previous_move: the opponent player's most recent move, or None if no moves
        have been made
        :return: a move to be made
        """
        if self._tree is None:  # initialize a tree if there is no tree
            if previous_move is None:
                self._tree = MCTSTree(START_MOVE, game)
            else:
                self._tree = MCTSTree(previous_move, game)
        else:  # update tree with previous move if there is a tree
            if len(self._tree.get_subtrees()) == 0:
                self._tree.expand()
            self._tree = self._tree.find_subtree_by_move(previous_move)

        # assert self._tree.get_game_after_move().get_game_board() == game.get_game_board()
        # assert self._tree.get_game_after_move().get_current_player() == game.get_current_player()
        decision_time = self.decision_time(game, self.time_decision_base,
                                           self.time_decision_intercept)
        time_start = time.time()
        while time.time() - time_start < decision_time:
            self._tree.mcts_round(self._c)

        # update tree with the decided move
        move = self._tree.get_most_confident_move()
        self._tree = self._tree.find_subtree_by_move(move)
        return move

    def decision_time(self, game: ReversiGame, t0: Union[int, float],
                      b: Union[int, float]) -> float:
        """Return the decision time based on the given game state. The given time constant
        should be greater than 1. Raise ValueError if time_constant <= 1
        """
        assert len(game.get_valid_moves()) >= 1

        if t0 > 1 and t0 > b:
            return min(t0 ** len(game.get_valid_moves()), self.time_limit)
        raise ValueError
