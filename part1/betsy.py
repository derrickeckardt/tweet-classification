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
n, current, board, time = [int(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]),int(sys.argv[4])]

# Utility function to get columns
# getColumns(board,n,n) # gets winable part of columns
# getColumns(board,n+3,n) # gets entire column
def getColumns(board,m,n):
    return [("".join([b for b in board[i:n*m:n]])) for i in range(n)]

# Utility function to get rows
# getRows(board,n) # Gets rows from winnable rows only
# getRows(board,n+3) # gets rows from all rows
def getRows(board,m,n):
    return [("".join([b for b in board[i:i+n]])) for i in range(0,n*m,n)]


# Implement heuristic function to determine strength of current player's move
def score(board):
    
    return 1

# See if board has a winning move
def winner(board):
    # Check row
    row_win = True if current*n in getRows(board,n,n) else False

    # Check column, if True, a column has a winning move for the current player
    column_win = True if current*n in getColumns(board,n,n) else False

    # Check diagonals
    
    # Just for readability, put this here,  Otherwise, would have combined all three of the above into one return line.
    return max([row_win,column_win])
    

# Define possible next moves, successor function
def moves(board):
    new_boards = []
    # Drop a pebble
        # Check if column is full
    
    # Rotate a column
    column_boards = getColumns(board,n+3,n)
    
    new_boards.append([])        
    
    return new_boards
    
    
print winner(board)
print moves(board)
print "12345672".rindex("4")
print "12345672".rindex("2")
