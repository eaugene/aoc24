from collections import defaultdict
from utils import timeit

FILE = "inp.txt"

def read():
    grid = []
    with open(FILE, 'r') as file:
        for line in file:
            grid.append(list(line.strip()))
    n = len(grid)
    m = len(grid[0])
    sx ,sy , ex, ey = -1,-1,-1,-1
    for i in range(n):
        for j in range(m):
            if grid[i][j]=='S':
                sx,sy = i,j
            if grid[i][j]=='E':
                ex,ey = i,j

    return grid,n,m,sx,sy,ex,ey

@timeit
def solve1(grid,n,m,sx,sy,ex,ey):
    # the path from S to E is one

    dir = [(0,1),(1,0),(0,-1),(-1,0)]

    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m

    def putValInGrid():
        pathGrid = [[-1 for i in range(m)] for j in range(n)]
        x , y = sx,sy
        pathGrid[sx][sy] = 0
        while (x,y) != (ex,ey):
            for d in dir:
                dx,dy = d[0] + x , d[1] + y
                if isLimit(dx,dy) and grid[dx][dy] != '#' and pathGrid[dx][dy] == -1:
                    pathGrid[dx][dy] = pathGrid[x][y] + 1
                    x,y = dx,dy
                    break
        return pathGrid

    pathGrid = putValInGrid()
    saveHol = defaultdict(int)
    for i in range(1,n-1):
        for j in range(1,m-1):
            if grid[i][j] == '#' :
                pos = [pathGrid[i+dx][j+dy] for dx,dy in dir if isLimit(i+dx,j+dy) and grid[i+dx][j+dy] != '#']
                pos = sorted(pos)
                for k1 in range(0,len(pos)):
                    for k2 in range(k1+1,len(pos)):
                        saveHol[pos[k2]-pos[k1]-2] += 1
    limit = 100
    if FILE == 'example.txt':
        limit = 0
    ans = 0
    for k,v in saveHol.items():
        if k>=limit:
            ans += v
    return ans

@timeit
def solve2Brute(grid,n,m,sx,sy,ex,ey):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def isLimit(x, y):
        return 0 <= x < n and 0 <= y < m

    def putValInGrid():

        x, y = sx, sy
        lst = [(x, y)]
        vis = set()
        vis.add((x, y))
        while (x, y) != (ex, ey):
            for d in dir:
                dx, dy = d[0] + x, d[1] + y
                if isLimit(dx, dy) and grid[dx][dy] != '#' and (dx, dy) not in vis:
                    x, y = dx, dy
                    lst.append((x, y))
                    vis.add((x, y))
                    break
        return lst

    path = putValInGrid()
    limit = 100
    if FILE == 'example.txt':
        limit = 50
    saveHol = defaultdict(int)
    for i in range(len(path)-1,-1,-1):
        for j in range(i-2-limit,-1,-1):
            ds = abs(path[i][0]-path[j][0]) + abs(path[i][1]-path[j][1])
            if ds <= 20:
                saveHol[i-j-ds] += 1
    ans = 0
    for k,v in saveHol.items():
        if k>=limit:
            ans += v
    return ans


@timeit
def solve2Optimised(grid,n,m,sx,sy,ex,ey):
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def isLimit(x, y):
        return 0 <= x < n and 0 <= y < m

    def putValInGrid():

        x, y = sx, sy
        posInPath = dict()
        posInPath[(x,y)] = 0
        pos = 1
        vis = set()
        vis.add((x, y))
        while (x, y) != (ex, ey):
            for d in dir:
                dx, dy = d[0] + x, d[1] + y
                if isLimit(dx, dy) and grid[dx][dy] != '#' and (dx, dy) not in vis:
                    x, y = dx, dy
                    posInPath[(x, y)]=pos
                    pos+=1
                    vis.add((x, y))
                    break
        return posInPath

    posInPath = putValInGrid()
    limit = 100
    if FILE == 'example.txt':
        limit = 50
    saveHol = defaultdict(int)

    def bfs(x1,y1,vis):
        queue = []
        queue.append((x1,y1))
        vis.add((x1,y1))
        step = 1
        while len(queue) > 0 and step <= 20:
            for _ in range(len(queue)):
                x,y = queue.pop(0)
                for dx,dy in dir:
                    nx,ny = x+dx,y+dy
                    if isLimit(nx,ny)  and (nx,ny) not in vis:
                        vis.add((nx,ny))
                        queue.append((nx,ny))
                        if grid[nx][ny] != '#' and posInPath[(nx, ny)] - posInPath[(x1, y1)] >= limit+2 :
                            saveHol[posInPath[(nx, ny)] - posInPath[(x1, y1)] - step] += 1

            step += 1

    for k,v in posInPath.items():
        vis = set()
        bfs(k[0],k[1],vis)


    ans = 0
    for k,v in saveHol.items():
        if k>=limit:
            ans += v
    return ans


@timeit
def solve2Optimised2(grid,n,m,sx,sy,ex,ey):
    ans = 0
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def isLimit(x, y):
        return 0 <= x < n and 0 <= y < m

    def putValInGrid():
        pathGrid2 = [[-1 for i in range(m)] for j in range(n)]
        x, y = sx, sy
        lst = [(x, y)]
        vis = set()
        vis.add((x, y))
        pathGrid2[sx][sy] = 0
        while (x, y) != (ex, ey):
            for d in dir:
                dx, dy = d[0] + x, d[1] + y
                if isLimit(dx, dy) and grid[dx][dy] != '#' and (dx, dy) not in vis:
                    x, y = dx, dy
                    lst.append((x, y))
                    pathGrid2[x][y] = len(lst) - 1
                    vis.add((x, y))
                    break
        return lst,pathGrid2

    def bfs(x1,y1):
        queue = [(x1, y1)]
        vis = set()
        vis.add((x1,y1))
        step = 1
        paths = set()
        paths.add((x1,y1))
        while len(queue) > 0 and step <= 20:
            for _ in range(len(queue)):
                x,y = queue.pop(0)
                for dx,dy in dir:
                    nx,ny = x+dx,y+dy
                    if isLimit(nx,ny)  and (nx,ny) not in vis:
                        vis.add((nx,ny))
                        queue.append((nx,ny))
                        if grid[nx][ny] != '#':
                            paths.add((nx,ny))
            step += 1
        return paths

    def movePaths(x1,y1,paths,pathGrid2):
        nonlocal ans
        pathsCopy = set()

        # filter out the paths not needed from prev
        for x,y in paths:
            if abs(x1-x) + abs(y1-y) <= 20 and pathGrid2[x][y] > pathGrid2[x1][y1] and pathGrid2[x][y] - pathGrid2[x1][y1] - (abs(x1-x) + abs(y1-y)) >= limit:
                pathsCopy.add((x,y))

        #check only the paths falling on the circumfrence
        # this you can optimise more by instead of checking the 4 possible paths , only do for the direction on the movement of the path
        for i in range(20,-1,-1):
            x2up = x1-i
            x2down = x1+i
            rem = 20-i
            left = y1-rem
            right = y1+rem
            if isLimit(x2up,left) and grid[x2up][left] != '#' and pathGrid2[x2up][left] > pathGrid2[x1][y1] and pathGrid2[x2up][left] - pathGrid2[x1][y1] - (abs(x1-x2up) + abs(y1-left)) >= limit:
                pathsCopy.add((x2up,left))
            if isLimit(x2up,right) and grid[x2up][right] != '#' and pathGrid2[x2up][right] > pathGrid2[x1][y1] and pathGrid2[x2up][right] - pathGrid2[x1][y1] - (abs(x1-x2up) + abs(y1-right)) >= limit:
                pathsCopy.add((x2up,right))
            if isLimit(x2down,left) and grid[x2down][left] != '#' and pathGrid2[x2down][left] > pathGrid2[x1][y1] and pathGrid2[x2down][left] - pathGrid2[x1][y1] - (abs(x1-x2down) + abs(y1-left)) >= limit:
                pathsCopy.add((x2down,left))
            if isLimit(x2down,right) and grid[x2down][right] != '#' and pathGrid2[x2down][right] > pathGrid2[x1][y1] and pathGrid2[x2down][right] - pathGrid2[x1][y1] - (abs(x1-x2down) + abs(y1-right)) >= limit:
                pathsCopy.add((x2down,right))


        ans += len(pathsCopy)

        return pathsCopy


    path,pathGrid = putValInGrid()
    limit = 100
    if FILE == 'example.txt':
        limit = 50
    pathsInRange = bfs(sx,sy)
    for X,Y in path:
        pathsInRange = movePaths(X,Y,pathsInRange,pathGrid)

    return ans

grid,n,m,sx,sy,ex,ey = read()
print(solve1(grid,n,m,sx,sy,ex,ey))
print(solve2Brute(grid,n,m,sx,sy,ex,ey)) # O(path^2) -> path can be n*m in worst case , so O((n*m)^2)
print(solve2Optimised(grid,n,m,sx,sy,ex,ey)) # O(( (40*40) * n*m ) -> O(n*m)
print(solve2Optimised2(grid,n,m,sx,sy,ex,ey)) # more optimal than solve2Optimised - effective moving  on the circumfrence of the path

"""
Function 'solve1' executed in 0.0225 seconds
1355
Function 'solve2Brute' executed in 6.3454 seconds
1007335
Function 'solve2Optimised' executed in 6.2547 seconds
1007335
Function 'solve2Optimised2' executed in 0.4638 seconds
1007335
"""
