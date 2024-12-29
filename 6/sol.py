FILE='inp.txt'
def read():
    grid = []
    lno = 0
    GuardPos = [-1,-1]
    with open(FILE, 'r') as file:
        for line in file:
            line = line.strip()
            if '^' in line:
                GuardPos = [lno, line.index('^')]
                line.replace('^','.')
            grid.append([c for c in line])
            lno+=1
    return grid,GuardPos

set1 = set()
set2 = set()

def solve1(grid,GuardPos) :
    n = len(grid)
    m = len(grid[0])
    dirs = [[-1,0],[0,1],[1,0],[0,-1]] # top right down left
    dir = 0
    uniqPos = set()
    uniqPos.add((GuardPos[0],GuardPos[1]))
    def inLimit(i,j):
        return i>=0 and i<n and j>=0 and j<m

    x = GuardPos[0] + dirs[dir][0]
    y = GuardPos[1] + dirs[dir][1]

    while(inLimit(x,y)):
        if(grid[x][y] == '#'):
            x -= dirs[dir][0]
            y -= dirs[dir][1]
            dir = (dir+1)%4
        else :
            uniqPos.add((x, y))
        x += dirs[dir][0]
        y += dirs[dir][1]
    return len(uniqPos)


def solve2Util(grid,GuardPos) :
    n = len(grid)
    m = len(grid[0])
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # top right down left
    dir = 0
    uniqPos = set()
    uniqPos.add((GuardPos[0], GuardPos[1],dir))

    def inLimit(i, j):
        return i >= 0 and i < n and j >= 0 and j < m

    x = GuardPos[0] + dirs[dir][0]
    y = GuardPos[1] + dirs[dir][1]

    while (inLimit(x, y)):
        if (grid[x][y] == '#'):
            x -= dirs[dir][0]
            y -= dirs[dir][1]
            dir = (dir + 1) % 4
        else:
            if (x,y,dir) in uniqPos:
                return True
            uniqPos.add((x, y,dir))
        x += dirs[dir][0]
        y += dirs[dir][1]
    return False

def solve2Brute(grid,GuardPos):
    # this is a brute force way O(n^4) . Do in a optimised manner
    n = len(grid)
    m = len(grid[0])
    ans = 0
    for i in range(n):
        for j in range(m):
            if i==GuardPos[0] and j==GuardPos[1]:
                continue
            if(grid[i][j] == '.'):
                grid[i][j] = '#'
                if(solve2Util(grid,GuardPos)):
                    ans += 1
                    set1.add((i,j))
                grid[i][j] = '.'
    return ans


def solve2Optimised(grid,GuardPos):
     # this won't work . Why ? think of a case when you are putting the block on a path , but the path in reverse direction is already visited .
    n = len(grid)
    m = len(grid[0])
    dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]  # top right down left
    dir = 0
    ans = 0

    topBottom = [[[-1,j] for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if(grid[i][j] == '#'):
                topBottom[i][j] = [i,j]
            elif (i!=0):
                topBottom[i][j] = topBottom[i-1][j]
    bottomTop = [[[-1,j] for j in range(m)] for i in range(n)]
    for i in range(n-1,-1,-1):
        for j in range(m):
            if(grid[i][j] == '#'):
                bottomTop[i][j] = [i,j]
            elif(i!=n-1) :
                bottomTop[i][j] = bottomTop[i+1][j]
    leftRight = [[[i,-1] for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            if(grid[i][j] == '#'):
                leftRight[i][j] = [i,j]
            elif(j!=0) :
                leftRight[i][j] = leftRight[i][j-1]
    rightLeft = [[[i,-1] for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m-1,-1,-1):
            if(grid[i][j] == '#'):
                rightLeft[i][j] = [i,j]
            elif(j!=m-1) :
                rightLeft[i][j] = rightLeft[i][j+1]

    uniqPos = set()
    uniqPos.add((GuardPos[0], GuardPos[1]))



    def inLimit(i, j):
        return i >= 0 and i < n and j >= 0 and j < m

    hol = [topBottom,rightLeft, bottomTop, leftRight]

    def isLock(lx,ly,x,y,dir):
        cX = x
        cY = y
        locks = set()
        locks.add((lx,ly,dir))
        dir = (dir+1)%4
        while True:
            cX = hol[dir][cX][cY][0]
            cY = hol[dir][cX][cY][1]
            if dir==0 and (cX < lx or cX==-1) and cY == ly:
                cX = lx
            if dir==1 and cX == lx and ( cY > ly or cY == -1 ):
                cY = ly
            if dir==2 and (cX > lx or cX==-1) and cY == ly:
                cX = lx
            if dir==3 and cX == lx and ( cY < ly or cY == -1 ):
                cY = ly
            if(cX == -1 or cY == -1):
                return False
            if (cX, cY, dir) in locks:
                return True
            locks.add((cX,cY,dir))
            cX = cX - dirs[dir][0]
            cY = cY - dirs[dir][1]
            dir = (dir + 1) % 4





    x = GuardPos[0] + dirs[dir][0]
    y = GuardPos[1] + dirs[dir][1]

    while (inLimit(x, y)):
        if (grid[x][y] == '#'):
            x -= dirs[dir][0]
            y -= dirs[dir][1]
            dir = (dir + 1) % 4
        else:
            olX = x - dirs[dir][0]
            olY = y - dirs[dir][1]
            if( (x!=GuardPos[0] or y!=GuardPos[1]) and isLock(x,y,olX,olY,dir)):
                ans += 1
                set2.add((x,y))

        x += dirs[dir][0]
        y += dirs[dir][1]
    return ans

grid,guaardPos = read()
#print(solve1(grid,guaardPos))
print(solve2Brute(grid,guaardPos))
print("###")
print(solve2Optimised(grid,guaardPos))

print(set1-set2)
print(set2-set1)