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

**Initial State:** The program is designed to suggest exactly one move, that can be anywhere in the game.  Our earliest initial state could be a board with no pieces, or it could be a board where every spot is full and players are rotating columns as the only available moves (see successor function for more info on rotating columns.)

**Goal State:** The goal state is one move later, that has hopefully improved the player's turn.  Ideally, it is to determine the move that leads to the a winning position.  However, since the state space cannot be fully searched, if a winning state cannot be found, then we want to get to the strongest position possible.

**Successor Function:** There are two kinds of valid moves in the game.  Players may add a pebble to a column that is not full, or it may rotate the pebbles in column that has at least one pebble.  These become the basis for the successor function, which will look for possible moves.  For a board n equal to three, the successor function will generate three to six moves, depending on the state of the game.  For n equal to five, it will generate five to ten.  As you can see, this game has a very high branching factor, so the overall state space in tremendously large.  That works out to 3<sup>18</sup> or 387,420,489 combinations.


**State Space:** The state space is the game board.  


**Search Algorithm:** TBD

**Heurestic Function:** TBD

**Cost Function:** TBD

## Discussion of Approach

TBD

## Opportunities for Improvement

TBD

