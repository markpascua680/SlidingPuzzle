import numpy as np
import timeit
import random

def shuffleGrid(grid_data):
    """
   transform 2D array into 1D array, then shuffles and returns
   shuffle 2D array
    """
    array = np.array(grid_data).flatten()
    random.shuffle(array)
    shuffled_grid = array.reshape((3, 3))
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

if __name__ == '__main__':
    goal_grid = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "0"],
        ]
    
    shuffle_grid = shuffleGrid(goal_grid)
    solve(shuffle_grid, goal_grid)
    
    

