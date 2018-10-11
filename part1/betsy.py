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

# Implement heuristic function to determine strength of current player's move
def score(board):
    
    return 1

# See if board has a winning move
def winner(board):
    # Check row
    
    
    # Check column, if True, a column has a winning move for the current player
    columnn = max([True if current*n in ("".join([b for b in board[i:n*n:n]])) else False for i in range(n)])
    print columnn

    
    
    # Check diagonals
    
    return False
    

# Define possible next moves, successor function
def moves(board):
    new_boards = []
    # Drop a pebble
        # Check if column is full
    
    # Rotate a column
    
    new_boards.append([])        
    
    return new_boards
    
    
winner(board)