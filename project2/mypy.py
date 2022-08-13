import util
import pacman

# Calculate Manhattan distance of two positions
def distance(start, target):
    x1, y1 = start
    x2, y2 = target
    return abs(x1 - x2) + abs(y1 - y2)


def findClosestFoodDistance(start, Gamestate):
    foodGrid = Gamestate.getFood()
    foods = foodGrid.asList()
    walls = Gamestate.getWalls()

    queue = util.Queue()
    visited = set()
    queue.push((start, 0))

    while not queue.isEmpty():
        cur = queue.pop()
        curPos = cur[0]
        curCost = cur[1]
        if curPos not in visited:
            if curPos in foods:
                return curCost
            visited.add(curPos)
            x, y = curPos
            for nextx, nexty in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if not walls[nextx][nexty]:
                    nextPost = nextx, nexty
                    queue.push((nextPost, curCost+1))

    return 0

def findClosestGhostDistance(start, Gamestate):
    ghostPos = Gamestate.getGhostPositions()
    walls = Gamestate.getWalls()

    queue = util.Queue()
    visited = set()
    queue.push((start, 0))

    while not queue.isEmpty():
        cur = queue.pop()
        curPos = cur[0]
        curCost = cur[1]
        if curPos not in visited:
            if curPos in ghostPos:
                return curCost
            visited.add(curPos)
            x, y = curPos
            for nextx, nexty in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                if not walls[nextx][nexty]:
                    nextPost = nextx, nexty
                    queue.push((nextPost, curCost+1))

    return 0
