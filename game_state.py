import numpy as np

class GameState():
    def __init__(self, state, goal_state, level, parent = None, heuristic_func = "manhattan"):
        self.__state = state
        self.__goal_state = goal_state
        self.__level = level
        self.__heuristic_func = heuristic_func
        self.__heuristic_score = level
        self.__parent = parent
        self.calculate_fitness()
        
    def __hash__(self):
        return hash(str(self.__state))
        
    def __lt__(self, other):
        return self.__heuristic_score < other.__heuristic_score
    
    def __eq__(self, other):
        return self.__heuristic_score == other.__heuristic_score
    
    def __gt__(self, other):
        return self.__heuristic_score > other.__heuristic_score
    
    def get_state(self):
        return self.__state
    
    def get_score(self):
        return self.__heuristic_score
    
    def get_level(self):
        return self.__level
    
    def get_parent(self):
        return self.__parent
    
    def calculate_fitness(self):
        if self.__heuristic_func == "misplaced_tiles":
            for cur_tile, goal_tile in zip(self.__state, self.__goal_state):
                if cur_tile != goal_tile:
                    self.__heuristic_score += 1
        elif self.__heuristic_func == "manhattan":
            for cur_tile in self.__state:
                cur_idx = self.__state.index(cur_tile)
                goal_idx = self.__goal_state.index(cur_tile)
                cur_i, cur_j = cur_idx // int(np.sqrt(len(self.__state))), cur_idx % int(np.sqrt(len(self.__state)))
                goal_i, goal_j = goal_idx // int(np.sqrt(len(self.__state))), goal_idx % int(np.sqrt(len(self.__state)))
                self.__heuristic_score += self.calculate_manhattan(cur_i, cur_j, goal_i, goal_j)
        elif self.__heuristic_func == "linear_conflict":
             for cur_tile, goal_tile in zip(self.__state, self.__goal_state):
                cur_idx = self.__state.index(cur_tile)
                self.__heuristic_score += self.linear_conflict(cur_idx, cur_tile, goal_tile)
        else:
            print('Unknown heuristic function is being used.')
            
    def calculate_manhattan(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
    
    def linear_conflict(self, i, line, dest):
        conflicts = 0
        conflict_graph = {}
        for j, u in enumerate(line):
            if u == 0:
                continue
            x, y = dest(u)
            if i != x:
                continue

            for k in range(j + 1, self.n):
                # opposing tile
                v = line[k]
                if v == 0:
                    continue
                tx, ty = dest(v)
                if tx == x and ty <= y:
                    u_degree, u_nbrs = conflict_graph.get(u) or (0, set())
                    u_nbrs.add(v)
                    conflict_graph[u] = (u_degree + 1, u_nbrs)
                    v_degree, v_nbrs = conflict_graph.get(v) or (0, set())
                    v_nbrs.add(u)
                    conflict_graph[v] = (v_degree + 1, v_nbrs)
        while sum([v[0] for v in conflict_graph.values()]) > 0:
            popped = max(conflict_graph.keys(),
                         key=lambda k: conflict_graph[k][0])
            for neighbour in conflict_graph[popped][1]:
                degree, vs = conflict_graph[neighbour]
                vs.remove(popped)
                conflict_graph[neighbour] = (degree - 1, vs)
                conflicts += 1
            conflict_graph.pop(popped)
        return conflicts