# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
import mypy

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
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

  def evaluationFunction(self, currentGameState, action):
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

    "*** YOUR CODE HERE ***"

    newGhostPos = successorGameState.getGhostPositions()
    x, y = newPos
    for GPos in newGhostPos:
        if GPos in [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            return -1000000

    # if action == 'Stop':
    #     return -1000000

    FoodGrid = currentGameState.getFood()
    foods = FoodGrid.asList()
    if newPos in foods:
        return 1000

    # foodsDis = [mypy.distance(newPos, food) for food in foods]
    # ghostDis = [mypy.distance(newPos, ghost) for ghost in newGhostPos]
    # return 10. / newFood.count() + 10. / (min(foodsDis) + 1) - 10 / (min(ghostDis) + 1)

    foodsDis = mypy.findClosestFoodDistance(newPos, currentGameState)
    ghostDis = mypy.findClosestGhostDistance(newPos, currentGameState)
    return 10./newFood.count() + 10./(foodsDis+1) - 10/(ghostDis+1)



def scoreEvaluationFunction(currentGameState):
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

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"

    ghostNum = gameState.getNumAgents() - 1
    # initialValue = {1: 9, 2: 8, 3: 7, 4: -492}

    def maxValue(curState, layer):
        #value = initialValue[layer]
        value = -1000000
        legalActions = curState.getLegalActions(0)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)

        successorStates = [curState.generateSuccessor(0, action) for action in legalActions]
        for successorState in successorStates:
            # if successorState.getPacmanPosition() in successorState.getGhostPositions():
            #     return -9999999
            value = max(value, minValue(successorState, layer, 1))

        return value

    def minValue(curState, layer, ghostIndex):
        #value = initialValue[layer]
        value = 1000000
        legalActions = curState.getLegalActions(ghostIndex)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
            # return -9999999
            return self.evaluationFunction(curState)

        successorStates = [curState.generateSuccessor(ghostIndex, action) for action in legalActions]
        for successorState in successorStates:
            # if successorState.getPacmanPosition() in successorState.getGhostPositions():
            if successorState.isLose():
                # return -9999999
                # value = -9999999
                value = min(value, self.evaluationFunction(successorState))
                continue
            if ghostIndex == ghostNum:
                if layer == self.depth:
                    #for successorState in successorStates:
                    value = min(value, self.evaluationFunction(successorState))
                else:
                    #for successorState in successorStates:
                    value = min(value, maxValue(successorState, layer+1))
            else:
                #for successorState in successorStates:
                value = min(value, minValue(successorState, layer, ghostIndex+1))

        return value

    legalMoves = gameState.getLegalActions(0)
    if len(legalMoves) > 1 and Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    succStates = [gameState.generateSuccessor(0, legalMove) for legalMove in legalMoves]
    values = []
    for succState in succStates:
        # if not succState.getPacmanPosition() in succState.getGhostPositions():
        if not succState.isLose():
            values.append(minValue(succState, 1, 1))
        else:
            values.append(self.evaluationFunction(succState))
    if len(values) == 0:
        return Directions.STOP

    #values = [minValue(succState, 1, 1) for succState in succStates]
    maxValue = max(values)
    bestMoves = [i for i in range(len(values)) if values[i] == maxValue]
    chosenMoveIndex = random.choice(bestMoves)

    return legalMoves[chosenMoveIndex]

    util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    ghostNum = gameState.getNumAgents() - 1

    def maxValue(curState, alpha, beta, layer):
        value = -100000000
        a = alpha
        b = beta
        legalActions = curState.getLegalActions(0)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)

        successorStates = [curState.generateSuccessor(0, action) for action in legalActions]
        for successorState in successorStates:
            value = max(value, minValue(successorState, a, b, layer, 1))
            a = max(a, value)
            if a >= b:
                return value

        return value

    def minValue(curState, alpha, beta, layer, ghostIndex):
        value = 100000000
        a = alpha
        b = beta
        legalActions = curState.getLegalActions(ghostIndex)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
            # return -9999999
            return self.evaluationFunction(curState)

        successorStates = [curState.generateSuccessor(ghostIndex, action) for action in legalActions]
        for successorState in successorStates:
            if successorState.isLose():
                # value = -9999999
                value = min(value, self.evaluationFunction(successorState))
                continue
            if ghostIndex == ghostNum:
                if layer == self.depth:
                    value = min(value, self.evaluationFunction(successorState))
                else:
                    value = min(value, maxValue(successorState, a, b, layer + 1))
                    b = min(b, value)
                    if a >= b:
                        return value
            else:
                value = min(value, minValue(successorState, a, b, layer, ghostIndex + 1))

        return value

    legalMoves = gameState.getLegalActions(0)
    if len(legalMoves) > 1 and Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    succStates = [gameState.generateSuccessor(0, legalMove) for legalMove in legalMoves]
    values = []
    for succState in succStates:
        if not succState.isLose():
            values.append(minValue(succState, -100000000, 100000000, 1, 1))
        else:
            values.append(self.evaluationFunction(succState))
    if len(values) == 0:
        return Directions.STOP

    maxValue = max(values)
    bestMoves = [i for i in range(len(values)) if values[i] == maxValue]
    chosenMoveIndex = random.choice(bestMoves)

    return legalMoves[chosenMoveIndex]

    util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"

    ghostNum = gameState.getNumAgents() - 1

    def maxValue(curState, layer):
        value = -1000000
        legalActions = curState.getLegalActions(0)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)

        successorStates = [curState.generateSuccessor(0, action) for action in legalActions]
        for successorState in successorStates:
            value = max(value, expValue(successorState, layer, 1))

        return value

    def expValue(curState, layer, ghostIndex):
        value = 0
        legalActions = curState.getLegalActions(ghostIndex)
        if len(legalActions) > 1 and Directions.STOP in legalActions:
            legalActions.remove(Directions.STOP)
        if len(legalActions) == 0:
             return self.evaluationFunction(curState)

        probability = 1./len(legalActions)
        successorStates = [curState.generateSuccessor(ghostIndex, action) for action in legalActions]
        for successorState in successorStates:
            if successorState.isLose():
                # value = -9999999
                value += probability * self.evaluationFunction(successorState)
                continue
            if ghostIndex == ghostNum:
                if layer == self.depth:
                    value += probability * self.evaluationFunction(successorState)
                else:
                    value += probability * maxValue(successorState, layer + 1)
            else:
                value += probability * expValue(successorState, layer, ghostIndex + 1)

        return value

    legalMoves = gameState.getLegalActions(0)
    if len(legalMoves) > 1 and Directions.STOP in legalMoves:
        legalMoves.remove(Directions.STOP)
    succStates = [gameState.generateSuccessor(0, legalMove) for legalMove in legalMoves]
    values = []
    for succState in succStates:
        if not succState.isLose():
            values.append(expValue(succState, 1, 1))
        else:
            values.append(self.evaluationFunction(succState))
    if len(values) == 0:
        return Directions.STOP

    maxValue = max(values)
    bestMoves = [i for i in range(len(values)) if values[i] == maxValue]
    chosenMoveIndex = random.choice(bestMoves)

    return legalMoves[chosenMoveIndex]

    util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin():
        return 1000000

    GhostPos = currentGameState.getGhostPositions()
    Pos = currentGameState.getPacmanPosition()
    x, y = Pos
    for GPos in GhostPos:
      if GPos in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
          return -1000000

    FoodGrid = currentGameState.getFood()
    foods = FoodGrid.asList()
    if Pos in foods:
      return 1000

    foodsDis = mypy.findClosestFoodDistance(Pos, currentGameState)
    ghostDis = mypy.findClosestGhostDistance(Pos, currentGameState)
    return currentGameState.getScore() * 1000 + 100. / (foodsDis + 1) - 10 / (ghostDis + 1)

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

