# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # successor (state, action, cost)

    # initialize
    stk = util.Stack()  # a stack for dfs
    visited = {}  # a library for visited state : [father, action]

    start = problem.getStartState()
    visited[start] = [None, None]
    for successor in problem.getSuccessors(start):
        stk.push((successor, start))

    # dfs
    goal = None
    while not stk.isEmpty():
        cur = stk.pop()  # cur ((state, action, cost), father)
        if cur[0][0] not in visited:  # make sure cur won't be visited twice
            visited[cur[0][0]] = [cur[1], cur[0][1]]
            # print cur[0][0]
            if problem.isGoalState(cur[0][0]):
                goal = cur[0][0]
                break
            for successor in problem.getSuccessors(cur[0][0]):
                stk.push((successor, cur[0][0]))

    # output
    route = []
    while goal != start:  # trace back from goal to start
        route += [visited[goal][1]]
        goal = visited[goal][0]
    route.reverse()
    return route

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"

    # initialize
    queue = util.Queue()  # a queue for bfs
    visited = {}  # a library for visited state : [father, action]

    start = problem.getStartState()
    visited[start] = [None, None]
    for successor in problem.getSuccessors(start):
        queue.push((successor, start))

    # bfs
    goal = None
    while not queue.isEmpty():
        cur = queue.pop()  # cur ((state, action, cost), father)
        if cur[0][0] not in visited:  # make sure cur won't be visited twice
            visited[cur[0][0]] = [cur[1], cur[0][1]]
            # print cur[0][0]
            if problem.isGoalState(cur[0][0]):
                goal = cur[0][0]
                break
            for successor in problem.getSuccessors(cur[0][0]):
                queue.push((successor, cur[0][0]))

    # output
    route = []
    while goal != start :  # trace back from goal to start
        route += [visited[goal][1]]
        goal = visited[goal][0]
    route.reverse()
    return route

    util.raiseNotDefined()


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"

    # initialize
    pQ = util.PriorityQueue()  # a priority queue for ucs
    visited = {}  # a library for visited state : [father, action, costFromStart]

    start = problem.getStartState()
    visited[start] = [None, None, 0]
    for successor in problem.getSuccessors(start):
        # push in ( ((state, action, cost), father), priority = costFromStart )
        pQ.push((successor, start), successor[2])

    # ucs
    goal = None
    while not pQ.isEmpty():
        cur = pQ.pop()  # cur ((state, action, cost), father)
        if cur[0][0] not in visited:  # make sure cur won't be visited twice
            visited[cur[0][0]] = [cur[1], cur[0][1], visited[cur[1]][2] + cur[0][2]]
            if problem.isGoalState(cur[0][0]):
                goal = cur[0][0]
                break
            for successor in problem.getSuccessors(cur[0][0]):  # successor (state, action, cost)
                # push in ( ((state, action, cost), father), priority = costFromStart )
                pQ.push((successor, cur[0][0]), visited[cur[0][0]][2] + successor[2])

    # output
    route = []
    while goal != start:  # trace back from goal to start
        route += [visited[goal][1]]
        goal = visited[goal][0]
    route.reverse()
    return route

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"

    # initialize
    pQ = util.PriorityQueue()  # a priority queue for A*
    visited = {}  # a library for visited state : [father, action, costFromStart]

    start = problem.getStartState()
    visited[start] = [None, None, 0]
    for successor in problem.getSuccessors(start):
        # push in ( ((state, action, cost), father), priority = costFromStart + heuristic )
        pQ.push((successor, start), successor[2] + heuristic(successor[0], problem))

    # A*
    goal = None
    while not pQ.isEmpty():
        cur = pQ.pop()  # cur ((state, action, cost), father)
        if cur[0][0] not in visited:  # make sure cur won't be visited twice
            visited[cur[0][0]] = [cur[1], cur[0][1], visited[cur[1]][2] + cur[0][2]]
            if problem.isGoalState(cur[0][0]):
                goal = cur[0][0]
                break
            for successor in problem.getSuccessors(cur[0][0]):  # successor (state, action, cost)
                # push in ( ((state, action, cost), father), priority = costFromStart + heuristic )
                pQ.push((successor, cur[0][0]), visited[cur[0][0]][2] + successor[2] + heuristic(successor[0], problem))

    # output
    route = []
    while goal != start:  # trace back from goal to start
        route += [visited[goal][1]]
        goal = visited[goal][0]
    route.reverse()
    return route

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
