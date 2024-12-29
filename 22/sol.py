from collections import defaultdict
from functools import cache

from utils import timeit

FILE = 'inp.txt'


def read():
    inp = []
    with open(FILE, 'r') as file:
        for line in file:
            inp.append(int(line.strip()))
    return inp


LIMIT = 2000

def process(val):

    act = val

    val = val * 64
    val = val ^ act
    val = val % 16777216

    act = val
    val = val // 32
    val = val ^ act
    val = val % 16777216

    act = val
    val = val * 2048
    val = val ^ act
    val = val % 16777216

    return val

@timeit
def solve1(inp):
    ans = 0
    for i in inp:
        st = i
        for j in range(2000):
            st = process(st)
        ans += st
    return ans

def convertToStr(diff):
    return ''.join([str(i) for i in diff])

@timeit
def solve2(inp):
    ans = 0
    storage = defaultdict(int)

    for i in range(len(inp)):
        st = inp[i]
        strDiff = ""
        loclStorage = set()
        for j in range(2000):
            nxt_st = process(st)

            if j>3:
                if strDiff[0] == '-':
                    strDiff = strDiff[2:]
                else:
                    strDiff = strDiff[1:]
            strDiff += str((nxt_st % 10 - st % 10))
            if strDiff not in loclStorage:
                storage[strDiff] += nxt_st%10
                ans = max(ans, storage[strDiff])
                loclStorage.add(strDiff)
            st = nxt_st

    return ans



inp = read()
print(solve1(inp))
print(solve2(inp))


"""
Function 'solve1' executed in 1.0076 seconds
21147129593
Function 'solve2' executed in 3.1517 seconds
2445

TODO : This reddit post seems intersting , try this ?  https://www.reddit.com/r/adventofcode/comments/1hjyfl7/2024_day_22_parts_3_and_4_infinite_byers_and/
"""