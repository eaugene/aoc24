from utils import timeit

FILE='inp.txt'
def read():
    lst = []
    with open(FILE, 'r') as file:
        for line in file:
            line = line.strip()
            lst = [int(x) for x in line if x!='\n']
            lst = [[lst[i],int(i/2)] if i%2 == 0 else [lst[i],-1] for i in range(len(lst)) ]
    return lst


@timeit
def solve1(lst):
    ans = 0
    n = len(lst)
    id = 0
    i=0
    j=n-1
    if(lst[j][1]==-1):
        j -= 1
    for k in range(lst[0][0]):
        ans += (id*lst[0][1])
        id += 1
    i += 1
    while(i<=j):
        if i ==j :
            for k in range(lst[j][0]):
                ans += (id * lst[j][1])
                id += 1
            break
        while(lst[j][0]>0 and lst[i][0]>0):
            ans += (id * lst[j][1])
            lst[j][0] -= 1
            lst[i][0] -= 1
            id += 1

        if(lst[j][0] == 0):
            j -= 2
        if(lst[i][0] == 0):
            i += 1
            for k in range(lst[i][0]):
                ans += (id * lst[i][1])
                id += 1
            i += 1
    return ans


def read2():
    lst = []
    with open(FILE, 'r') as file:
        for line in file:
            line = line.strip()
            lst = [int(x) for x in line if x!='\n']
            lst = [[0,[[lst[i],int(i/2)]]] if i%2 == 0 else [lst[i],[]] for i in range(len(lst)) ]
    return lst

@timeit
def solve2(lst):
    # This currently runs at O(n^2) , if you have time later , try to optimise it
    ans = 0
    n = len(lst)
    id = 0
    j=n-1
    if j%2:
        j -= 1
    while j>=0:
        i=1
        if lst[j][1][0] == 0:
            j -= 2
            continue
        while(i<j):
            if lst[i][0] < lst[j][1][0][0]:
                i += 2
            else:
                lst[i][0] -= lst[j][1][0][0]
                lst[i][1].append(lst[j][1][0])
                lst[j][0] = lst[j][1][0][0]
                lst[j][1]= []
                break
        j-=2
    for i in lst:
        for J in i[1]:
            ans+= J[1]*( (id*J[0])+int((J[0]*(J[0]-1))/2) )
            id += J[0]
        if i[0]>0:
            id+=i[0]
    return ans




lst = read()
print(solve1(lst))

lst = read2()
print(solve2(lst))
