import time
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


def solve2(inps):
    ans = 0
    def rec(idx,inp,tot,curr,countJoin):
        n=len(inp)
        if (curr == tot and idx==n):
            return True
        if (curr > tot):
            return False
        if(idx>=n):
            return False
        return rec(idx+1,inp,tot,curr+inp[idx],countJoin) or rec(idx+1,inp,tot,curr*inp[idx],countJoin) or rec(idx+1,inp,tot,(curr*pow(10,len(str(inp[idx]))))+inp[idx],countJoin+1)

    for i in inps:
        if(rec(1,i[1],i[0],i[1][0],0)):
            ans+=i[0]
    return ans

inps = read()
st = time.time()
res,unsolved = solve1(inps)
print(res)
print("time taken in seconds :" + str(time.time()-st))


st = time.time()
print(res+solve2(unsolved))
print("time taken in seconds :" + str(time.time()-st))