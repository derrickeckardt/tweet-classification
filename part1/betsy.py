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
# getColumns(board,n,n) gets winable part of columns
# getColumns(board,n+3,n) gets entire column
def getColumns(board,m,n):
    return [("".join([b for b in board[i:n*m:n]])) for i in range(n)]

# Utility function to get rows
# getRows(board,n) gets rows from winnable rows only
# getRows(board,n+3) gets rows from all rows
def getRows(board,m,n):
    return [("".join([b for b in board[i:i+n]])) for i in range(0,n*m,n)]

# Utility function to get diagonals
# getDiagonals(board,n) gets diagonals for winnable section only.
def getDiagonals(board,n):
    return ["".join(board[0:n*n:n+1]),"".join(board[n-1:n*n-1:n-1])]

# See if board has a winning move for current player in rows, columns, and diagonals.
def winner(board):
    return True if current * n in getRows(board,n,n) + getColumns(board,n,n) + getDiagonals(board,n) else False    

# Implement heuristic function to determine strength of current player's move
def score(board):
    return 1

# Define possible next moves, successor function
def moves(board):
    new_boards = []
    
    # Rotate a column
    for each in getColumns(board,n+3,n):
        print each.count(".")*"." + each[each.count("."):n+3][-1] + each[each.count("."):n+3][0:-1]

    
    # Drop a pebble
    i = 0
    for each in getColumns(board,n+3,n):
        print each
        if "." in each:
            right_most = each.rindex(".")
            print each[0:right_most]+current+each[right_most+1:n+3]
            print right_most
            print board

# wrong        print board[0:i*n+right_most]+current+ board[i*nright_most+1:len(board)]
        i += 1    
    
    new_boards.append([])        
    
    return new_boards
    
    
winner(board)
print moves(board)
