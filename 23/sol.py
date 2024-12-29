from collections import defaultdict

from utils import timeit

FILE = "inp.txt"

def read():
    graph = defaultdict(list)
    with open(FILE, 'r') as file:
        for line in file:
            a,b = line.strip().split('-')
            graph[a].append(b)
            graph[b].append(a)
    return graph

@timeit
def solve1(graph):

    ones = 0
    twos = 0
    threes = 0
    for k,v in graph.items():
        if 't' == k[0]:
            sz = len(v)
            for i in range(sz):
                for j in range(i+1,sz):
                    if v[j] in graph[v[i]]:
                        if 't' == v[i][0] and 't' == v[j][0]:
                            threes+=1
                        elif 't' == v[i][0] or 't' == v[j][0]:
                            twos+=1
                        else:
                            ones+=1

    return ones + (twos//2) + (threes//3 )

@timeit
def solve2(graph):

    # https://en.wikipedia.org/wiki/Clique_problem#Listing_all_maximal_cliques

    curAnsLen = 0
    ans = ""
    def checkAnswer(nodes : list):
        nonlocal curAnsLen,ans
        sz = len(nodes)
        if sz < curAnsLen:
            return

        if sz == curAnsLen:
            ans = max(ans,','.join(sorted(nodes)))
        else:
            ans = ','.join(sorted(nodes))
        curAnsLen = sz


    def bron_kerbosch(graph, r, p, x,):
        if not p and not x:
            # No more nodes to process, R is a maximal clique
            checkAnswer(r)
            return

        for vertex in list(p):
            # Recursive call with updated sets
            bron_kerbosch(
                graph,
                r.union({vertex}),  # Add vertex to R
                p.intersection(graph[vertex]),  # P ∩ N(vertex)
                x.intersection(graph[vertex])  # X ∩ N(vertex)
            )
            # Move vertex from P to X
            p.remove(vertex)
            x.add(vertex)

    r = set()
    p = set(graph.keys())
    x = set()

    bron_kerbosch(graph, r, p, x)

    return ans

graph = read()
print(solve1(graph))
print(solve2(graph))

"""
Function 'solve1' executed in 0.0005 seconds
1467
Function 'solve2' executed in 0.2127 seconds
di,gs,jw,kz,md,nc,qp,rp,sa,ss,uk,xk,yn
"""