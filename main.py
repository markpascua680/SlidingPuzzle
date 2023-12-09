from copy import copy, deepcopy
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

    astar(shuffle_grid, shuffle_grid, goal_grid)
    return shuffle_grid

def get_empty_tile_position(grid_values):
    for x, row in enumerate(grid_values):
        for y, column in enumerate(row):
            if (column == '0'):
                return [x, y]

def is_invalid_move(grid_node, move):
    """
    ensure that the move stays within grid dimensions
    """
    projected_x_move = grid_node.empty_tile_position[0] + move[0]
    projected_y_move = grid_node.empty_tile_position[1] + move[1]

    grid_width = len(grid_node.grid_values[0]) - 1
    grid_height = len(grid_node.grid_values) - 1

    if (projected_x_move > grid_width or projected_x_move < 0):
        return True
    elif (projected_y_move > grid_height or projected_y_move < 0):
        return True
    return False

def move_empty_tile(grid_node, move):
    if (is_invalid_move(grid_node, move)):
        return None

    new_grid_node = copy(grid_node)

    # Get position and value of the tile that is going to be moved into the empty tile
    tile_to_move_position = [new_grid_node.empty_tile_position[0] + move[0], new_grid_node.empty_tile_position[1] + move[1]]
    tile_to_move_value = new_grid_node.grid_values[tile_to_move_position[0]][tile_to_move_position[1]]

    # Swap values
    new_grid_node.grid_values[tile_to_move_position[0]][tile_to_move_position[1]] = 0
    new_grid_node.grid_values[new_grid_node.empty_tile_position[0]][new_grid_node.empty_tile_position[1]] = tile_to_move_value
    
    new_grid_node.empty_tile_position = tile_to_move_position

    return new_grid_node

class GridNode():    
    def __init__(self, parent=None, grid_values=None, empty_tile_position=None):
        self.parent = parent
        self.grid_values = grid_values
        self.empty_tile_position = empty_tile_position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        grid1 = deepcopy(self.grid_values)
        grid2 = deepcopy(other.grid_values)
        return np.array_equal(grid1, grid2)

def astar(grid, start, end):

    # Create start and end node
    start_grid_node = GridNode(None, start, get_empty_tile_position(start))
    start_grid_node.g = start_grid_node.h = start_grid_node.f = 0
    end_grid_node = GridNode(None, end, get_empty_tile_position(end))
    end_grid_node.g = end_grid_node.h = end_grid_node.f = 0
    
    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_grid_node)

    # Possible moves
    move_up = [0, -1]
    move_down = [0, 1]
    move_left = [-1, 0]
    move_right = [1, 0]

    # Loop until you find the end
    while len(open_list) > 0:
    #for i in range(3):

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_grid_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.grid_values)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        #print("PRINTING CURRENT CHILDREN")
        for move in [move_up, move_down, move_left, move_right]: # Adjacent squares

            # Get grid node values
            new_node = deepcopy(current_node)
            new_grid_node = move_empty_tile(new_node, move)
            
            # Make sure move is valid; new_grid_values is none if the move is invalid
            if (new_grid_node is None):
                continue

            #print(current_node.grid_values, 'CURRENT')
            #print(new_grid_node.grid_values, 'NEW')
            #print('----------------------------')

            # Append
            children.append(deepcopy(new_grid_node))
            
        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child.__eq__(closed_child):
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            #child.h = ((child.position[0] - end_grid_node.position[0]) ** 2) + ((child.position[1] - end_grid_node.position[1]) ** 2)
            child.h = count_misplaced_tiles(child, end_grid_node)
            child.f = child.g + child.h
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            #print(child.grid_values)
            #print('=========================')
            # Add the child to the open list
            open_list.append(deepcopy(child))

def count_misplaced_tiles(current_node, goal_node):
    count = 0
    grid1 = current_node.grid_values.flatten()
    grid2 = goal_node.grid_values.flatten()
    
    for i in range(len(grid1)):
        if grid1[i] == grid2[i]:
            count += 1

    return count

if __name__ == '__main__':
    goal_grid = [
            ["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "0"],
        ]
    
    shuffle_grid = shuffleGrid(goal_grid)
    goal_grid = np.array(goal_grid).reshape(3, 3)

    solve(shuffle_grid, goal_grid)
    
    

