from copy import deepcopy
import random
import numpy as np

class GridNode:
    def __init__(self, grid, g_score = 0, f_score = 0):
        """
        graph instance contain the grid, g_score which is the amount of moves, 
        and f_score which is g_score + h_score
        """
        self.grid = grid
        self.g_score = g_score
        self. f_score = f_score

    def nextMoves(self):
        """
        create children to be able to choose the best child 
        """
        # possible moves
        x, y = self.findCoord(0)
        move_up = [x, y - 1]
        move_down = [x, y + 1]
        move_left = [x - 1, y]
        move_right = [x + 1, y]

        children = []
        for move in [move_up, move_down, move_left, move_right]:
            child = self.verifyMove(x, y, move[0], move[1])

            if child is None:
                continue
            
            new_GridNode = GridNode(child, self.g_score + 1, 0)
            children.append(new_GridNode)

            # print(f"move: {move}")
            # print(new_GridNode.grid)

        return children
    
    def verifyMove(self, curr_coord_x, curr_coord_y, future_coord_x, future_coord_y):
        """
        test the blank tile in new directional tile and verify
        within bounds of the grid
        """
        if (0 <= future_coord_x < len(self.grid) and
            0 <= future_coord_y < len(self.grid)):

            # switch blank tile with tile in its new position
            temp_grid = deepcopy(self.grid)
            temp_val = temp_grid[future_coord_x][future_coord_y]
            temp_grid[future_coord_x][future_coord_y] = temp_grid[curr_coord_x][curr_coord_y]
            temp_grid[curr_coord_x][curr_coord_y] = temp_val

            return temp_grid
        else:
            return None
     

    def findCoord(self, target_val):
        """
        determine coordinate points of provided value
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == target_val:
                    return [i, j]

class SlidingPuzzle:
    def __init__(self, n):
        """
        sliding puzzle instance which track the tree that being created
        from the available moves and choice of best move
        """
        self.n = n
        self.open_list = []
        self.close_list = []

    def generateStartGrid(self):
        """
       create a list of random value from 0 - n then reshape 
       into a n x n grid
        """
        values = np.arange(self.n**2)
        np.random.shuffle(values)
       
        return values.reshape((self.n, self.n))
    
    def generateGoalGrid(self):
        """
        create a list of values from 1 - n and 0 then reshape
        into a n x n grid
        """
        values = np.arange(1, self.n**2)
        values = np.append(values, 0)

        return values.reshape((self.n, self.n))

    def hScore(self, curr_grid, goal_grid):
        """
        h-score will be determine by the number of misplaced tiles 
        """  
        if np.array_equal(curr_grid, goal_grid):
            return 0

        misplaced_coord= np.where(curr_grid != goal_grid)
        misplaced = len(misplaced_coord[0])
        
        return misplaced
    
    def fScore(self, curr_GridNode, goal_grid):
        g_score = curr_GridNode.g_score
        h_score = self.hScore(curr_GridNode.grid, goal_grid)

        return g_score + h_score

    def solve(self):
        start_grid = self.generateStartGrid() 
        goal_grid = self.generateGoalGrid()
        # start_grid = np.array([
        #         [1, 2, 3],
        #         [0, 4, 6],
        #         [7, 5, 8]
        #     ])
        # goal_grid = np.array( [
        #         [1, 2, 3],
        #         [4, 5, 6],
        #         [7, 8, 0]
        #     ])

        start_GridNode = GridNode(start_grid)
        start_GridNode.f_score = self.fScore(start_GridNode, goal_grid)
        self.open_list.append(start_GridNode)

        #
        while True:
            current_GridNode = self.open_list[0]
            print("Current Grid:")
            print(current_GridNode.grid)
            print("X-----X-----X")

            # h_score is 0 because no misplaced tiles exist 
            if self.hScore(current_GridNode.grid, goal_grid) == 0:
                break

            # create children
            for child_GridNode in current_GridNode.nextMoves():
                # print("printing childGridNode")
                # print(child_GridNode.grid)
                child_GridNode.f_score = self.fScore(child_GridNode, goal_grid)
                self.open_list.append(child_GridNode)

            # print("done printing childGridNode")
            #
            self.close_list.append(current_GridNode)
            del self.open_list[0]
          
            #self.open_list.sort(key = lambda x:x.f_score, reverse=False)
        

if __name__ == '__main__':
    game = SlidingPuzzle(3)
    game.solve()

  