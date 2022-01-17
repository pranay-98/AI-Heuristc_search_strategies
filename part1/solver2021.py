#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: "Pranay Reddy / pdasari, Vamsee Krishna Sai / vnarams, Anil Ravi/ anilravi "
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

from os import stat_result
import sys
import heapq
import numpy as np
from copy import deepcopy

ROWS=5
COLS=5

goal=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

# some of the below action functions (successor generation functions) are taken from test_a1p1.py file

def move_right(board, row):
    board1=deepcopy(board)
    board1[row] = board1[row][-1:] + board1[row][:-1]
    return board1

def move_left(board, row):
    board1=deepcopy(board)
    board1[row] = board1[row][1:] + board1[row][:1]
    return board1

def move_up(board,col):
    board1=deepcopy(board)
    board1=transpose_board(board1)
    board1=move_left(board1,col)
    return transpose_board(board1)

def move_down(board,col):
    board1=deepcopy(board)
    board1=transpose_board(board1)
    board1=move_right(board1,col)
    return transpose_board(board1)


def rotate_right(board,row,residual):
    board[row] = [board[row][0]] +[residual] + board[row][1:]
    residual=board[row].pop()
    return residual

def rotate_left(board,row,residual):
    board[row] = board[row][:-1] + [residual] + [board[row][-1]]
    residual=board[row].pop(0)
    return residual

def Ic_rotate_right(board,row,residual):
    board[row] = board[row][:2] + [residual] + board[row][2:]
    residual=board[row].pop(-2)
    return residual

def Ic_rotate_left(board,row,residual):
    board[row] = board[row][:3] + [residual] + board[row][3:]
    residual=board[row].pop(1)
    return residual

def Oc_clockwise(board):
    board1=deepcopy(board)
    board1[0]=[board1[1][0]]+board1[0]
    residual=board1[0].pop()
    board1=transpose_board(board1)
    residual=rotate_right(board1,-1,residual)
    board1=transpose_board(board1)
    residual=rotate_left(board1,-1,residual)
    board1=transpose_board(board1)
    residual=rotate_left(board1,0,residual)
    board1=transpose_board(board1)
    return board1

def Oc_cclockwise(board):
    board1=deepcopy(board)
    board1[0]=board1[0]+[board1[1][-1]]
    residual=board1[0].pop(0)
    board1=transpose_board(board1)
    residual=rotate_right(board1,0,residual)
    board1=transpose_board(board1)
    residual=rotate_right(board1,-1,residual)
    board1=transpose_board(board1)
    residual=rotate_left(board1,-1,residual)
    board1=transpose_board(board1)
    return board1

def Ic_clockwise(board):
    board1=deepcopy(board)
    board1[1]=[board1[1][0]]+[board1[2][1]]+board1[1][1:]
    residual=board1[1].pop(4)
    board1=transpose_board(board1)
    residual=Ic_rotate_right(board1,-2,residual)
    board1=transpose_board(board1)
    residual=Ic_rotate_left(board1,-2,residual)
    board1=transpose_board(board1)
    residual=Ic_rotate_left(board1,1,residual)
    board1=transpose_board(board1)
    return board1

def Ic_cclockwise(board):
    board1=deepcopy(board)
    board1[1]=board1[1][0:-1]+[board1[2][-2]]+[board1[1][-1]]
    residual=board1[1].pop(1)
    board1=transpose_board(board1)
    residual=Ic_rotate_right(board1,1,residual)
    board1=transpose_board(board1)
    residual=Ic_rotate_right(board1,-2,residual)
    board1=transpose_board(board1)
    residual=Ic_rotate_left(board1,-2,residual)
    board1=transpose_board(board1)
    return board1

def transpose_board(board):
    return [[row[i] for row in board] for i in range(len(board[0]))]

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

# misplaced_tiles heuristic
def h(current_state,goal):
    temp = 0
    for i in range(0,ROWS*COLS):
        if current_state[i] != goal[i]:
            temp += 1
    return temp

def goal_position(board, number):
   
    for i in range(ROWS):
        for j in range(COLS):
            if board[i][j] == number:
                return i, j
# manhattan_distance heuristic
def heuristic(board):
    goal_board=[goal[i:i+ROWS] for i in range(0,len(goal),ROWS)]
    c_state=[board[i:i+ROWS] for i in range(0,len(board),ROWS)]
    manhattan_distance = 0
    for row in range(ROWS):
        for col in range(COLS):
            number = c_state[row][col]
            x, y = goal_position(goal_board, number)
            manhattan_distance += abs(x - row) + abs(y - col)
    
    return manhattan_distance

# return a list of possible successor states
def successors(state):
    current_state = [state[i:i+ROWS] for i in range(0,len(state),ROWS)]
    successor_nodes=[]
# MOVE_LEFT
    for i in range(ROWS):
        child1=move_left(current_state,i)
        child_node = [x for sublist in child1 for x in sublist]
        successor_nodes.append([child_node,"L"+str(i+1)])
#MOVE_RIGHT

    for i in range(ROWS):
        child2=move_right(current_state,i)
        child_node = [x for sublist in child2 for x in sublist]
        successor_nodes.append([child_node,"R"+str(i+1)])

    for i in range(COLS):
        child3=move_up(current_state,i)
        child_node = [x for sublist in child3 for x in sublist]
        successor_nodes.append([child_node,"U"+str(i+1)])
    
    for i in range(COLS):
        child4=move_down(current_state,i)
        child_node = [x for sublist in child4 for x in sublist]
        successor_nodes.append([child_node,"D"+str(i+1)])


    child5=Ic_clockwise(current_state)
    child_node = [x for sublist in child5 for x in sublist]
    successor_nodes.append([child_node,"Ic"])
    

    child6=Ic_cclockwise(current_state)
    child_node = [x for sublist in child6 for x in sublist]
    successor_nodes.append([child_node,"Icc"])


    child7=Oc_clockwise(current_state)
    child_node = [x for sublist in child7 for x in sublist]
    successor_nodes.append([child_node,"Oc"])
    

    child8=Oc_cclockwise(current_state)
    child_node = [x for sublist in child8 for x in sublist]
    successor_nodes.append([child_node,"Occ"])
    

    return successor_nodes


# check if we've reached the goal
def is_goal(state):
    if state==goal:
        return True
    return False

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    board=list(initial_board)
    successor_nodes=list()
    #start_state = [initial_board[i:i+ROWS] for i in range(0,len(initial_board),ROWS)]
    route=[]
    fringe=[[0,board,route]]
    heapq.heapify(fringe)
    explored=[]
    while fringe:
        current_node=heapq.heappop(fringe)
        if is_goal(current_node[1]):
            break
        explored.append(current_node[1])
        successor_nodes=successors(current_node[1])
        for i in range(len(successor_nodes)):
            present=False
            f_score=heuristic(successor_nodes[i][0])+len(current_node[2])+1
            if successor_nodes[i][0] not in explored:
                for j in range(len(fringe)):
                    if successor_nodes[i][0]==fringe[j][1]:
                        present=True
                        break
                if not present:
                    heapq.heappush(fringe,(f_score,successor_nodes[i][0],current_node[2][0:] + [successor_nodes[i][1]]))
            for j in range(len(fringe)):
                if successor_nodes[i][0]==fringe[j][1] and f_score<fringe[j][0]:
                    heapq.heappush(fringe,(f_score,successor_nodes[i][0],current_node[2][0:] + [successor_nodes[i][1]]))
                    break
        
    return current_node[2]

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print(start_state)
    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
