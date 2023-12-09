import numpy as np
import timeit
import random
from solver import Solver
import sys, getopt

def shuffleGrid(grid_data, n):
    """
   transform 2D array into 1D array, then shuffles and returns
   shuffle 2D array
    """
    array = np.array(grid_data).flatten()
    random.shuffle(array)
    shuffled_grid = array.reshape((n, n))
    return shuffled_grid

def validateGrid(grid_data):
    """
    verifies that a shuffled grid is solvable by transforming
    a 1D array and contains an even number of inversions
    """
   
    # inversions consists of a current position and every position after it
    # checking if the current value is larger then the observation value
    array = np.array(grid_data).flatten()
    
    count = 0
    for i in range(len(array) - 1):
        for j in range(i + 1, len(array)):
            if (array[i] > array[j]):
                count += 1
    
    return True if count % 2 == 0 else False

def hScore(shuffle_grid, goal_grid):
    """
    heuristic function that compares the current state and the goal state
    h-score will be determine by the number of misplaced tiles 
    """

    print("heuristic value")

     
def solve(shuffle_grid, goal_grid):
    g_score = 0 # number of moves
    f_score = 0 # g_score + h_score

    print("solving...")
    return shuffle_grid

def a_star(init_state, goal_state, max_iter, heuristic):
    solver = Solver(init_state, goal_state, heuristic, max_iter)
    path = solver.solve_a_star()
    print(len(path))
    if len(path) == 0:
        exit(1)
    
    init_idx = init_state.flatten().tolist().index(0)
    init_i, init_j = init_idx // goal_state.shape[0], init_idx % goal_state.shape[0]
    
    print()
    print('INITIAL STATE')
    for i in range(goal_state.shape[0]):
        print(init_state[i, :]) 
    print()
    for node in reversed(path):
        cur_idx = node.get_state().index(0)
        cur_i, cur_j = cur_idx // goal_state.shape[0], cur_idx % goal_state.shape[0]
        
        new_i, new_j = cur_i - init_i, cur_j - init_j
        if new_j == 0 and new_i == -1:
            print('Moved UP    from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
        elif new_j == 0 and new_i == 1:
            print('Moved DOWN  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
        elif new_i == 0 and new_j == 1:
            print('Moved RIGHT from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
        else:
            print('Moved LEFT  from ' + str((init_i, init_j)) + ' --> ' + str((cur_i, cur_j)))
        print('Score using ' + heuristic + ' heuristic is ' + str(node.get_score() - node.get_level()) + ' in level ' + str(node.get_level()))
    
        init_i, init_j = cur_i, cur_j
        
        for i in range(goal_state.shape[0]):
            print(np.array(node.get_state()).reshape(goal_state.shape[0], goal_state.shape[0])[i, :]) 
        print()
    print(solver.get_summary())

if __name__ == '__main__':
    max_iter = 5000
    heuristic = "linear_conflict"
    algorithm = "a_star"
    n = 3
    
    goal_state = [
            [1, 2, 3],
            [4, 5, 6,],
            [7, 8, 0],
        ]
    
    #goal_state = [
    #        [1, 2, 3, 4],
    #        [5, 6, 7, 8],
    #        [9, 10, 11, 12],
    #        [13, 14, 15, 0],
    #    ]
    
    init_state = shuffleGrid(goal_state, n)

    init_state = np.array(init_state).reshape(n, n)
    goal_state = np.array(goal_state).reshape(n, n)
    
    a_star(init_state, goal_state, max_iter, heuristic)
    
    

