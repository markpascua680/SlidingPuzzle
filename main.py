import copy
import random
def shuffleGrid(grid_data, n):
    """
   transform 2D array into 1D array, then shuffles and returns
   shuffle 2D array
    """
    for i in range(n - 1):
        random.shuffle(grid_data[i])

    random.shuffle(grid_data)
    
    return grid_data

     
def solve(shuffle_grid, goal_grid):
    print("solving...")
    return a_star(shuffle_grid, goal_grid)

class Node:
    def __init__(self,data,level,f_score):
        """ Initialize the node with the data, level of the node and the calculated fvalue """
        self.data = data
        self.level = level
        self.f_score = f_score

def get_f_score(start, goal):
    score = 0
    n = len(start.data)

    for i in range(0, n):
        for j in range(0, n):
            if start.data[i][j] != goal[i][j] and start [i][j] != 0:
                score += 1

    return score

def get_children(current_node):
    x, y = current_node.find(current_node.data, '0')

    children = []
    moves = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]

    for move in moves:
        child = move(current_node.data, x, y, move[0], move[1])
        if child is not None:
                child_node = Node(child, current_node.level + 1, 0)
                children.append(child_node)
    return children

def move(node_data, x1, y1, x2, y2):
    if x2 >= 0 and x2 < len(node_data) and y2 >= 0 and y2 < len(node_data):
        temp_data = []
        temp_data = copy(node_data)
        temp = temp_data[x2][y2]
        temp_data[x2][y2] = temp_data[x1][y1]
        temp_data[x1][y1] = temp
        return temp_data
    return None


def a_star(init_state, goal_state):
    n_size = len(init_state)
    open_list = []
    closed_list = []

    start = Node(init_state,0,0)
    start.f_score = get_f_score(start, goal_state)
    """ Put the start node in the open list"""
    open_list.append(start)
    print("\n\n")
    while True:
        cur = open_list[0]
        print("")
        print("  | ")
        print("  | ")
        print(" \\\'/ \n")
        for i in cur.data:
            for j in i:
                print(j,end=" ")
            print("")
        """ If the difference between current and goal node is 0 we have reached the goal node"""
        if(get_f_score(cur.data, goal_state) == 0):
            break
        for i in cur.get_children():
            i.f_score = get_f_score(i, goal_state)
            open_list.append(i)
        closed_list.append(cur)
        open_list.pop(0)

        """ sort the opne list based on f value """
        open_list.sort(key = lambda x:x.f_score, reverse=False)

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
    
    initial_state = shuffleGrid(goal_state, n)
    
    solve(initial_state, goal_state)
