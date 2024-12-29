from utils import timeit
FILE = "inp.txt"
def read():
    grid = []
    with open(FILE) as f:
        for l in f:
            grid.append(list(l.strip()))
    return grid


@timeit
def solve1(grid):
    n = len(grid)
    m = len(grid[0])

    vis = [[False for _ in range(m)] for _ in range(n)]

    dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]

    def isLimit(x, y):
        return x >= 0 and x < n and y >= 0 and y < m

    def dfs(x, y,char):
        vis[x][y] = True
        area = 1
        per = 0
        for d in dir:
            dx = x + d[0]
            dy = y + d[1]
            if isLimit(dx, dy) and  grid[dx][dy] == char:
                if not vis[dx][dy]:
                    a, p = dfs(dx, dy, char)
                    area += a
                    per += p
            else:
                per += 1
        return area , per

    ans = 0

    for i in range(n):
        for j in range(m):
            if not vis[i][j]:
                a, p = dfs(i, j, grid[i][j])
                # print(a, p,i,j)
                ans += ( a*p )
    return ans



@timeit
def solve2Optimised(grid):
    # TC : O((n*m)^2)
    n = len(grid)
    m = len(grid[0])

    vis = [[False for _ in range(m)] for _ in range(n)]

    dir = [[1, 0], [0, 1], [-1, 0], [0, -1]] # down, right, up, left

    def isLimit(x, y):
        return x >= 0 and x < n and y >= 0 and y < m

    def bfs(x, y,char,per):
        vis[x][y] = True
        queue = [(x,y)]
        area = 0
        side = 0
        while len(queue) > 0:
            x,y = queue.pop(0)
            area += 1
            for r in range(len(dir)):
                dx = x + dir[r][0]
                dy = y + dir[r][1]
                if isLimit(dx, dy) and  grid[dx][dy] == char:
                    if not vis[dx][dy]:
                        vis[dx][dy] = True
                        queue.append((dx,dy))
                else:
                    if dx == x :
                        # vertical fence
                        if (dx-1,dy)  in per[r] and (dx+1,dy) in per[r]:
                            # both side independency counted , so remove one - equivalent of joining
                            side -=1
                        elif (dx-1,dy) not in per[r] and (dx+1,dy) not in per[r]:
                            #print(x+1,y+1," ",dx+1,dy+1,r,"vertical",char)
                            side += 1
                        per[r].add((dx,dy))
                    elif dy == y:
                        # horizontal fence
                        if (dx, dy-1)  in per[r] and (dx, dy+1) in per[r]:
                            # both side independency counted , so remove one - equivalent of joining
                            side -=1
                        elif (dx, dy-1) not in per[r] and (dx, dy+1) not in per[r]:
                            #print(x+1,y+1," ",dx+1,dy+1,r,"hori",char)
                            side += 1
                        per[r].add((dx, dy))
        return area , side


    ans = 0

    for i in range(n):
        for j in range(m):
            if not vis[i][j]:
                per = [set() for _ in range(4)]
                a, p = bfs(i, j, grid[i][j],per)
                ans += ( a*p )
    return ans


@timeit
def solve2Brute(grid):
    # TC : O((n*m)^2)
    n = len(grid)
    m = len(grid[0])

    vis = [[False for _ in range(m)] for _ in range(n)]

    dir = [[1, 0], [0, 1], [-1, 0], [0, -1]] # down, right, up, left

    def isLimit(x, y):
        return x >= 0 and x < n and y >= 0 and y < m

    def bfs(X, Y,char,lvis):
        vis[X][Y] = True

        queue = [(X,Y)]
        area = 0
        while len(queue) > 0:
            x,y = queue.pop(0)
            lvis[x][y] = True
            area += 1
            for r in range(len(dir)):
                dx = x + dir[r][0]
                dy = y + dir[r][1]
                if isLimit(dx, dy) and  grid[dx][dy] == char:
                    if not vis[dx][dy]:
                        vis[dx][dy] = True
                        queue.append((dx,dy))
        return area

    def processlvis(lvis):

        ans = 0
        left = 0
        right = 0
        # vertical
        for j in range(m):
            for i in range(n):
                if lvis[i][j]:
                    if not isLimit(i,j-1) or not lvis[i][j-1]:
                        left += 1
                    else:
                        if left > 0:
                            ans += 1
                        left = 0
                    if not isLimit(i, j+1) or not lvis[i][j+1]:
                        right += 1
                    else:
                        if right > 0:
                            ans += 1
                        right = 0
                else:
                    if left > 0:
                        ans += 1
                    left = 0
                    if right > 0:
                        ans += 1
                    right = 0
            if left > 0:
                ans += 1
            left = 0
            if right > 0:
                ans += 1
            right = 0

        top = 0
        bottom = 0
        # horizontal
        for i in range(n):
            for j in range(m):
                if lvis[i][j]:
                    if not isLimit(i-1, j) or not lvis[i-1][j]:
                        top += 1
                    else:
                        if top > 0:
                            ans += 1
                        top = 0
                    if not isLimit(i+1 , j) or not lvis[i+1][j]:
                        bottom += 1
                    else:
                        if bottom > 0:
                            ans += 1
                        bottom = 0
                else:
                    if top > 0:
                        ans += 1
                    top = 0
                    if bottom > 0:
                        ans += 1
                    bottom = 0
            if top > 0:
                ans += 1
            top = 0
            if bottom > 0:
                ans += 1
            bottom = 0

        return  ans



    ans = 0

    for i in range(n):
        for j in range(m):
            if not vis[i][j]:
                lvis = [[False for _ in range(m)] for _ in range(n)]
                a = bfs(i, j, grid[i][j],lvis)
                p = processlvis(lvis)
                ans += ( a*p )
    return ans

grid = read()
print(solve1(grid))
print(solve2Brute(grid))
print(solve2Optimised(grid))

"""
For both side counted edge case in the optimised example, use this input to find 

AAAAAAAAAAAAAAAA
AAAAAABBBBAAAAAA
AAAAABBBBBAAAAAA
AAABBBBBBBBBAAAA
ABBBBBBBBBBBAAAA
AAAABBABBBBBBBAA
AAABBBBBBBBBBAAA
AAAAABBBBBBBAAAA
AAAAAAAAAABBAAAA
AAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAA

The sample inputs were working fine without the edge case solved 
 
"""


"""
Function 'solve1' executed in 0.0182 seconds
1363484
Function 'solve2Brute' executed in 1.3180 seconds
838988
Function 'solve2Optimised' executed in 0.0250 seconds
838988
"""