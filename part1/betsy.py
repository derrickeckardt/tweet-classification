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
def winner(board, turn):
    return True if turn * n in getRows(board, n, n) + getColumns(board, n, n) + getDiagonals(board, n) else False

# Todo
# Implement heuristic function to determine strength of current player's move,
# to be used when terminal states cannot be found
# This heurisitc is based on connect four and tic-tac-toe strategy
# In tic-tac-toe, the center box is the most value place, as we saw in lecture
# I used the following Connect 4 simulator, to build up some intuition, and it
# showed that the first column is the absolute best position
# Since this game has similar dynamics, modeled it where it prioritizes placement
# of pieces towards the center, and then pieces above the cut-off line.
def score(board, turn):
    if winner(board, turn):
        return (float("inf") if turn == current else -float('inf'))
    else:
        interim = [ [spot if spot == current else spot if spot == not_current else spot for spot in row] for row in getRows(board,n+3,n)]        
        interim_2 =[ sum([colValue*rowValue if spot == current else -colValue*rowValue if spot == not_current else 0 for spot, colValue in zip(row, range(0,n))]) for row, rowValue in zip(getRows(board,n+3,n), range(n+3,0,-1))]
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
            new_boards.append(rotated_board)

    # Drop a pebble and add new boards
    # check to make sure player does not go over alloted number of game pieces.  If over, can't drop pieces.
    if board.count(turn) < (n*(n+3)/2):
        # Originally had this on one line, but it was just ugly to follow.  COuld combine them if I wanted to.
        drop_boards = filter(None,[(board[0:n*each.rindex(".") + i] + turn + board[n*each.rindex(".") + i + 1:len(board)]) if "." in each else None for each, i in zip(getColumns(board, n+3, n), range(0, n))])
        [new_boards.append(move) for move in drop_boards]

    return new_boards


# Alpha-beta pruning, adopted from pseudocode in Russell & Norvig textbook, page 172
# Added ability to end after moves m, since because of a time limit, we know the
# code will not be able to run everything to the leaves, especially if the board
# is exceeding large 
def alphabeta(board, max_m):

    def maxValue(board, alpha, beta, current_m):
        if current_m > max_m:
            return score(board, current), board
        for each in moves(board,current):
            v_min, v_min_board = minValue(each, alpha,beta,current_m+1) 
            v = max(-float('inf'),v_min)
            if v >= beta:
                return v, v_min_board
            alpha = max(alpha,v)
        "Finished maxValue loop"
        return v, v_min_board

    def minValue(board, alpha, beta, current_m):
        if current_m > max_m:
            return score(board, current), board
        # Initially thought i would need the board scored at htis point, but don't
        # think i do, so i may be able to scrap that in the future
        for each in moves(board,not_current):
            v_max, v_max_board = maxValue(each, alpha,beta,current_m+1) 
            v = min(float('inf'),v_max)
            if v <= alpha:
                return v, v_max_board
            beta = min(beta,v)
    #    print "finished MinValue loop"
        return v, v_max_board

    alpha, beta = -float('inf'), float('inf')

    for my_move in moves(board,current):
        v, min_board = minValue(my_move,alpha,beta,1)
        if v > alpha:
            best_move = my_move
            best_score = v
            print "current best move: \n", pretty_print(best_move)
            print "current best score: ", best_score
    return best_move, best_score




# print "current board"
# print pretty_print(board)
# print "\nsuccessor boards"
# for successor, score in moves(board,current):
#     print pretty_print(successor)

# Let's Play!
print "Starting board"
print pretty_print(board)
for max_m in range(1,4,2):
    lets_play = alphabeta(board,max_m)
    print pretty_print(lets_play[0])
    print "score ", lets_play[1]
    # if lets_play == float('inf'): break