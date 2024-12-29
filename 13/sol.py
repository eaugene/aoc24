from utils import timeit
import re
FILE = "inp.txt"
def read():
    with open(FILE, 'r') as file:
        lines = file.readlines()

    results = []
    for i in range(0, len(lines), 4):  # Process every 4 lines as a set , the 4th line is empty
        set_values = []
        # Process Button A line
        button_a_match = re.findall(r'\bX\+(\d+)|Y\+(\d+)', lines[i])
        set_values.extend([int(val) for pair in button_a_match for val in pair if val])

        # Process Button B line
        button_b_match = re.findall(r'\bX\+(\d+)|Y\+(\d+)', lines[i + 1])
        set_values.extend([int(val) for pair in button_b_match for val in pair if val])

        # Process Prize line
        prize_match = re.findall(r'X=(\d+)|Y=(\d+)', lines[i + 2])
        set_values.extend([int(val) for pair in prize_match for val in pair if val])

        results.append(set_values) # x1 y1 x2 y2 X Y

    return results

INF = 9999999999999

@timeit
def solve1(vals):
    pushACost = 3
    pushBCost = 1
    def solve(val):
        mn = INF
        x1, y1, x2, y2, X, Y = val
        for pushA in range(1,101):
            if (X - pushA*x1) % x2 == 0:
                pushB = (X - pushA*x1) // x2
                if pushB <=100 and pushA*y1 + pushB*y2 == Y:
                    mn = min(mn, pushA*pushACost + pushB*pushBCost)
        return mn



    ans =0
    for i in vals:
        mn = solve(i)
        if mn != INF:
            ans += mn
    return ans


@timeit
def solve2(vals):
    pushACost = 3
    pushBCost = 1

    def solve(val):
        '''

        Given :
        (A * x1) + (B * x2) = X
        (A * y1) + (B * y2) = Y


         (1) B = (X - (A * x1)) / x2
         (2) B = (Y - (A * y1)) / y2

         equating sides of B :
            (X - (A * x1)) / x2 = (Y - (A * y1)) / y2

        pull A out
            (y2 * X ) - ( A * x1 * y2 ) = (x2 * Y) - (A * x2 * y1)
            A = ((x2 * Y) - (X * y2)) / ((x2 * y1) - (x1 * y2))

        From A find B as in problem 1

        '''
        mn = INF
        x1, y1, x2, y2, X, Y = val
        numerator = (x2*Y)-(X*y2)
        denom =  (x2*y1) - (x1*y2)
        if denom !=0 and numerator % denom == 0:
            pushA = numerator // denom
            if (X - (pushA * x1)) % x2 == 0:
                pushB = (X - pushA * x1) // x2
                # optional add condition to check pushB>0
                mn = pushA * pushACost + pushB * pushBCost
        return mn



    ans =0
    for i in vals:
        i[4] += 10000000000000
        i[5] += 10000000000000
        mn = solve(i)
        if mn != INF:
            ans += mn
    return ans

vals = read()
print(solve1(vals))
print(solve2(vals))