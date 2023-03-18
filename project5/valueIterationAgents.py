# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        
        self.runValueIterations(self)

    def runValueIterations(self, state):
        "**Your code here **"
        
        bestVal=0
        
        for i in range(self.iterations):
            newValues = self.values.copy() #temporary list to store the state values
            
            for mdpstate in self.mdp.getStates():  #to go to all states
                if not self.mdp.isTerminal(mdpstate): #if not terminal state
                    qvalList=[]                      #creating a list to store q values
                    # get value for best possible action
                    actions=self.mdp.getPossibleActions(mdpstate)
                    for action in actions:
                        qvalList.append(self.getQValue(mdpstate,action))   #stores all the q values corresponding to each action
                    bestVal=max(qvalList)         #computes max q value from said list
                    newValues[mdpstate]=bestVal

            self.values = newValues
            
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        qValue = 0

        # for every possible instance of outcome
        for nextState, probability in self.mdp.getTransitionStatesAndProbs(state, action):

            # adding future reward * probability of the outcome to reward 
            reward = self.mdp.getReward(state, action, nextState)
            qValue += probability * (reward + self.discount * self.values[nextState])

        return qValue


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """

        # to get the best possible action for a state
        policies = util.Counter()
        for action in self.mdp.getPossibleActions(state):

            # to find how good a particular action will be
            policies[action] = self.getQValue(state, action)

        # to return the best action
        return policies.argMax()


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)