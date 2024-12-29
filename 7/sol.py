from utils import timeit
FILE_NAME = 'inp.txt'


def read():
    inps = []

    # Open the file and process its lines
    with open(FILE_NAME, 'r') as file:
        for line in file:
            vals = line.strip().split(' ')
            tot = int(vals[0][0:-1])
            vals = vals[1:]
            vals = [int(i) for i in vals]
            inps.append([tot,vals])
    return inps

@timeit
def solve1(inps):
    ans = 0
    unsolved = []

    def rec(idx,inp,tot,curr):
        n=len(inp)
        if (curr == tot and idx==n):
            return True
        if (curr > tot):
            return False
        if(idx>=n):
            return False
        return rec(idx+1,inp,tot,curr+inp[idx]) or rec(idx+1,inp,tot,curr*inp[idx])

    for i in inps:
        if(rec(1,i[1],i[0],i[1][0])):
            ans+=i[0]
        else :
            unsolved.append(i)
    return ans,unsolved

@timeit
def solve2(inps):
    ans = 0
    def rec(idx,inp,tot,curr,n):
        if (curr == tot and idx==n):
            return True
        if (curr > tot or idx>=n):
            return False
        return rec(idx+1,inp,tot,curr+inp[idx],n) or rec(idx+1,inp,tot,curr*inp[idx],n) or rec(idx+1,inp,tot,int(str(curr)+str(inp[idx])),n)

    for i in inps:
        if(rec(1,i[1],i[0],i[1][0],len(i[1]))):
            ans+=i[0]
    return ans

inps = read()
res,unsolved = solve1(inps)
print(res)
print(res+solve2(unsolved))
