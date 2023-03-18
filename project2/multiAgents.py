# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        

        from util import manhattanDistance

        food = newFood.asList()
        Distancetofood = []                  #stores the manhattan distance from current state of pacman to food posns
        Distancetoghost = []                #stores the manhattan distance from the current state of pacman to ghost posns
        score = 0 

        if successorGameState.isWin():
            return 10000
        
        for item in food:
            Distancetofood+=[(manhattanDistance(newPos,item))] #assigns the manhattan distance to each food item in the layout to the distancetofoodlist

        for dis in Distancetofood:              #score is evaluated according to the distance values in distancetofood list
            if dis <= 2:
                score += 3.5
            elif dis>2 and dis <= 4:               #for less dis, score is more
                score += 2
            elif dis> 4 and dis <= 10:
                score += 0.5
            else:
                score += 0.15

        for ghost in successorGameState.getGhostPositions():        #assigns the manhattan distance to each ghost in the layout to the distancetoghost list
            Distancetoghost+=[(manhattanDistance(ghost,newPos))]

        for ghost in successorGameState.getGhostPositions():
            if ghost == newPos:                                     #when we get closer to ghost, score decreases. if ghost is in the next position, we decrement score
                score = score-200

            elif manhattanDistance(ghost,newPos) <= 3.5:
                score = score-50
        
        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"


        def minimaxDecision(gameState):
            actions = gameState.getLegalActions(0)
            intitialScore = -10000
            for act in actions:
                nextState = gameState.generateSuccessor(0,act)
            # We always go into the minimising player level first from the root
                score = minPlay(nextState,0,1)
            #Overwriting the score
                if score > intitialScore:
                    returnAction = act
                    intitialScore = score
            return returnAction
        
        #funtion to find return the pacman's choice
        def maxPlay(gameState,depth):
    
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose() or self.depth==depth + 1:    
                return self.evaluationFunction(gameState)
            maxvalue = -10000
            actions = gameState.getLegalActions(0)
            for act in actions:
                successor= gameState.generateSuccessor(0,act)
                #finding the maximum of the both the values
                maxvalue = max (maxvalue,minPlay(successor,depth + 1,1))
            return maxvalue
        
        ##funtion to find return the ghost's choice
        def minPlay(gameState,depth, agentIndex):
            
            minvalue = 10000
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose() or depth==self.depth:    
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            for act in actions:
                successor= gameState.generateSuccessor(agentIndex,act)
                #finding the minimum of the both the values
                if agentIndex == (gameState.getNumAgents() - 1):
                    minvalue = min (minvalue,maxPlay(successor,depth))
                else:
                    minvalue = min(minvalue,minPlay(successor,depth,agentIndex+1))
            return minvalue
        
        return minimaxDecision(gameState)
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "* YOUR CODE HERE *"
        
        def AlphaBeta(gameState):
            actions = gameState.getLegalActions(0)
            intitialScore = -10000
            alpha = -10000
            beta = 10000
            for act in actions:
                nextState = gameState.generateSuccessor(0,act)
                # We always go into the minimising player level first from the root
                score = minPlay(nextState,0,1,alpha,beta)
                #Overwriting the score
                if score > intitialScore:
                    returnAction = act
                    intitialScore = score
            # Updating alpha value at root.    
                if score > beta:
                    return returnAction
                alpha = max(alpha,score)
            return returnAction
        
        #funtion to find return the pacman's choice
        def maxPlay(gameState,depth,alpha, beta):
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose() or self.depth==depth+1:   #Terminal Test 
                return self.evaluationFunction(gameState)
            maxvalue = -10000
            curr_alpha = alpha
            actions = gameState.getLegalActions(0)
            for act in actions:
                successor= gameState.generateSuccessor(0,act)
                #finding the maximum of the both the values
                maxvalue = max (maxvalue,minPlay(successor,depth+1,1,curr_alpha,beta))
                if maxvalue > beta:
                    return maxvalue
                curr_alpha = max(curr_alpha,maxvalue)
            return maxvalue
        
        ##funtion to find return the ghost's choice
        def minPlay(gameState,depth,agentIndex,alpha,beta):
            minvalue = 10000
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose():   #Terminal Test 
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            curr_beta = beta
            for act in actions:
                #finding the minimum of the both the values
                successor= gameState.generateSuccessor(agentIndex,act)
                if agentIndex == (gameState.getNumAgents()-1):
                    minvalue = min (minvalue,maxPlay(successor,depth,alpha,curr_beta))
                    if minvalue < alpha:
                        return minvalue
                    curr_beta = min(curr_beta,minvalue)
                else:
                    minvalue = min(minvalue,minPlay(successor,depth,agentIndex+1,alpha,curr_beta))
                    if minvalue < alpha:
                        return minvalue
                    curr_beta = min(curr_beta,minvalue)
            return minvalue
        
        return AlphaBeta(gameState)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "* YOUR CODE HERE *"
        def minimaxDecision(gameState):
            actions = gameState.getLegalActions(0)
            currentScore = -10000
            for act in actions:
                nextState = gameState.generateSuccessor(0,act)
            # We always go into the minimising player level first from the root
                score = minPlay(nextState,0,1)
            #Overwriting the score
                if score > currentScore:
                    returnAction = act
                    currentScore = score
            return returnAction
    
        #funtion to find return the pacman's choice
        def maxPlay(gameState,depth):
    
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose() or self.depth==depth + 1:   #Terminal Test 
                return self.evaluationFunction(gameState)
            maxvalue = -10000
            actions = gameState.getLegalActions(0)
            
            for act in actions:
                successor= gameState.generateSuccessor(0,act)
                maxvalue = max (maxvalue,minPlay(successor,depth + 1,1))
                #finding the maximum of the both the values
            return maxvalue
        
        ##funtion to find return the ghost's choice
        def minPlay(gameState,depth, agentIndex):
            
            # checking the terminal condition
            if gameState.isWin() or gameState.isLose() or depth==self.depth:   #Terminal Test 
                return self.evaluationFunction(gameState)
            actions = gameState.getLegalActions(agentIndex)
            finalVal = 0
            numberofactions = len(actions)
            for act in actions:
                successor= gameState.generateSuccessor(agentIndex,act)
                #finding the minimum of the both the values
                if agentIndex == (gameState.getNumAgents() - 1):
                    max=maxPlay(successor,depth)
                else:
                    max = minPlay(successor,depth,agentIndex+1)
                finalVal+=max
            if numberofactions == 0:
                return  0
            return float(finalVal)/(numberofactions)
        
        return minimaxDecision(gameState)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
# Abbreviation
better = betterEvaluationFunction
