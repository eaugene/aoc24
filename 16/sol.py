from utils import timeit
import heapq
FILE = "inp.txt"
inf = 9999999999999999

def read():
    grid = []
    with open(FILE, 'r') as file:
        for l in file:
            l = l.strip()
            line = []
            for k in l:
                line.append(k)
            grid.append(line)

    n = len(grid)
    m = len(grid[0])

    st = ()
    en = ()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                st = (i, j)
            if grid[i][j] == 'E':
                en = (i, j)

    return st,en,grid

@timeit
def solve1(st,en,grid):
    """
    Time Complexity
    Edges ( E ) : O(4*n*m) = O(n*m)
    Vertices ( V ) : O(4 * n*m) = O(n*m)
    Dijkstra : O(E *log(V) ) = O(n*m*log(n*m))
    """
    n = len(grid)
    m = len(grid[0])

    def isLimit(x,y):
        return x>=0 and y>=0 and x<n and y<m

    dirs = [(0,1),(1,0),(0,-1),(-1,0)]

    ansGrid = [[inf for i in range(m)] for j in range(n)]

    def dijkstraw(x,y,dir):
        nonlocal ansGrid
        pq = []
        ansGrid[x][y] = 0
        heapq.heappush(pq,(0,(x,y,dir)))
        while len(pq)>0:
            dist, (x,y,dir) = heapq.heappop(pq)
            if (x,y) == en:
                continue

            #same dir
            nx,ny = x+dirs[dir][0], y+dirs[dir][1]
            if isLimit(nx,ny) and grid[nx][ny] != '#' :
                if ansGrid[nx][ny] > dist + 1:
                    ansGrid[nx][ny] = dist + 1
                    heapq.heappush(pq,(ansGrid[nx][ny],(nx,ny,dir)))

            # clock wise 90
            nx,ny = x+dirs[(dir+1)%4][0], y+dirs[(dir+1)%4][1]
            if isLimit(nx,ny) and grid[nx][ny] != '#' :
                if ansGrid[nx][ny] > dist+1001:
                    ansGrid[nx][ny] = dist+1001
                    heapq.heappush(pq,(ansGrid[nx][ny],(nx,ny,(dir+1)%4)))

            # anti clock wise 90
            nx, ny = x + dirs[(dir + 3) % 4][0], y + dirs[(dir + 3) % 4][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                if ansGrid[nx][ny] > dist + 1001:
                    ansGrid[nx][ny] = dist + 1001
                    heapq.heappush(pq, (ansGrid[nx][ny], (nx, ny, (dir + 3) % 4)))

            #  clock wise 180
            nx, ny = x + dirs[(dir + 2) % 4][0], y + dirs[(dir + 2) % 4][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                if ansGrid[nx][ny] > dist + 2001:
                    ansGrid[nx][ny] = dist + 2001
                    heapq.heappush(pq, (ansGrid[nx][ny], (nx, ny, (dir + 2) % 4)))

    dijkstraw(st[0],st[1],0)
    assert ansGrid[en[0]][en[1]] != inf
    # for i in ansGrid:
    #     for j in i:
    #         if j == inf:
    #             print('inf ',end=" ")
    #         else:
    #             print(" "*(4-len(str(j)))+str(j),end=" ")
    #     print('')
    return ansGrid[en[0]][en[1]],ansGrid

@timeit
def solve2(st,en,ans,grid):
    """
        Time Complexity
        Edges ( E ) : O(4*n*m) = O(n*m)
        Vertices ( V ) : O(4 * n*m) = O(n*m)
        Dijkstra : O(E *log(V) ) = O(n*m*log(n*m))

    Here we make 5X operations than problem 1 , so the factor of increase in runtime


    """

    n = len(grid)
    m = len(grid[0])

    def isLimit(x, y):
        return x >= 0 and y >= 0 and x < n and y < m

    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


    def dijkstraw(x, y,lansGrid,end,extraMod=0):
        """
        extraMod acts as a modifier to the direction storage by 180 ( if extraMod == 2 ) . used in the reverse dijkstraw ( EndToFrom )

        """
        pq = []
        for i in range(4):
            heapq.heappush(pq, (lansGrid[x][y][i], (x, y, i)))
        while len(pq) > 0:
            dist, (x, y, dir) = heapq.heappop(pq)
            if (x, y) == end:
                continue

            # same dir
            nx, ny = x + dirs[dir][0], y + dirs[dir][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                lval = dist+1
                if lansGrid[nx][ny][(dir+extraMod)%4] > lval:
                    lansGrid[nx][ny][(dir+extraMod)%4] = lval
                    heapq.heappush(pq, (lval, (nx, ny, dir)))

            # clock wise 90
            nx, ny = x + dirs[(dir + 1) % 4][0], y + dirs[(dir + 1) % 4][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                lval = dist + 1001
                if lansGrid[nx][ny][(dir + 1+extraMod) % 4] > lval:
                    lansGrid[nx][ny][(dir + 1+extraMod) % 4] = lval
                    heapq.heappush(pq, (lval, (nx, ny, (dir + 1) % 4)))

            # anti clock wise 90
            nx, ny = x + dirs[(dir + 3) % 4][0], y + dirs[(dir + 3) % 4][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                lval = dist + 1001
                if lansGrid[nx][ny][(dir + 3+extraMod) % 4] > lval:
                    lansGrid[nx][ny][(dir + 3+extraMod) % 4] = lval
                    heapq.heappush(pq, (lval, (nx, ny, (dir + 3) % 4)))

            #  clock wise 180
            nx, ny = x + dirs[(dir + 2) % 4][0], y + dirs[(dir + 2) % 4][1]
            if isLimit(nx, ny) and grid[nx][ny] != '#' :
                lval = dist + 2001
                if lansGrid[nx][ny][(dir+2+extraMod)%4] > lval:
                    lansGrid[nx][ny][(dir+2+extraMod)%4] = lval
                    heapq.heappush(pq, (lval, (nx, ny, (dir + 2) % 4)))


    fromToEnd = [[[inf for k in range(4)] for i in range(m)] for j in range(n)]
    fromToEnd[st[0]][st[1]][0] = 0
    fromToEnd[st[0]][st[1]][1] = 1000
    fromToEnd[st[0]][st[1]][2] = 2000
    fromToEnd[st[0]][st[1]][3] = 1000
    dijkstraw(st[0], st[1],fromToEnd,en, 0)
    EndToFrom = [[[inf for k in range(4)] for i in range(m)] for j in range(n)]
    EndToFrom[en[0]][en[1]][0] = 0
    EndToFrom[en[0]][en[1]][1] = 0
    EndToFrom[en[0]][en[1]][2] = 0
    EndToFrom[en[0]][en[1]][3] = 0
    dijkstraw(en[0], en[1], EndToFrom, st, 2)

    pathAns = 0


    for i in range(n):
        for j in range(m):
            ok = False
            # print(
            #     [" "*(4-len(str(D)))+str(D) if D != inf else 'inf ' for D in fromToEnd[i][j]],
            #     [" "*(4-len(str(D)))+str(D) if D != inf else 'inf ' for D in EndToFrom[i][j]],
            #     end="   "
            # )
            for k in range(4):
                if fromToEnd[i][j][k] + EndToFrom[i][j][k] <= ans or fromToEnd[i][j][k] + EndToFrom[i][j][(k+1)%4] + 1000 <= ans or fromToEnd[i][j][k] + EndToFrom[i][j][(k+3)%4] + 1000 <= ans or fromToEnd[i][j][k] + EndToFrom[i][j][(k+2)%4] + 2000 <= ans:
                    ok = True
            if ok:
                grid[i][j] = 'O'
                pathAns += 1
        # print('',end="\n")

    # for i in grid:
    #     for j in i:
    #         print(j,end="")
    #     print('')
    return pathAns


st, en , grid = read()
ans1 , ansGrid = solve1(st,en,grid)
print(ans1)
print(solve2(st,en,ans1,grid))


"""
Function 'solve1' executed in 0.0167 seconds
114476
Function 'solve2' executed in 0.1218 seconds
508
"""