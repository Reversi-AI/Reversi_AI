# Reversi AI
In this project, we will implement AI players in the board game Reversi (also called Othello) with
the utilization of Tree data structure. 

Due to the 8x8 size of the grid, there are many potential moves that can be made each turn, which
provides some unique challenges when implementing decision-making algorithms. We want to compare the
performance of different decision-making algorithms. 

We will focus on two algorithms in the project:
- Minimax: This is an algorithm widely used in two player turn-based game. We would
  implement various versions of the AI player with this algorithm based on different strategies 
  presented by different value evaluation functions
  - The greedy strategy: Aiming for the maximum number of pieces of its side after a certain
    depth of the game tree
  - The positional strategy: Aiming for occupying certain position on the board to gain positional 
    advantage. For instance, corner pieces are immune to being flipped.
  - Mobility strategy: Aiming for as many possible moves as possible
    
- Monte Carlo Tree Search (MCTS): An heuristic search algorithm for decision making used in complex
  engines like AlphaGo

## Getting started

These instructions will get you a copy of the project up and running on your local machine for
development and testing purposes.

The project is built on python 3.9. Please install python 3.9 with tkinter installation

Please install all python libraries in requirement.txt.
  
## Authors
- Haoze Deng
- Peifeng Zhang
- Man Chon Ho
- Alexander Nicholas Conway
