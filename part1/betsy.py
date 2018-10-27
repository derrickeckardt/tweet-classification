#!/usr/bin/env python
#
# CS B551 - Elements of AI
# Indiana University, Fall 2018
# Assignment 2, Part 1 - Betsy
#
# Completed by Derrick Eckardt
# derrick@iu.edu
#
###############################################################################
###############################################################################
#
# A full discussion and details can be found in the Readme file for Part 1, 
# which is located at:
# https://github.iu.edu/cs-b551-fa2018/derrick-a2/tree/master/part1
#
###############################################################################
###############################################################################


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


# Heuristic Function
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
            interim_2.extend([2*n*n])
        elif each.count(current) >= n-2:
            interim_2.extend([n*n])
        if each.count(not_current) >= n-1:
            interim_2.extend([-2*n*n])
        elif each.count(not_current) >= n-2:
            interim_2.extend([-n*n])

    # Might need to modify it further in the future
    for each in getColumns(board,n+3,n):
        if current*n in (each+each).replace(".",""):
            interim_2.extend([2*n*n])
        elif current*(n-1) in (each+each).replace(".","") and (each+each).count(".") > 0:
            interim_2.extend([n*n])
        if not_current*n in each+each.replace(".",""):
            interim_2.extend([-2*n*n])
        elif not_current*(n-1) in (each+each).replace(".","") and (each+each).count(".") > 0:
            interim_2.extend([-n*n])

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
            new_boards.extend([[rotated_board,-(i+1)]])  #append

    # Drop a pebble and add new boards
    # check to make sure player does not go over alloted number of game pieces.  If over, can't drop pieces.
    if board.count(turn) < (n*(n+3)/2):
        # Originally had this on one line, but it was just ugly to follow.  COuld combine them if I wanted to.
        drop_boards = filter(None,[[(board[0:n*each.rindex(".") + i] + turn + board[n*each.rindex(".") + i + 1:len(board)]),i+1] if "." in each else None for each, i in zip(getColumns(board, n+3, n), range(0, n))])
        [new_boards.extend([move]) for move in drop_boards] #append

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



# profile.run("alphabeta(board,8)")

# Let's Play!
for max_m in range(0,100,1):
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
    
