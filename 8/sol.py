from utils import timeit
FILE_NAME = 'inp.txt'


def read():
    dct = {}
    n,m=0,0
    with open(FILE_NAME, 'r') as file:
        r=0
        for line in file:
            c=0
            for x in line:
                if x != '.' and x!='\n':
                    if x not in dct:
                        dct[x]=list()
                    dct[x].append((r,c))
                c+=1
                m=c
            r+=1
            n=r
    return n,m,dct

@timeit
def solve1(n,m,dct):
    ans=set()
    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m
    for k in dct:
        v=dct[k]
        ln = len(v)
        for i in range(ln):
            for j in range(i+1,ln):
                x = v[i][0]-v[j][0]
                y = v[i][1]-v[j][1]
                if isLimit(v[i][0]+x,v[i][1]+y) :
                    ans.add((v[i][0]+x,v[i][1]+y))
                if isLimit(v[j][0]-x,v[j][1]-y) :
                    ans.add((v[j][0]-x,v[j][1]-y))

    return len(ans)

@timeit
def solve2(n,m,dct):
    ans=set()
    def isLimit(x,y):
        return 0 <= x < n and 0 <= y < m
    for k in dct:
        v=dct[k]
        ln = len(v)
        for i in range(ln):
            for j in range(i+1,ln):
                ans.add((v[i][0],v[i][1]))
                ans.add((v[j][0],v[j][1]))
                x = v[i][0]-v[j][0]
                y = v[i][1]-v[j][1]
                fX = v[i][0]
                fY = v[i][1]
                while isLimit(fX+x,fY+y) :
                    fX = fX+x
                    fY = fY+y
                    ans.add((fX,fY))

                fX = v[j][0]
                fY = v[j][1]
                while isLimit(fX-x,fY-y) :
                    fX = fX-x
                    fY = fY-y
                    ans.add((fX,fY))

    return len(ans)

n,m,dct = read()
print(solve1(n,m,dct))
print(solve2(n,m,dct))