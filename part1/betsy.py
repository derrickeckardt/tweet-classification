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
def winner(board):
    return True if current * n in getRows(board, n, n) + getColumns(board, n, n) + getDiagonals(board, n) else False

# Todo
# Implement heuristic function to determine strength of current player's move,
# to be used when terminal states cannot be found
# This heurisitc is based on connect four and tic-tac-toe strategy
# In tic-tac-toe, the center box is the most value place, as we saw in lecture
# I used the following Connect 4 simulator, to build up some intuition, and it
# showed that the first column is the absolute best position
# Since this game has similar dynamics, modeled it where it prioritizes placement
# of pieces towards the center, and then pieces above the cut-off line.
def score(board):
    return 1

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
            new_boards.append([rotated_board,score(rotated_board)])

    # Drop a pebble and add new boards
    # check to make sure player does not go over alloted number of game pieces.  If over, can't drop pieces.
    if board.count(turn) < (n*(n+3)/2):
        # Originally had this on one line, but it was just ugly to follow.  COuld combine them if I wanted to.
        drop_boards = filter(None,[(board[0:n*each.rindex(".") + i] + turn + board[n*each.rindex(".") + i + 1:len(board)]) if "." in each else None for each, i in zip(getColumns(board, n+3, n), range(0, n))])
        [new_boards.append([move, score(move)]) for move in drop_boards]

    return new_boards


# Alpha-beta pruning, adopted from pseudocode in Russell & Norvig textbook, page 172
# Added ability to end after moves m, since because of a time limit, we know the
# code will not be able to run everything to the leaves, especially if the board
# is exceeding large 
def alphabeta(board):
    return None


# todo
def maxValue(board, alpha, beta, current_m):
    if current_m > max_m:
        return score(board)
    # Initially thought i would need the board scored at htis point, but don't
    # think i do, so i may be able to scrap that in the future
    for each, scored_board in moves(board,current):
        v = max(-1*float('inf'),minValue(each, alpha,beta,current_m+1)
        if v >= beta:
            return v
        alpha = max(alpha,v)
    return v

def minValue(board, alpha, beta, current_m):
    if current_m > max_m:
        return score(board)
    # Initially thought i would need the board scored at htis point, but don't
    # think i do, so i may be able to scrap that in the future
    for each, scored_board in moves(board,not_current):
        v = min(float('inf'),minValue(each, alpha,beta,current_m+1)
        if v <= alpha:
            return v
        beta = min(alpha,v)
    return v



winner(board)
# print "current board"
# print pretty_print(board)
# print "\nsuccessor boards"
# for successor, score in moves(board,current):
#     print pretty_print(successor)

# Let's Play!
# Will keep digging until it has exhausted space, found a winning next move..

for max_m in range(0,1):
    print alphabeta(board)