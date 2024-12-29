from utils import timeit
from functools import lru_cache

file  = 'inp.txt'
def read():
    vals = []
    with open(file) as f:
        for line in f:
            vals=[int(x) for x in line.strip().split(' ')]
            break
    return vals

@timeit
def solve1and2(vals,steps):

    @lru_cache(maxsize=None)
    def rec(val,stepsMore):
        if(stepsMore == 0):
            return 1
        if val == 0 :
            return rec(1,stepsMore-1)
        elif len(str(val))%2 == 0 :
            val = str(val)
            return rec(int(val[:int(len(val)/2)]),stepsMore-1)+rec(int(val[int(len(val)/2):]),stepsMore-1)
        else:
            return rec(val*2024,stepsMore-1)

    ans = 0
    for val in vals:
        ans += rec(val,steps)

    return ans

vals = read()
print(solve1and2(vals,25))
print(solve1and2(vals,75))

"""
# with lru cache 
Function 'solve1and2' executed in 0.0023 seconds
182081
Function 'solve1and2' executed in 0.0890 seconds
216318908621637

#without lru cache 
Function 'solve1and2' executed in 0.1556 seconds
182081
Solve with 75 steps took infinite time - basically cannot see the program getting completed

"""