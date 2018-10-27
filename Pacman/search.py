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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

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
    import game
    succes = []
    sucstack = util.Stack()
    hf = problem.getStartState()
    succ = (hf,'Stop',0)
    while(True):
        if(succ == 'return'):
            succes.pop()
        else:
            succes.append(succ)
            if(problem.isGoalState(succ[0])): break
            sucstack.push('return')
            for ss in problem.getSuccessors(succ[0]):
                flag = True
                for i in range(len(succes),0,-1):
                    if(ss[0] == succes[i - 1][0]):
                        flag = False
                        break
                if(flag): sucstack.push(ss)
        if(sucstack.isEmpty()):break
        succ= sucstack.pop()
            
    actions = []
    for s in succes:
        actions.append(s[1])
    return actions[1:]

    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    import game
    succes = []
    sucqueue = util.Queue()
    succ = (problem.getStartState(),'Stop',0)
    lp = -1
    Flg = True
    while(Flg):
        succes.append((succ,lp))
        for ss in problem.getSuccessors(succ[0]): 
            if(problem.isGoalState(ss[0])):
                succes.append((ss,len(succes)-1))
                Flg = False
                break
            flag = True
            for i in range(len(succes),0,-1):
                if(ss[0] == succes[i - 1][0][0]):
                    flag = False
                    break
            if(flag): sucqueue.push((ss,len(succes)-1))
        if(sucqueue.isEmpty() or Flg==False):break
        succ, lp = sucqueue.pop()
    action = []
    lp = len(succes)-1
    while(lp!=0):
        action.append(succes[lp][0][1])
        lp = succes[lp][1]
    action.reverse()
    return action

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    import game
    succes = []
    sucqueue = util.PriorityQueue()
    succ = (problem.getStartState(),'Stop',0)
    lp = -1
    gn = 0
    while(True):
        succes.append((succ,lp,gn))
        if(problem.isGoalState(succ[0])):
            succes.append((ss,len(succes)-1))
            break
        for ss in problem.getSuccessors(succ[0]): 
            flag = True
            for i in range(len(succes),0,-1):
                if(ss[0] == succes[i - 1][0][0]):
                    flag = False
                    break
            if(flag): sucqueue.push((ss,len(succes)-1,gn+ss[2]),gn+ss[2])
        if(sucqueue.isEmpty()):break
        succ, lp, gn = sucqueue.pop()
    action = []
    lp = len(succes)-1
    while(lp!=0):
        action.append(succes[lp][0][1])
        lp = succes[lp][1]
    action.reverse()
    return action

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    import game
    succes = []
    sucqueue = util.PriorityQueue()
    succ = (problem.getStartState(),'Stop',0)
    lp = -1
    gn = 0
    hn = 0
    while(True):
        succes.append((succ,lp,gn))
        if(problem.isGoalState(succ[0])):
            succes.append((ss,len(succes)-1))
            break
        for ss in problem.getSuccessors(succ[0]): 
            flag = True
            for i in range(len(succes),0,-1):
                if(ss[0] == succes[i - 1][0][0]):
                    flag = False
                    break
            if(flag):
                hn = heuristic(ss[0],problem)
                sucqueue.push((ss,len(succes)-1,gn+ss[2]),gn+ss[2]+hn)
        if(sucqueue.isEmpty()):break
        succ, lp, gn = sucqueue.pop()
    action = []
    lp = len(succes)-1
    while(lp!=0):
        action.append(succes[lp][0][1])
        lp = succes[lp][1]
    action.reverse()
    return action


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
