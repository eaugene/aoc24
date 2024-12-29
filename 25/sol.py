from utils import timeit

FILE = "inp.txt"

def read():

    keys = []
    locks = []

    def getCount(locl):
        m = len(locl[0])
        n = len(locl)
        hol = []
        for j in range(m):
            cnt = 0
            for i in range(n):
                if locl[i][j] == '#':
                    cnt += 1
            hol.append(cnt)
        return hol

    def processLocl(locl):
        if locl[0] == '#####' and locl[-1]=='.....':
            locks.append(getCount(locl[1:-1]))
        elif locl[0] == '.....' and locl[-1]=='#####':
            keys.append(getCount(locl[1:-1][::-1]))

    with open(FILE, 'r') as file:
        locl = []
        for line in file:
            if line == '\n':
                processLocl(locl)
                locl = []
                continue
            else:
                locl.append(line.strip())
        processLocl(locl)

    return keys,locks

@timeit
def solve1Brute(keys,locks):
    ans = 0
    for key in keys:
        for lock in locks:
            if all([key[i]+lock[i]<=5 for i in range(5)]):
                ans += 1
    return ans

@timeit
def solve1Optimised(keys,locks):
    """
    Hard coded some values , to make it quick in implementation . Ignore them . xD
    """

    m = len(keys[0])

    keysLessThanInPosition = [[set() for i in range(6)] for j in range(m)]


    for j in range(m):
        for keyIdx in range(len(keys)):
            keysLessThanInPosition[j][keys[keyIdx][j]].add(keyIdx)
        for i in range(1,6):
            keysLessThanInPosition[j][i].update(keysLessThanInPosition[j][i-1])

    ans =0
    for lock in locks:
        rem = 5 - lock[0]
        hol = keysLessThanInPosition[0][rem]
        for l in range(1,5):
            rem = 5 - lock[l]
            hol = hol.intersection(keysLessThanInPosition[l][rem])
        ans += len(hol)


    return ans

@timeit
def solve2():
    return "A tribute to Eric Wastl https://was.tl/ for creating this"

keys,locks = read()
print(solve1Brute(keys,locks))
print(solve1Optimised(keys,locks))
print(solve2())

"""
Function 'solve1Brute' executed in 0.0316 seconds
3287
Function 'solve1Optimised' executed in 0.0017 seconds
3287
Function 'solve2' executed in 0.0000 seconds
A tribute to Eric Wastl https://was.tl/ for creating this
"""