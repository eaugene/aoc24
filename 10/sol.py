from utils import timeit

file  = 'inp.txt'
def read():
    grid = []
    with open(file) as f:
        for line in f:
            grid.append([int(x) for x in list(line.strip())])
    return grid


@timeit
def solve1and2(grid):
    dir = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    n = len(grid)
    m = len(grid[0])
    vis = [[-1 for _ in range(m)] for _ in range(n)]
    visSet = [[set() for _ in range(m)] for _ in range(n)]

    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m


    def dfs(x,y):
        if vis[x][y] >= 0:
            return vis[x][y],visSet[x][y]
        if(grid[x][y]==9):
            vis[x][y] = 1
            visSet[x][y] =  set([(x, y)])
            return vis[x][y], visSet[x][y]

        ans = 0
        ansSet = set()
        for d in dir:
            nx, ny = x + d[0], y + d[1]
            if isLimit(nx, ny) and grid[nx][ny] == grid[x][y] + 1:
                val,valSet = dfs(nx, ny)
                ans += val
                ansSet = ansSet.union(valSet)
        vis[x][y] = ans
        visSet[x][y] = ansSet
        return vis[x][y], visSet[x][y]

    ans1 = 0
    ans2 = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 0:
                val, valset = dfs(i, j)
                ans1 += len(valset)
                ans2 += val
    return ans1,ans2

grid = read()
ans1,ans2 = solve1and2(grid)
print(ans1)
print(ans2)
