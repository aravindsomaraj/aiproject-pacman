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

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    
    frontier=util.Stack()              #FrontierList which stores the nodes which are to be expanded, in a stack structure

    frontier.push(problem.getStartState())   #Pushes the initial node into frontierlist
    explored=[]
    visited=[]

    path=util.Stack()               #this stores a path from the initial node to the current node, like explored list
    while True:

        if frontier.isEmpty():              #Checking to see if frontier list is empty
            return
        leafnode=frontier.pop()             #popping top element of frontier list

        if problem.isGoalState(leafnode):      #checking if it is a goal state. if so, we return the correct path
            return explored
        if leafnode not in visited:         #if the node hasn't been visited, we put it in the visited list. checking condition for same
            visited+=[leafnode]
            children=problem.getSuccessors(leafnode)  #gets the successor states of the current state
            for child,action,cost in children:
                frontier.push(child)                #pushes each of the nodes of the successor state into the frontierlist
                path.push(explored+[action])        #maintaining the path till the current node

        explored=path.pop()         #explored list now stores the path from initial node to the node that was just expanded
    

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    frontier=util.Queue()                   #FrontierList which stores the nodes which are to be expanded, in a queue structure

    frontier.push(problem.getStartState())      #Pushes the initial node into frontierlist
    explored=[]
    visited=[]

    path=util.Queue()                   #this stores a path from the initial node to the current node, like explored list
    while True:

        if frontier.isEmpty():          #Checking to see if frontier list is empty
            return
        leafnode=frontier.pop()         #popping front element element in queue of frontier list

        if problem.isGoalState(leafnode):       #checking if it is a goal state. if so, we return the correct path
            return explored
        if leafnode not in visited:         #if the node hasn't been visited, we put it in the visited list. checking condition for same
            visited+=[leafnode]
            children=problem.getSuccessors(leafnode)    #gets the successor states of the current state
            for child,action,cost in children:
                frontier.push(child)            #pushes each of the nodes of the successor state into the frontierlist
                path.push(explored+[action])    #maintaining the path till the current node

        explored=path.pop()             #explored list now stores the path from initial node to the node that was just expanded


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    frontier=util.PriorityQueue()           #FrontierList which stores the nodes which are to be expanded, in a PriorityQueue structure

    frontier.push(problem.getStartState(),0)        #Pushes the initial node into frontierlist, with initial cost zero
    explored=[]
    visited=[]
    path=util.PriorityQueue()           #this stores a path from the initial node to the current node, like explored list
    while True:

        if frontier.isEmpty():          #Checking to see if frontier list is empty
            return
        leafnode=frontier.pop()         #popping top element of frontier list

        if problem.isGoalState(leafnode):       #checking if it is a goal state. if so, we return the correct path
            return explored
        if leafnode not in visited:             #if the node hasn't been visited, we put it in the visited list. checking condition for same
            visited+=[leafnode]
            children=problem.getSuccessors(leafnode)        #gets the successor states of the current state
            for child,action,cost in children:
                pathCost=problem.getCostOfActions(explored+[action])  #computes the path cost from the initial node to the next node
                if child not in visited:
                    path.push(explored+[action],pathCost)       #maintaining the path till the current node, and the pathCost till the current node too
                    frontier.push(child,pathCost)               #pushes each of the nodes of the successor state into the frontierlist
                
        
        explored=path.pop()                 #explored list now stores the path from initial node to the node that was just expanded


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    frontier=util.PriorityQueue()       #FrontierList which stores the nodes which are to be expanded, in a PriorityQueue structure

    frontier.push(problem.getStartState(),0)        #Pushes the initial node into frontierlist, with initial cost zero
    explored=[]
    visited=[]
    path=util.PriorityQueue()       #this stores a path from the initial node to the current node, like explored list
    while True:

        if frontier.isEmpty():          #Checking to see if frontier list is empty
            return
        leafnode=frontier.pop()         #popping top element of frontier list

        if problem.isGoalState(leafnode):       #checking if it is a goal state. if so, we return the correct path
            return explored
        if leafnode not in visited:     #if the node hasn't been visited, we put it in the visited list. checking condition for same
            visited+=[leafnode]
            children=problem.getSuccessors(leafnode)    #gets the successor states of the current state
            for child,action,cost in children:
                pathCost=problem.getCostOfActions(explored+[action])+heuristic(child,problem)  #in addition to computing the cost from inital node to current node, the heuristic function also computes the cost from the current node to nearest goal state, unlike UCS which is just g(n)
                if child not in visited:
                    path.push(explored+[action],pathCost)   #maintaining the path till the current node
                    frontier.push(child,pathCost)          #pushes each of the nodes of the successor state into the frontierlist
                
        
        explored=path.pop()         #explored list now stores the path from initial node to the node that was just expanded



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
