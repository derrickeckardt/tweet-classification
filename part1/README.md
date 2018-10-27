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

## Summary of Problem and Discussion of Approach

In general, think of this as a search problem.  I'm searching for the best moves that get me to a win the fastest, assuming my opponent plays perfectly.  What will make the most difference is my strategy (my heurisitc).

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

Since the program cannot practically get to all of the leaves given the state space, I use heuristic function to evaluate the strength of a board.  The heuristic function in this case might be best referred to as my game play strategy.  So how do I determine which boards are the best?  I'm not sure, but here is my best guess of what and how I got there.

First, I thought a good heurisitc would value position and the potential for biggers moves.  Also, it would also be to recognize threats from the opponenent.  A strong position for me would be a large positive number, and a bad board for me would be a large negative value.  (values according to some scale I would later set)

Next, I looked at similar games.  We learned in class that tic-tac-toe strategy favors starting in the center square.  Another similar game is Connect Four.  I used this [Connect 4 Solver](http://connect4.gamesolver.org/?pos=34) in order to build up some intuition.  That showed that the center column is the absolute best position for the first six moves of the game since it is involved in the most possible winning outcomes.  Betsy is similarily structured.

So, since Betsy has similar dynamics, the first part of my heurisitc assigned weights to each square on the board.  If it was one my pieces, I added it.  If it was one of my opponents pieces I substracted it.  

I modeled it where it prioritizes placement of pieces towards the center, and then pieces above the cut-off line where you can actually win.  Each spot on the board's score has two compoents a column value (colValue) and a row value (rowValue).  The center column is the most valuable (middle two columns if n is is even) and the edges are the least valuable and it slopes down in between. In terms of rows, the top row is the most valuable, given a value of n, and it loses a value of 1 from each row as it down to right above the cut-off line above the cut-off line.  The three rows bottom are always valued as 1,2, and3.   to get the spot's score, they are multiplied by each other. This is a very simple scoring algorithm.  it only prefers moves that result with more pieces in the the higher value positions.  check out a map of values for a board of n equal to 3.

![alt text](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/part1/n3boardvalues.jpg "n=3 board values")

Now, the algorithm needed to account for strength of future moves.  In other moves, boards that not only have high value points, but also have possible winning outcomes.  More [Connect 4 Strategy](https://www.quora.com/What-is-the-winning-strategy-for-the-first-player-in-Connect-Four-games) and [Expert Connect 4 Strategy](http://www.pomakis.com/c4/expert_play.html) went into great depth.  While not a one-to-one analogy, it drove home the importance of positions that lead to multiple different ways to win.

Since, the board can change fairly easily via rotations, the way I implemented that part of the heuristic was to recognize rows, diagonals, and/or columns that had the potential to win by having enough pieces in those lines.  Then, I added or subtracted values of either 2n<sup>2</sup> or just n<sup>2</sup> to my board score.  This would cause the number to move significantly based on the strength of the future wins.

I thought about hard-coding some things into it such as, if you see four in a row, immediately block it.  However, that may cause me to actually miss opportunities to win sooner, and that is actually a suboptimal move. This is where confidence in the heurisitc is necessary.

## Does it work?

Well, yes it does.  My Betsy bot has played several matches against other players.  It seems to make good moves.  She does not miss too many obvious good moves, and seems to know the right times to play defense.  With that said, I have watched as Betsy was only a couple of moves away from a win, and just did not make the necessary moves to win.  I'm probably not going to win the Western Pennsylvania Betsy world championship, though.

## Opportunities for Improvement

**More in-depth strategy** - This heurisitc function only scratches the surfaces as to what can be done.  It evaluates strength of position, and the possibility of future wins.  Since this game is relatively new to me, I'm sure more games would reveal some basic strategy, edge cases, or other ways to think about playing the game and completely rewrite the heurisitc.

**Refactor code** - This might be the best code I have written.  Some of the functions are single lines, which make me happy.  However, this game is all about speed.  I used the profile library to check the time of the program, and I found that my heurisitc function consumes a significant chunk of the time resources.  If I could figure out a way to more efficiently evaluate the board, I might be able to win more matches simply by the ability to look deeper into the board for future winning moves.  Since, thousands of boards are evaluated, some gains in just efficient code could result in an extra level of results.  That could be enough to ensure a win.

**Build a Better Betsy Bot** - Clearly, Betsy can be improved.  How good a player could she be?  Significantly better.  Yesterday (October 25), I came across an article on [how to build my own AlphaZero game playing bot for any game](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188).  This has me really intrigued, because, in reality, AlphaZero would know exactly what I know about Betsy at this point.  This could be a fun side project.  Or, perhaps we'll do this as part of a future assignment. :-)