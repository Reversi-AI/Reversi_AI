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
from typing import Optional, Union, Callable
import copy
import random
import math
import pickle
import time

from constants import BLACK, WHITE, START_MOVE, BOARD_POSITION_8, BOARD_POSITION_6
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
        and the highest win rate

        Return the leftmost one if tie
        """
        best_subtree = max(self._subtrees,
                           key=lambda subtree: subtree.get_total_simulation_number())
        return best_subtree.move

    def get_total_simulation_number(self) -> int:
        """Return the number of simulation run on this node"""
        return sum(self.simulations.values())

    def mcts_round(self, c: Union[int, float], rollout_policy: Optional[Callable] = None) -> None:
        """Perform one round of MCTS with the given exploration parameter

        :param c: the exploration parameter
        :param rollout_policy: the function for the rollout process
        """
        if rollout_policy is None:
            rollout_policy = MCTSTree.rollout_random

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
            rollout_winner = rollout_policy(selected_leaf)
            self.update(rollout_winner, path)
        else:  # update the path directly and multiple times when the node is terminal
            for _ in range(3):
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
                    if subtree._uct(side, c, n_total) >= max_ucb_value_so_far:
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
        if side == BLACK:
            opposite = WHITE
        else:
            opposite = BLACK

        if self._game_after_move.get_current_player() != side:  # player's move
            w = self.simulations[side]
        else:  # opponent's move
            w = self.simulations[opposite]

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

    def rollout_random(self) -> str:
        """Rollout process of the MCTS. Moves are randomly chosen.
        Return the winner of the rollout"""
        game_copy = copy.deepcopy(self._game_after_move)

        # rollout
        while game_copy.get_winner() is None:
            selected_move = random.choice(game_copy.get_valid_moves())
            game_copy.make_move(selected_move)
        return game_copy.get_winner()

    def rollout_position(self) -> str:
        """Rollout process of the MCTS. Moves are chosen based on positional strategy.
        Return the winner of the rollout"""
        game_copy = copy.deepcopy(self._game_after_move)

        # rollout
        while game_copy.get_winner() is None:
            moves = game_copy.get_valid_moves()

            # weight: corner > edges > center > buffers
            if game_copy.get_size() == 8:
                positions = BOARD_POSITION_8
            else:
                positions = BOARD_POSITION_6

            weights_so_far = []
            for move in moves:
                if move in positions['corners']:
                    weights_so_far.append(3)
                else:
                    weights_so_far.append(1)

            selected_move = random.choices(moves, weights_so_far)[0]
            game_copy.make_move(selected_move)
        return game_copy.get_winner()

    def rollout_mobility(self) -> str:
        """Rollout process of the MCTS. Moves are chosen based on mobility strategy.
        Return the winner of the rollout"""
        game_copy = copy.deepcopy(self._game_after_move)

        # rollout
        while game_copy.get_winner() is None:
            moves = game_copy.get_valid_moves()
            # the game state after the move should have the less move
            # which means fewer moves are opponent
            weights = []
            for move in moves:
                if len(game_copy.simulate_move(move).get_valid_moves()) < len(moves):
                    weights.append(2)
                else:
                    weights.append(1)
            selected_move = random.choices(moves, weights)[0]
            game_copy.make_move(selected_move)
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


class MCTSRoundPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS"""
    # Private Instance Attributes:
    #     - _round: The number of round of MCTS performed on each move
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    #     - _rollout_policy: The rollout function for the MCTS algorithm
    _n: int
    _c: Union[float, int]
    _rollout_policy: Callable

    def __init__(self, n: Union[int, float],
                 c: Union[float, int] = math.sqrt(2), rollout: Optional[Callable] = None) -> None:
        """Initialize this player with the time limit per move and exploration parameter

        :param n: round of MCTS run per move
        :param c: exploration parameter
        :param rollout: the rollout function for the tree search
        """
        self._n = n
        self._c = c
        if rollout is None:
            rollout = MCTSTree.rollout_random
        self._rollout_policy = rollout

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
        if previous_move is None:
            current_tree = MCTSTree(START_MOVE, copy.deepcopy(game))
        else:
            current_tree = MCTSTree(previous_move, copy.deepcopy(game))

        assert current_tree.get_game_after_move().get_game_board() == game.get_game_board()
        assert current_tree.get_game_after_move().get_current_player() == game.get_current_player()

        for _ in range(self._n):
            current_tree.mcts_round(self._c, self._rollout_policy)

        # update tree with the decided move
        move = current_tree.get_most_confident_move()
        return move


class MCTSTimerPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS with limited time"""
    # Private Instance Attributes:
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    #     - _time_limit: The time limit for each move
    #     - _rollout_policy: The rollout function for the MCTS algorithm
    _tree: Optional[MCTSTree]
    _c: Union[float, int]
    _time_limit: Union[int, float]
    _rollout_policy: Callable

    def __init__(self, time_limit: Union[int, float], tree: Optional[MCTSTree] = None,
                 c: Union[float, int] = math.sqrt(2), rollout: Optional[Callable] = None) -> None:
        """Initialize this player with the time limit per move and exploration parameter

        :param time_limit: time limit per move in seconds
        :param tree: the MCTSTree used for making decisions
        :param c: exploration parameter
        """
        self._time_limit = time_limit
        self._tree = tree
        self._c = c
        if rollout is None:
            rollout = MCTSTree.rollout_random
        self._rollout_policy = rollout

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
        if previous_move is None:
            current_tree = MCTSTree(START_MOVE, copy.deepcopy(game))
        else:
            current_tree = MCTSTree(previous_move, copy.deepcopy(game))

        assert current_tree.get_game_after_move().get_game_board() == game.get_game_board()
        assert current_tree.get_game_after_move().get_current_player() == game.get_current_player()

        time_start = time.time()
        while time.time() - time_start < self._time_limit:
            current_tree.mcts_round(self._c)

        # update tree with the decided move
        move = current_tree.get_most_confident_move()
        return move


class MCTSTimeSavingPlayer(Player):
    """A Reversi AI player who makes decisions with MCTS. Before making a decision, the player
    would repeatedly run MCTS on its tree. Once the number of round reaches a certain number
    or the time reaches the time limit of the move, the player would stop running MCTS and
    make a decision.

    The number of rounds of MCTS run per move is a exponential function of the number of
    valid moves, which is calculated by a0^n where a0 is a given constant and n is the number
    of valid moves of the current game state.

    Instance Attributes:
        - n: the number of MCTS runs per turn
        - time_limit: the time limit for each move
    """
    n: int
    time_limit: Union[int, float]

    # Private Instance Attributes:
    #     - _tree: The decision tree for this player to make its moves
    #     - _c: The exploration parameter for the MCTS algorithm
    #     - _time_limit: The time limit for each move
    #     - _rollout_policy: The rollout function for the MCTS algorithm
    _tree: Optional[MCTSTree]
    _c: Union[float, int]
    _rollout_policy: Callable

    def __init__(self, n: Union[int, float], time_limit: Union[int, float],
                 tree: Optional[MCTSTree] = None, c: Union[float, int] = math.sqrt(2),
                 rollout: Optional[Callable] = None) -> None:
        """Initialize this player with the time limit per move and other parameters

        :param n: the number of MCTS runs per turn
        :param time_limit: time limit per move in seconds
        :param tree: the MCTSTree used for making decisions
        :param c: exploration parameter
        """
        self.n = n
        self.time_limit = time_limit
        self._tree = tree
        self._c = c
        if rollout is None:
            rollout = MCTSTree.rollout_random
        self._rollout_policy = rollout

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
        if previous_move is None:
            current_tree = MCTSTree(START_MOVE, copy.deepcopy(game))
        else:
            current_tree = MCTSTree(previous_move, copy.deepcopy(game))

        assert current_tree.get_game_after_move().get_game_board() == game.get_game_board()
        assert current_tree.get_game_after_move().get_current_player() == game.get_current_player()

        # return move if there is only one move
        if len(game.get_valid_moves()) == 1:
            return game.get_valid_moves()[0]

        runs_so_far = 0  # the counter for the rounds of MCTS run
        time_start = time.time()

        # at least run 1 second, ends when exceeds time limit or finishes n runs
        while not (time.time() - time_start > max(self.time_limit, 1) or runs_so_far == self.n):
            current_tree.mcts_round(self._c, self._rollout_policy)
            runs_so_far += 1

        # update tree with the decided move
        move = current_tree.get_most_confident_move()
        return move


################################################################################
# The following functions are for exporting the decision trees for MCTS players
################################################################################

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


# if __name__ == '__main__':
#     for _ in range(10):
#         mcts_train(n_games=10, game_size=8, mcts_rounds=500, verbose=True)
