## Part 1: Betsy 

Completed by Derrick Eckardt on October 26, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Getting Started

As directed in the assignment, to run this program type the following at the command line:

    ./betsy.py [n] [current] [board] [time]
    
Where n is the dimension indicating the board size, current is whose turn it is (x or o), board is the current game board in a text string, and time is the move time limit in seconds

For example, the first move of a game by player x would be:

    ./betsy.py 3 x .................. 10

Or a move later in the game might look like:

    ./betsy.py 3 x ........xooooooxxx 10

For a more details on the required set-up and game set-up, please see the [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf)

## Summary of Problem

In general, think of this as a search problem.

### Initial State

The program is designed to suggest exactly one move, that can be anywhere in the game.  Our earliest initial state could be a board with no pieces, or it could be a board where every spot is full and players are rotating columns as the only available moves (see successor function for more info on rotating columns.)

### Goal State

The goal state is one move later, that has hopefully improved the player's turn.  Ideally, it is to determine the move that leads to the a winning position.  However, since the state space cannot be fully searched, if a winning state cannot be found, then we want to get to the strongest position possible.

### Successor Function

There are two kinds of valid moves in the game.  Players may add a pebble to a column that is not full, or it may rotate the pebbles in column that has at least one pebble.  These become the basis for the successor function, which will look for possible moves.  For a board n equal to three, the successor function will generate three to six moves, depending on the state of the game.  For n equal to five, it will generate five to ten.  

### State Space

The state space is the game board.  Based on the successor function mentioned above Betsy has a very high branching factor, so the overall state space is tremendously large.  That works out to 3<sup>18</sup> or 387,420,489 combinations for an n = 3 board.  For n = 5, that is 1.21 x 10<sup>19</sup> combinations.  Not easily searchable by any algorithm.

### Search Algorithm

For this program, I implemented the MinMax algorithm with Alphabeta pruning.  This algorithm goes iteratively deeper, with each level taking approximately n to 2n times longer than the previous level to evaluate.  Because this is meant to be time limited, I cannot expect the algorithm to find the winning states, particularly for early game states.  In order to do that, I implemented a heuristic function that assesses the strength of board.   The algorithm goes by assuming that my opponent always makes the best possible for them and worst for me.   The alpha beta pruning allows me to eliminate paths that are clearly inferior to other states, reducing the branching factor, and allowing for the evaluation of deeper levels.

### Heurestic Function

Since the program cannot practically get to all of the leaves given the state space, I use heuristic function to evaluate the strength of a board.  The heuristic function in this case might be best referred to as my game play strategy.  How do I determine which boards are the best.  



A good heurisitc hear would value position and potential moves.  it would also be good at
anticipating when someone else will win, and value it low enough it can get pruned
early to save computing resources.
Implement heuristic function to determine strength of current player's move,
to be used when terminal states cannot be found
This heurisitc is based on connect four and tic-tac-toe strategy
In tic-tac-toe, the center box is the most value place, as we saw in lecture
I used the following Connect 4 simulator, to build up some intuition, and it
showed that the first column is the absolute best position for the first six moves
of the game.  As you move away from the center, the moves become worse.
http://connect4.gamesolver.org/?pos=34
Since this game has similar dynamics, modeled it where it prioritizes placement
of pieces towards the center, and then pieces above the cut-off line.
so it has two parts. the center column is the most valuable (middle two if n is
is even) and the edges are the least event, and it fans out from there.
in terms of rows, the top row is the most valuable, given a value of n, and it loses value as it goes down to right above the cut-off line
after the cut-off line, the three rows are always valued as 1,2,3
to get the spot's score, they are multiplied by each other.
this is a very simple scoring algorithm.  it only prefers moves that result with more pieces in the the higher value positions.  check out a heat map of the area.

This article talks about the general strategy for connect four, about expert play
https://www.quora.com/What-is-the-winning-strategy-for-the-first-player-in-Connect-Four-games
and this goes into indepth connect4 strategy
http://www.pomakis.com/c4/expert_play.html
A heuristic algorithm would be much much more detailed and anticipate different
scenarios better for valuing.





**Cost Function:** TBD

## Discussion of Approach

TBD

## Opportunities for Improvement

TBD

