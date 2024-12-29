from utils import timeit
import re

FILE = "inp.txt"

def read():
    vals = []
    n,m = 7,7
    with open(FILE, 'r') as file:
        for line in file:
            line = line.strip().split(',')
            vals.append((int(line[0]), int(line[1])))
    if FILE == 'inp.txt':
        n,m = 71,71
    return n,m,vals

@timeit
def solve1(n,m,vals,limit):
    grid = [['.' for i in range(m)] for j in range(n)]

    for x,y in vals[:limit]:
        grid[x][y] = '#'

    sx,sy=0,0
    ex,ey=n-1, m-1

    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m

    # bfs
    vis = [[False for i in range(m)] for j in range(n)]
    q = [(sx, sy, 0)]
    vis[sx][sy] = True
    while len(q) > 0:
        x,y,d = q.pop(0)
        if x == ex and y == ey:
            return d
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            nx,ny = x+dx, y+dy
            if isLimit(nx,ny) and not vis[nx][ny] and grid[nx][ny] != '#':
                vis[nx][ny] = True
                q.append((nx,ny,d+1))
    return -1

@timeit
def solve2(n,m,vals):

    # Binary search . Next time try out without binary search , is there any other way possible ? think of strong nodes - weak nodes like
    st = 0
    en = len(vals)-2

    while st <= en:
        md = (st+en)//2
        if solve1(n,m,vals,md+1) == -1:
            en = md-1
        else:
            st = md+1
    return vals[en+1]

n,m,val = read()
print(solve1(n,m,val,1024 if FILE == 'inp.txt' else 12))
print(solve2(n,m,val))

"""
Function 'solve1' executed in 0.0040 seconds
372
Function 'solve2' executed in 0.0121 seconds
(25, 6)
"""