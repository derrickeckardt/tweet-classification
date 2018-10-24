#!/usr/bin/env python
#
# CS B551 - Elements of AI
# Indiana University, Fall 2018
# Assignment 2, Part 1 - Betsy
#
# Completed by Derrick Eckardt
# derrick@iu.edu

# Import libraries
import sys
import profile # For speed optimization.

# Get command line input
n, current, board, time = [int(sys.argv[1]), str(sys.argv[2]).lower(), str(sys.argv[3]), int(sys.argv[4])]
not_current = "o" if current=="x" else "x"

# Utility function to get columns
# getColumns(board,n,n) gets winable part of columns+
# getColumns(board,n+3,n) gets entire column
def getColumns(board, m, n):
    return [("".join([b for b in board[i:n*m:n]])) for i in range(n)]

# Utility function to get rows
# getRows(board,n) gets rows from winnable rows only
# getRows(board,n+3) gets rows from all rows
def getRows(board, m, n):
    return [("".join([b for b in board[i:i+n]])) for i in range(0, n*m, n)]

# Utility function to get diagonals
# getDiagonals(board,n) gets diagonals for winnable section only.
def getDiagonals(board, n):
    return ["".join(board[0:n*n:n+1]), "".join(board[n-1:n*n-1:n-1])]

# See if board has a winning move for current player in rows, columns, and diagonals.
def winner(board, turn):
    return True if turn * n in getRows(board, n, n) + getColumns(board, n, n) + getDiagonals(board, n) else False

# Todo
# A good heurisitc hear would value position and potential moves.  it would also be good at
# anticipating when someone else will win, and value it low enough it can get pruned
# early to save computing resources.
# Implement heuristic function to determine strength of current player's move,
# to be used when terminal states cannot be found
# This heurisitc is based on connect four and tic-tac-toe strategy
# In tic-tac-toe, the center box is the most value place, as we saw in lecture
# I used the following Connect 4 simulator, to build up some intuition, and it
# showed that the first column is the absolute best position for the first six moves
# of the game.  As you move away from the center, the moves become worse.
# http://connect4.gamesolver.org/?pos=34
# Since this game has similar dynamics, modeled it where it prioritizes placement
# of pieces towards the center, and then pieces above the cut-off line.
# so it has two parts. the center column is the most valuable (middle two if n is
# is even) and the edges are the least event, and it fans out from there.
#in terms of rows, the top row is the most valuable, given a value of n, and it loses value as it goes down to right above the cut-off line
# after the cut-off line, the three rows are always valued as 1,2,3
# to get the spot's score, they are multiplied by each other.
# this is a very simple scoring algorithm.  it only prefers moves that result with more pieces in the the higher value positions.  check out a heat map of the area.

# This article talks about the general strategy for connect four, about expert play
# https://www.quora.com/What-is-the-winning-strategy-for-the-first-player-in-Connect-Four-games
# and this goes into indepth connect4 strategy
# http://www.pomakis.com/c4/expert_play.html
# A heuristic algorithm would be much much more detailed and anticipate different
# scenarios better for valuing.


def score(board):
    
    def spotValue(colValue, rowValue):
        col = (n+1.0)/2.0-abs(colValue-(n+1.0)/2)
        row = n-rowValue if rowValue < n else rowValue-3
        return col*row
    # interim = [ [spot if spot == current else spot if spot == not_current else spot for spot in row] for row in getRows(board,n+3,n)]        
    interim_2 =[ sum([spotValue(colValue,rowValue) if spot == current else -spotValue(colValue,rowValue) if spot == not_current else 0 for spot, colValue in zip(row, range(1,n+1))]) for row, rowValue in zip(getRows(board,n+3,n), range(1,n+4))]
    
    # favors boards that have 4 in a row or a diagonal, if disfavors if opponent has them.
    for each in getRows(board,n,n)+getDiagonals(board,n):
        if each.count(current) >= n-1:
            interim_2 += 2 * n * n
        if each.count(not_current) >= n-1:
            interim_2 += -2 * n * n

    # print interim
    # print interim_2
    return sum(interim_2)


# Superfulous function to make board visually print nice
def pretty_print(board):
    return "".join([board[i*n:i*n+n] + "\n" for i in range(n+3)])

# Define possible next moves, successor function
def moves(board,turn):
    new_boards = []
    
    # Rotate a column
    for each, i in zip(getColumns(board, n+3, n),range(n)):
        if "."*(n+3) in each:
            None # nothing to rotate
        else:
            rotated_column = ["."]*each.count(".") + list(filter(lambda k:"." not in k,list(each)).pop()) + filter(lambda k:"." not in k,list(each))[0:-1]
            rotated_board = "".join([rotated_column.pop(0) if j in [i+m*n for m in range(n+3)] else list(board)[j] for j in range(n*(n+3))])
            new_boards.append([rotated_board,-(i+1)])

    # Drop a pebble and add new boards
    # check to make sure player does not go over alloted number of game pieces.  If over, can't drop pieces.
    if board.count(turn) < (n*(n+3)/2):
        # Originally had this on one line, but it was just ugly to follow.  COuld combine them if I wanted to.
        drop_boards = filter(None,[[(board[0:n*each.rindex(".") + i] + turn + board[n*each.rindex(".") + i + 1:len(board)]),i+1] if "." in each else None for each, i in zip(getColumns(board, n+3, n), range(0, n))])
        [new_boards.append(move) for move in drop_boards]

    return new_boards


# Alpha-beta pruning, adopted from pseudocode in Russell & Norvig textbook, page 172
# Added ability to end after moves m, since because of a time limit, we know the
# code will not be able to run everything to the leaves, especially if the board
# is exceeding large 
def alphabeta(board, max_m):

    def maxValue(board, alpha, beta, current_m):
        if winner(board, not_current):
            return -float("inf"), board
        if winner(board, current):
            return float('inf'), board
        if current_m > max_m:
            return score(board), board
        v = -float("inf")
        for each, move_descriptor in moves(board,current):
            v_min, v_min_board = minValue(each, alpha,beta,current_m+1) 
            v = max(v,v_min)
            if v >= beta:
                return v, v_min_board
            alpha = max(alpha,v)
        "Finished maxValue loop"
        return v, v_min_board

    def minValue(board, alpha, beta, current_m):
        if winner(board, current):
            return float('inf'), board
        if winner(board, not_current):
            return -float('inf'),board
        if current_m > max_m:
            return score(board), board
        v = float("inf")
        for each, move_descriptor in moves(board,not_current):
            v_max, v_max_board = maxValue(each, alpha,beta,current_m+1) 
            v = min(v,v_max)
            if v <= alpha:
                return v, v_max_board
            beta = min(beta,v)
    #    print "finished MinValue loop"
        return v, v_max_board

    alpha, beta, best_move, best_move_descriptor = -float('inf'), float('inf'), None, 0
    for my_move, my_move_desciptor in moves(board,current):
        v, min_board = minValue(my_move,alpha,beta,1)
        # (best_move, best_move_descriptor, alpha) = (my_move, my_move_desciptor, v) if v > alpha else best_move, best_move_descriptor, alpha
        if v > alpha:
            best_move = my_move
            best_move_descriptor = my_move_desciptor
            alpha = v
            # print "current best move: \n", pretty_print(best_move)
            # print "current best score: ", best_score
    return alpha, (best_move if best_move != None else my_move ), best_move_descriptor if best_move_descriptor !=0 else my_move_desciptor

# Let's Play!
# print "Starting board"
# print pretty_print(board)

# profile.run("alphabeta(board,8)")

for max_m in range(0,10,2):
    lets_play = alphabeta(board,max_m)
    # print max_m
    # print "score ", lets_play[0]
    # print "descriptor", lets_play[2]
    # print pretty_print(lets_play[1])
    if lets_play[0] == -float('inf'):
        print "I cannot win. You will only need to take "+str(int(max_m/2)+1)+" moves or fewer to beat me.  That makes me sad.  This game doesn't even let me resign.  Here is a move, please make it a swift execution."
        print str(lets_play[2])+ " "+lets_play[1]
        break
    if lets_play[0] == float('inf'):
        print "I only need to take "+str(int(max_m/2)+1)+" moves or fewer to vanguish you!"
        print str(lets_play[2])+ " "+lets_play[1]
        break
    print str(lets_play[2])+ " "+lets_play[1]