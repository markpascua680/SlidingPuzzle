from bisect import bisect_left, insort
from queue import Empty, PriorityQueue
import time
import numpy as np
import random
import heuristics
from actions import up, down, left, right

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

class Node(object): # pylint: disable=too-few-public-methods
	def __init__(self, state, parent, action_taken):
		self.state = state
		self.parent = parent
		self.action_taken = action_taken
		self.num_parents = 0 if parent == None else parent.num_parents + 1

	# ordering does not matter, needed for use in priority queue when priorities are equal
	def __lt__(self, other): return False 
	
def _bisect_index(collection, value):
	"""
	Searches collection for value using binary search, returning the index of value or None.
	collection _must_ be sorted!
	"""
	for thing in collection:
		print(thing, value)
	i = bisect_left(collection, value)
	if i != len(collection) and collection[i] == value:
		return i
	return None
	
def _state_is_valid(state, closed_set):
	return (state is not None and 
			_bisect_index(closed_set, state) == None)

def _search(initial_state, desired_state, open_set_get, open_set_add):
	"""
	Avoids repetition of the generic parts of all of the search strategies. 
	The search strategies turn out to be similar except in the way the open set data structure works. 
	open_set_get: () -> Node. Pulls the next relevant node from the open set.
	open_set_add: Node -> (). Adds a successor node to the open set.
	reverse_add_calls: Adds successors to open_set in order right, down, left, up instead of up, left, down, right.
	"""
	def open_set_add_if_new(successor_state, action_taken):
		if _state_is_valid(successor_state, closed_set):
			open_set_add(Node(successor_state, current_node, action_taken))

	def reconstruct_actions(node):
		actions = []
		while node.action_taken != None:
			actions.append(node.action_taken)
			node = node.parent
		return actions

	closed_set = []
	current_node = Node(initial_state, None, None)
	while current_node.state is not desired_state:
		insort(closed_set, current_node.state) # adds state to closed_set while maintaining sorted order.
		
		open_set_add_if_new(up(current_node.state), "Up;")
		open_set_add_if_new(left(current_node.state), "Left;")
		open_set_add_if_new(down(current_node.state), "Down;")
		open_set_add_if_new(right(current_node.state), "Right;")

		try:
			current_node = open_set_get()
		except (IndexError, Empty):
			return len(closed_set), None

	return len(closed_set), reconstruct_actions(current_node)

def a_star(initial_state, desired_state, heuristic=heuristics.manhattan_distance):
	"""
	Like greedy best-first, except considers the cost already incurred to reach the current state in addition
	  to the value of the heuristic.
	This results in interesting behaviour where promising paths can be pursued relentlessly like 
		depth-first search, but when paths appear similar each of them are considered. 
	Complete, optimal because heuristic is monotone, very fast (fastest informed) for this puzzle.
	"""
	def open_set_add(node):
		priority = node.num_parents + heuristic(node.state, desired_state)
		open_set.put( (priority, node) )

	def open_set_get():
		_, node = open_set.get_nowait()
		return node

	open_set = PriorityQueue() # contains (priority, Node)
	return _search(initial_state, desired_state, open_set_get, open_set_add)

def dijkstra(initial_state, desired_state):
	"""
	Like breadth-first search in spirit, except expands nodes with the least cost incurred so far
		first rather than nodes with the least parents first. As all actions have equal cost in this 
		puzzle, it is equivalent to breadth-first search, but may expand nodes slightly differently 
		due to how the PriorityQueue data structure sorts nodes of equal priority. 
	It is equivalent to A* with a heuristic of 0 in all cases.
	Complete, optimal, slow for this puzzle.
	"""
	return a_star(initial_state, desired_state, heuristic=lambda current_state, desired_state: 0)

if __name__ == '__main__':
    max_iter = 5000
    heuristic = "manhattan_distance"
    algorithm = "a_star"
    n = 3
    
    goal_state = [
            ['1', '2', '3'],
            ['4', '5', '6',],
            ['7', '8', '0'],
        ]
    
    #goal_state = [
    #        [1, 2, 3, 4],
    #        [5, 6, 7, 8],
    #        [9, 10, 11, 12],
    #        [13, 14, 15, 0],
    #    ]
    
    initial_state = shuffleGrid(goal_state, n)
    desired_state = goal_state
	
    start_time = time.process_time() # does not include time process was swapped out

    if (heuristic == ''):
        number_of_nodes, solution = dijkstra(initial_state, desired_state)
    else:
        number_of_nodes, solution = a_star(initial_state, desired_state, heuristics.manhattan_distance)
    print("Time taken: " + str(time.process_time() - start_time) + " secs")
    
    

