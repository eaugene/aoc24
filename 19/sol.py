from functools import lru_cache
from utils import timeit

FILE = "inp.txt"

# TODO : Next time try to do it better in Trie (or) any other optimised way

def read():
    vals = []
    inp = []

    with open(FILE, 'r') as file:
        valEnd = False
        for line in file:
            if line == '\n':
                valEnd = True
                continue
            if not valEnd:
                vals = line.strip().split(', ')
            else:
                inp.append(line.strip())
    return vals,inp

@timeit
def solve1(vals,inp):

    @lru_cache(maxsize=None)
    def rec(rem):
        if len(rem) == 0:
            return True

        hol = False
        for v in vals:
            if len(rem) >= len(v) and v == rem[:len(v)]:
                hol = hol or rec(rem[len(v):])
        return hol

    ans = 0
    for i in inp:
        ans += rec(i)

    return ans

@timeit
def solve2(vals,inp):
    ans = 0

    @lru_cache(maxsize=None)
    def rec(rem):
        lans = 0
        if len(rem) == 0:
            return 1

        for v in vals:
            if len(rem) >= len(v) and v == rem[:len(v)]:
                lans += rec(rem[len(v):])
        return lans

    for i in inp:
        ans+= rec(i)
    return ans



vals , inp = read()
print(solve1(vals,inp))
print(solve2(vals,inp))


