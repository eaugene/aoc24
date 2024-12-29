from utils import timeit
FILE_NAME = 'inp.txt'


def read():
    grid = []
    with open(FILE_NAME, 'r') as file:
        for line in file:
            grid.append([c for c in line.strip()])
    return grid

@timeit
def solve1(grid):
    ans = 0
    n = len(grid)
    m = len(grid[0])
    dir = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m

    def isXmas(x, y,dir):
        return isLimit(x,y) and grid[x][y] == 'X' and isLimit(x+dir[0],y+dir[1]) and grid[x+dir[0]][y+dir[1]] == 'M' and isLimit(x+2*dir[0],y+2*dir[1]) and grid[x+2*dir[0]][y+2*dir[1]] == 'A' and isLimit(x+3*dir[0],y+3*dir[1]) and grid[x+3*dir[0]][y+3*dir[1]] == 'S'

    for i in range(n):
        for j in range(m):
            for d in dir:
                if(isXmas(i,j,d)):
                    ans+=1

    return ans


@timeit
def solve2(grid):
    ans = 0
    n = len(grid)
    m = len(grid[0])

    dir = [[-1,-1],[-1,1],[1,-1],[1,1]]
    """
    0 . 1
    . X .
    2 . 3
    """

    dirJoined = [[0,3],[1,2]]


    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m


    def isXamsUtil(x,y,idx):
        x1 = dir[dirJoined[idx][0]][0]
        y1 = dir[dirJoined[idx][0]][1]
        x2 = dir[dirJoined[idx][1]][0]
        y2 = dir[dirJoined[idx][1]][1]
        return isLimit(x+x1,y+y1) and isLimit(x+x2,y+y2) and ( (grid[x+x1][y+y1] == 'M' and grid[x+x2][y+y2] == 'S') or (grid[x+x1][y+y1] == 'S' and grid[x+x2][y+y2] == 'M') )

    def isXams(x,y):
        return isXamsUtil(x,y,0) and isXamsUtil(x,y,1)

    for i in range(n):
        for j in range(m):
            if grid[i][j]=='A' and isXams(i,j):
                ans+=1

    return ans

grid = read()
print(solve1(grid))
print(solve2(grid))