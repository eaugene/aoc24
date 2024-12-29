from utils import timeit

FILE = "inp.txt"
def read(part=1):
    grid = []
    path = ""
    with open(FILE, 'r') as file:
        isGridDone = False
        for l in file:
            if l.strip() == '':
                isGridDone = True
                continue
            if not isGridDone:
                l = l.strip()
                line = []
                for k in l:
                    line.append(k)
                grid.append(line)
            else:
                l = l.strip()
                path += l
    if part == 2 :
        expGrid = []
        for r in grid:
            expLine = []
            for c in r:
                if c == '#':
                    expLine.append('#')
                    expLine.append('#')
                elif c == 'O':
                    expLine.append('[')
                    expLine.append(']')
                elif c == '@':
                    expLine.append('@')
                    expLine.append('.')
                else:
                    expLine.append('.')
                    expLine.append('.')
            expGrid.append(expLine)
        grid = expGrid
    return grid, path

def printGrid(grid):
    for i in grid:
        for j in i:
            print(j, end=" ")
        print()

@timeit
def solve1(grid, path):
    # This solution follows the plan brute way of moving things . TC : O(P*max(m,n)) the max part is due to movement can be either vertical or horizontal
    n = len(grid)
    m = len(grid[0])

    def findRobot():
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '@':
                    return i, j

    rx,ry = findRobot()

    def getDir(chr):
        if chr == '^':
            return -1, 0
        if chr == 'v':
            return 1, 0
        if chr == '<':
            return 0, -1
        if chr == '>':
            return 0, 1
        assert False

    def isValid(x, y):
        return 0 <= x < n and 0 <= y < m

    def move(x, y, chr):

        delX , delY = getDir(chr)
        dx = x + delX
        dy = y + delY
        x2 = x
        y2 = y
        emptyFound = False
        while isValid(dx, dy) and grid[dx][dy] != '#' and not emptyFound:
            if grid[dx][dy] == '.':
                emptyFound = True
            x2 = dx
            y2 = dy
            dx += delX
            dy += delY
        if x2 == x and y2 == y:
            return x, y
        if not emptyFound:
            return x, y
        hold = '@'
        grid[x][y] = '.'
        if x + delX == x2 and y + delY == y2:
            grid[x2][y2] = '@'
            return x2, y2

        grid[x2][y2] = 'O'
        grid[x+delX][y+delY] = hold
        return x+delX, y+delY

    for p in path:
        rx , ry = move(rx, ry, p)

    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'O':
                ans += ((i)*100) + (j)
    return ans

@timeit
def solve2(grid, path):
    # This solution follows the plan brute way of moving things . TC : O(P*(m*n)) . As in each movement we are potentially doing n*m transformation
    # its not ideally n*m - it would be a shape of triangle - but in asymptotic terms ins n*m.
    n = len(grid)
    m = len(grid[0])

    def findRobot():
        for i in range(n):
            for j in range(m):
                if grid[i][j] == '@':
                    return i, j

    rx,ry = findRobot()

    def getDir(chr):
        if chr == '^':
            return -1, 0
        if chr == 'v':
            return 1, 0
        if chr == '<':
            return 0, -1
        if chr == '>':
            return 0, 1
        assert False

    def isValid(x, y):
        return 0 <= x < n and 0 <= y < m

    def moveHori(x, y, chr):
        delX , delY = getDir(chr)
        dx = x + delX
        dy = y + delY
        x2 = x
        y2 = y
        emptyFound = False
        while isValid(dx, dy) and grid[dx][dy] != '#' and not emptyFound:
            if grid[dx][dy] == '.':
                emptyFound = True
            x2 = dx
            y2 = dy
            dx += delX
            dy += delY
        if x2 == x and y2 == y:
            return x, y
        if not emptyFound:
            return x, y
        hold = '@'
        grid[x][y] = '.'
        if x + delX == x2 and y + delY == y2:
            grid[x2][y2] = '@'
            return x2, y2
        dx = x
        dy = y
        while True:
            dx = dx + delX
            dy = dy + delY
            hold , grid[dx][dy] = grid[dx][dy], hold
            if dx == x2 and dy == y2:
                break

        return x+delX, y+delY

    def recMove(x,y,delX,delY,movedAlready):
        if (x,y) in movedAlready:
            return
        movedAlready.add((x, y))
        if grid[x+delX][y+delY] == '.':
            grid[x + delX][y + delY] = grid[x][y]
            grid[x][y]='.'
        elif grid[x+delX][y+delY] == '[':
            recMove(x+delX, y+delY, delX, delY,movedAlready)
            recMove(x + delX, y + delY+1, delX, delY,movedAlready)
            grid[x + delX][y + delY] = grid[x][y]
            grid[x][y] = '.'
        elif grid[x+delX][y+delY] == ']':
            recMove(x + delX, y + delY, delX, delY, movedAlready)
            recMove(x + delX, y + delY - 1, delX, delY, movedAlready)
            grid[x + delX][y + delY] = grid[x][y]
            grid[x][y] = '.'


    def moveVert(x, y, chr):
        delX , delY = getDir(chr)
        elementsToMove = set()
        elementsToMove.add((x,y))
        while len(elementsToMove) > 0 :
            sz = len(elementsToMove)
            nextElementsToMove = set()
            while sz > 0:
                sz -= 1
                x2, y2 = elementsToMove.pop()
                dx = x2 + delX
                dy = y2 + delY
                if not isValid(dx,dy) or grid[dx][dy] == '#':
                    return x,y
                if grid[dx][dy] == '[':
                    nextElementsToMove.add((dx,dy))
                    nextElementsToMove.add((dx, dy+1))
                elif grid[dx][dy] == ']':
                    nextElementsToMove.add((dx,dy))
                    nextElementsToMove.add((dx, dy-1))
            elementsToMove = nextElementsToMove

        # the recMove does not do any validation - it assumes that the move is valid
        # validity is checked in the previous level order traversal
        recMove(x, y, delX, delY, set())
        return x+delX, y+delY

    def move(x, y, chr):
        if chr == '^' or chr == 'v':
            return moveVert(x,y,chr)
        else:
            return moveHori(x, y, chr)

    for p in path:
        rx , ry = move(rx, ry, p)

    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '[':
                ans += ((i)*100) + (j)
    return ans


grid , path = read()
print(solve1(grid, path))
grid , path = read(2)
print(solve2(grid, path))

"""
Function 'solve1' executed in 0.0147 seconds
1509863
Function 'solve2' executed in 0.0242 seconds
1548815
"""