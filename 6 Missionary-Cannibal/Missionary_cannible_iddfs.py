class CannibalProblem:
    def __init__(self, start_state=(3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)
        self.total_missionaries = start_state[0]
        self.total_cannibals = start_state[1]

    # get successor states for the given state
    def get_successors(self, state):
        possible = set()  # all potential successor states
        final = set()     # all final successor states

        if state[2] == 1:  # boat on original side, subtract missionaries/cannibals
            possible.add((state[0]-1, state[1],   0))    # send one missionary on boat
            possible.add((state[0],   state[1]-1, 0))    # send one cannibal on boat
            possible.add((state[0]-1, state[1]-1, 0))    # send one missionary and one cannibal on boat
            possible.add((state[0]-2, state[1],   0))    # send two missionaries on boat
            possible.add((state[0],   state[1]-2, 0))    # send two cannibals on boat

        else:  # boat on other side, add missionaries/cannibals
            possible.add((state[0]+1, state[1],   1))  # bring back one missionary on boat
            possible.add((state[0],   state[1]+1, 1))  # bring back one cannibal on boat
            possible.add((state[0]+1, state[1]+1, 1))  # bring back one missionary and one cannibal on boat
            possible.add((state[0]+2, state[1],   1))  # bring back two missionaries on boat
            possible.add((state[0],   state[1]+2, 1))  # bring back two cannibals on boat

        for successor in possible:  # add all legal states in possible to final
            if self.is_legal(successor):
                final.add(successor)

        return final


    # get predecessors states for the given state
    def get_predecessors(self, state):
        possible = set()
        final = set()

        # pretty much the opposite logic of get_successors, to go up the tree rather than down
        if state[2] == 1:
            possible.add((state[0]-1, state[1],   0))
            possible.add((state[0],   state[1]-1, 0))
            possible.add((state[0]-1, state[1]-1, 0))
            possible.add((state[0]-2, state[1],   0))
            possible.add((state[0],   state[1]-2, 0))
        else:
            possible.add((state[0]+1, state[1],   1))
            possible.add((state[0],   state[1]+1, 1))
            possible.add((state[0]+1, state[1]+1, 1))
            possible.add((state[0]+2, state[1],   1))
            possible.add((state[0],   state[1]+2, 1))

        for state in possible:
            # check to see if it would be a legal start state
            if (state[0] >= 0 and state[1] >= 0) and ((state[0] >= state[1]) or state[0] == 0):
                final.add(state)

        return final

    # returns whether or not given state is legal in current CannibalProblem object
    def is_legal(self, state):
        # make sure that # of given missionaries/cannibals <= total missionaries/cannibals
        # as well as there are no negative quantities of missionaries/cannibals
        if 0 <= state[0] <= self.total_missionaries and 0 <= state[1] <= self.total_cannibals:
            # exception case where there are no missionaries on one side, still a valid state
            if state[0] == 0 or state[0] == self.total_missionaries:
                return True
            # general rule; there must be more missionaries than cannibals on both sides at all times
            return (state[0] >= state[1]) and \
                   ((self.total_missionaries - state[0]) >= (self.total_cannibals - state[1]))
        return False

    # returns whether or not given state is the goal state in current CannibalProblem object
    def goal_test(self, state):
        return state == self.goal_state

    def __str__(self):
        string = "Missionaries and cannibals problem: " + str(self.start_state)
        return string

class SearchSolution:
    def __init__(self, problem, search_method):
        self.problem_name = str(problem)
        self.search_method = search_method
        self.path = []
        self.nodes_visited = 0

    def __str__(self):
        string = "----\n"
        string += "{:s}\n"
        string += "Attempted with search method {:s}\n"

        if len(self.path) > 0:

            string += "Number of nodes visited: {:d}\n"
            string += "Solution length: {:d}\n"
            string += "Path: {:s}\n"

            string = string.format(self.problem_name, self.search_method,
                                   self.nodes_visited, len(self.path), str(self.path))
        else:
            string += "No solution found after visiting {:d} nodes\n"
            string = string.format(self.problem_name, self.search_method, self.nodes_visited)

        return string

# returns a SearchSolution object with given search_problem, search_method, and count and empty path
def no_solution(search_problem, search_method, count):
    solution = SearchSolution(search_problem, search_method)
    solution.nodes_visited = count
    return solution


# given search problem, found goal node, search method and count, returns corresponding SearchSolution object
# (constructs the path using backpointers from goal node)
def backchain(search_problem, goal_node, search_method, count):
    solution = SearchSolution(search_problem, search_method)
    solution.nodes_visited = count

    temp = goal_node
    solution.path.append(temp.state)
    while temp.parent is not None:
        solution.path.insert(0, temp.parent.state) # insert before child
        temp = temp.parent

    return solution


# returns true if test state is not equal to given node's state, or any of its (extended) predecessors, false otherwise
def not_in(given, test):
    temp = given
    while temp.parent is not None:
        if temp.state == test:
            return False
        temp = temp.parent
    if temp.state == test:
        return False
    return True

class SearchNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        

def dfs_search(search_problem, depth_limit=100, node=None, solution=None):
    # if no node object given, create a new search from starting state
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")

    solution.nodes_visited += 1  # increment nodes visited count
    # base case: test to see if goal is current node
    if search_problem.goal_test(node.state):
        return backchain(search_problem, node, "DFS", solution.nodes_visited)
    else:
        # base case: depth limit has been exceeded, handle accordingly
        if depth_limit-1 <= 0:  # -1 for logic purposes
            if node.state == search_problem.start_state:
                return no_solution(search_problem, "DFS", solution.nodes_visited)
            else:
                return None

        # recursive case: continue recursing down successors, searching for goal node
        for successor in search_problem.get_successors(node.state):
            if not_in(node, successor):
                result = dfs_search(search_problem, depth_limit-1, SearchNode(successor, node), solution)
                if result:  # ensure that result is not none
                    if not len(result.path) == 0:  # ensure that result is not no_result
                        return result
        # none of the successors had any promise, return no_solution
        return no_solution(search_problem, "DFS", solution.nodes_visited)

def ids_search(search_problem, depth_limit=100):
    count = 0 # keep track of nodes that were visited in failed depths
    for depth in range(depth_limit):
        solution = dfs_search(search_problem, depth)
        if not len(solution.path) == 0:  # actual solution found
            solution.search_method = "IDS" # this is IDS, not DFS
            solution.nodes_visited += count  # adding dfs searches of earlier depths
            return solution
        count += solution.nodes_visited  # solution was no good, add nodes visited to count
    return no_solution(search_problem, "IDS", count) # no solution found in given depth_limit


problem331 = CannibalProblem((3, 3, 1))
problem541 = CannibalProblem((5, 4, 1))
problem551 = CannibalProblem((5, 5, 1))

print(ids_search(problem331))

print(ids_search(problem551))

print(ids_search(problem541))