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
n, current, board, time = [int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4])]

# Utility function to get columns
# getColumns(board,n,n) gets winable part of columns
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
# Implement heuristic function to determine strength of current player's move
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
    # Originally had this on one line, but it was just ugly to follow.  COuld combine them if I wanted to.
    # check to make sure player does not go over alloted number of game pieces.  If over, can't drop pieces.
    if board.count(turn) < (n*(n+3)/2):
        drop_boards = filter(None,[(board[0:n*each.rindex(".") + i] + current + board[n*each.rindex(".") + i + 1:len(board)]) if "." in each else None for each, i in zip(getColumns(board, n+3, n), range(0, n))])
        [new_boards.append([move, score(move)]) for move in drop_boards]

    return new_boards

# todo
def minimax(board):
    return "Make this move"

# todo
def alphabetapruning(board):
    return None

# todo
def selectBestMove(board):
    return moves(board,current)[0][0] # Change this once I actually get it running


winner(board)
# print "current board"
# print pretty_print(board)
# print "\nsuccessor boards"
# for successor, score in moves(board,current):
#     print pretty_print(successor)

# Let's Play!
# Will keep digging until it has exhausted space, found a winning next move..
n = 1
while n > 0:
    print minimax(board)