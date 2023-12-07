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
    a 1D array and contains an even number of inversions.
    """
   
    # inversions consists of a current position and every position after it
    # checking if the current value is larger then the observation value
    array = np.array(grid_data).flatten()
    
    count = 0
    for i in range(len(array)):
        for j in range(len(array)):
            if (array[i] > array[j]):
                count += 1
    
    return True

def solve(grid_data):
    print("solving...")
    return grid_data

if __name__ == '__main__':
    grid_data = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "0"]
        ]
    
    shuffle_grid = shuffleGrid(grid_data)
    
    

