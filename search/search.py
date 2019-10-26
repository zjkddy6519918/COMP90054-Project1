# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Model:
    """
    This class aims to do preprocesses, including creating initial nodes and success nodes,
    calulating the path, and designing a common algorithm which can be invoked by different
    searching algorithms.
    """
    def make_root_node(self,init_state):
        """
        initial the root node, of which the information is stored in dict
        """
        init_node = {
            "state":init_state,
            "parent":None,
            "action":None,
        }
        return init_node

    def make_succ_node(self,curr_node,successor):
        """
        add information in successor nodes
        """
        succ_node = {
            "state":successor[0],
            "parent":curr_node,
            "action":successor[1],
        }
        return succ_node

    def make_actions(self,goal_node):
        """
        return a list of actions that reaches the
        goal.
        """
        actions = []
        while (goal_node["parent"]):
            actions.append(goal_node["action"])
            goal_node = goal_node["parent"]
        actions = actions[::-1]
        return actions



def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

model = Model()

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***" 
    init_state = problem.getStartState()
    init_node  = model.make_root_node(init_state)
    frontier = util.Stack()
    frontier.push(init_node)
    explored_set = []
    while not frontier.isEmpty():
        node = frontier.pop()
        if node["state"] not in explored_set:
            explored_set.append(node["state"])
            if problem.isGoalState(node["state"]):
                return model.make_actions(node)
            for successor in problem.getSuccessors(node["state"]):
                succ_node = model.make_succ_node(node,successor)
                frontier.push(succ_node)
    return None
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    init_state = problem.getStartState()
    init_node  = model.make_root_node(init_state)
    frontier = util.Queue()
    frontier.push(init_node)
    explored_set = []
    while not frontier.isEmpty():
        node = frontier.pop()
        if node["state"] not in explored_set:
            explored_set.append(node["state"])
            if problem.isGoalState(node["state"]):
                return model.make_actions(node)
            for successor in problem.getSuccessors(node["state"]):
                succ_node = model.make_succ_node(node,successor)
                frontier.push(succ_node)
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    init_state = problem.getStartState()
    init_node  = model.make_root_node(init_state)
    frontier = util.PriorityQueue()
    frontier.push(init_node,0)
    explored_set = []
    while not frontier.isEmpty():
        node = frontier.pop()
        if node["state"] not in explored_set:
            explored_set.append(node["state"])
            if problem.isGoalState(node["state"]):
                return model.make_actions(node)
            for successor in problem.getSuccessors(node["state"]):
                succ_node = model.make_succ_node(node,successor)
                succ_actions = model.make_actions(succ_node)
                succ_cost = problem.getCostOfActions(succ_actions)
                frontier.update(succ_node,succ_cost)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    init_state = problem.getStartState()
    init_node  = model.make_root_node(init_state)
    frontier = util.PriorityQueue()
    frontier.push(init_node,0)
    explored_set = []
    while not frontier.isEmpty():
        node = frontier.pop()
        if node["state"] not in explored_set:
            explored_set.append(node["state"])
            if problem.isGoalState(node["state"]):
                return model.make_actions(node)
            for successor in problem.getSuccessors(node["state"]):
                succ_node = model.make_succ_node(node,successor)
                succ_actions = model.make_actions(succ_node)
                g = problem.getCostOfActions(succ_actions)
                h = heuristic(succ_node["state"],problem)
                f = g + h
                frontier.update(succ_node,f)
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

