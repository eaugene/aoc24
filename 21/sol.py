from functools import cache

from utils import timeit
from itertools import permutations,product

FILE = 'inp.txt'

def read():
    inp = []
    with open(FILE, 'r') as file:
        for line in file:
            inp.append(line.strip())
    return inp

revDir = {
    '^' : [-1,0],
    'v' : [1,0],
    '<' : [0,-1],
    '>' : [0,1]
}

dir = [(-1,0),(1,0),(0,-1),(0,1)] # up,down,left,right


def preProcessNumericPad():
    """
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    :return: path[st][en] should give list of size 4 [ up,down,left,right ] steps needed
    """

    grid = [['7','8','9'],['4','5','6'],['1','2','3'],['#','0','A']]
    reverseGrid = {val: (i,j) for i in range(len(grid)) for j,val in enumerate(grid[i])}
    n = len(grid)
    m = len(grid[0])

    valsToProcess = ['1','2','3','4','5','6','7','8','9','A','0']
    path ={val: {val2: [] for val2 in valsToProcess} for val in valsToProcess}

    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m

    def IsValidPath(st,path):

        x, y = reverseGrid[st]
        for i in path:
            if i=='A':
                break
            if grid[x][y] == '#':
                return False
            x += revDir[i][0]
            y += revDir[i][1]
        return True


    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue
            st = grid[i][j]
            queue = []
            vis=set()
            queue.append((i,j,[0,0,0,0]))
            vis.add((i,j))
            while len(queue) > 0:
                x,y,dis = queue.pop(0)
                path[st][grid[x][y]] = [ p for p in  getAllPaths(dis) if IsValidPath(st,p)]
                for d in range(len(dir)):
                    dx,dy = x+dir[d][0],y+dir[d][1]
                    if isLimit(dx,dy) and grid[dx][dy] != '#' and (dx,dy) not in vis:
                        disCopy = dis.copy()
                        disCopy[d] += 1
                        queue.append((dx,dy,disCopy))
                        vis.add((dx,dy))
    return path

def preProcessDirectionPad():
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    :return: path[st][en] should give list of size 4 [ up,down,left,right ] steps needed
    """

    grid = [['#','^','A'],['<','v','>']]
    reverseGrid = {val: (i, j) for i in range(len(grid)) for j, val in enumerate(grid[i])}
    n = len(grid)
    m = len(grid[0])

    valsToProcess = ['^','v','<','>','A']
    path ={val: {val2: [] for val2 in valsToProcess} for val in valsToProcess}

    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m

    def IsValidPath(st,path):
        x, y = reverseGrid[st]
        for i in path:
            if i=='A':
                break
            if grid[x][y] == '#':
                return False
            x += revDir[i][0]
            y += revDir[i][1]
        return True

    for i in range(n):
        for j in range(m):
            if grid[i][j] == '#':
                continue
            st = grid[i][j]
            queue = []
            vis=set()
            queue.append((i,j,[0,0,0,0]))
            vis.add((i,j))
            while len(queue) > 0:
                x,y,dis = queue.pop(0)
                path[st][grid[x][y]] = [ p for p in  getAllPaths(dis) if IsValidPath(st,p)]
                for d in range(len(dir)):
                    dx,dy = x+dir[d][0],y+dir[d][1]
                    if isLimit(dx,dy) and grid[dx][dy] != '#' and (dx,dy) not in vis:
                        disCopy = dis.copy()
                        disCopy[d] += 1
                        queue.append((dx,dy,disCopy))
                        vis.add((dx,dy))
    return path


def unique_string_permutations(s):
    # Generate all permutations of the string
    perms = permutations(s)
    # Use a set to eliminate duplicate permutations
    unique_perms = set(''.join(p) for p in perms)
    # Convert the set back to a sorted list (optional)
    return sorted(unique_perms)

def getPath(arr):
    assert len(arr)==4
    hol = ""
    for i in range(arr[0]):
        hol += '^'
    for i in range(arr[1]):
        hol += 'v'
    for i in range(arr[2]):
        hol += '<'
    for i in range(arr[3]):
        hol += '>'
    return hol


def getAllPaths(arr):
    prePermutePath = getPath(arr)
    permutePath = unique_string_permutations(prePermutePath)
    permutePath = [x+'A' for x in permutePath]
    return permutePath

@cache
def solveNumericPad(inp):
    n = len(inp)
    ans = ['']
    inp = 'A' + inp
    for i in range(1,n+1):
        allPaths = numPath[inp[i-1]][inp[i]]
        ans = [x + y for x, y in product(ans, allPaths)]
    return ans

@cache
def solveDirectionPad(inp):
    n = len(inp)
    ans = ['']
    inp = 'A' + inp
    for i in range(1, n+1):
        allPaths = dirPath[inp[i - 1]][inp[i]]
        ans = [x + y for x, y in product(ans, allPaths)]
    return ans

@timeit
def solveBrute(inp):


    def solveUtil(val):
        level1 = solveNumericPad(val)
        level2 = set()
        for i in level1:
            level2.update(solveDirectionPad(i))
        level3 = set()
        for i in level2:
            level3.update(solveDirectionPad(i))

        mn = 99999999999999999999999
        for i in level3:
            mn = min(mn,len(i))

        return mn


    ans = 0

    for I in inp:
        intVal = int(I[:-1])
        ans += (intVal * solveUtil(I))
    return ans


@cache
def solveDirectionPadMemo(fr,to,level):
    if level > ROBOT_LEVEL:
        return len(dirPath[fr][to][0])

    mn = 99999999999999999999999
    for posPaths in dirPath[fr][to]:
        pathCopy = 'A' + posPaths
        sz = len(pathCopy)
        lVal = 0
        for i in range(1,sz):
            lVal += solveDirectionPadMemo(pathCopy[i-1],pathCopy[i],level+1)
        mn = min(mn,lVal)
    return mn


@timeit
def solveOptimised(inp):


    def solveUtil(val):
        level1 = solveNumericPad(val)

        mn = 99999999999999999999999
        for i in level1:
            ic = 'A' + i
            sz = len(ic)
            lval = 0
            for j in range(1,sz):
                lval += solveDirectionPadMemo(ic[j-1],ic[j],1)
            mn = min(mn,lval)

        return mn


    ans = 0

    for I in inp:
        intVal = int(I[:-1])
        ans += (intVal * solveUtil(I))
    return ans

numPath = preProcessNumericPad()
dirPath = preProcessDirectionPad()

inp = read()
print(solveBrute(inp))


"""
numericPad - Robot 1 

Direction Pad - Robot 2 
Direction Pad - Robot 3

Direction Pad - You 
"""


ROBOT_LEVEL = 2 - 1 # R2 to R1 is already solved as normal way ( line : 235 )  , so we need to solve R3 to R2 and You to R3 . You to R3 is the last so just take the length of any path , as all paths should have same length


print(solveOptimised(inp))

solveDirectionPadMemo.cache_clear()

ROBOT_LEVEL = 25 - 1 # Refer the explanation above on why 25-1

print(solveOptimised(inp))

"""
Function 'solveBrute' executed in 8.2062 seconds
176650
Function 'solveOptimised' executed in 0.0001 seconds
176650
Function 'solveOptimised' executed in 0.0841 seconds
217698355426872
"""