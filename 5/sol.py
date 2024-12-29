from collections import defaultdict, deque

from utils import timeit


def read():
    # Initialize empty lists
    edges = []
    pagesInUpdate = False
    queries = []

    # Open the file and process its lines
    with open('inp.txt', 'r') as file:
        for line in file:
            if(line == '\n'):
                pagesInUpdate = True
                continue
            if pagesInUpdate:
                pages = line.strip().split(',')
                pages = [int(i) for i in pages]
                queries.append(pages)
            else :
                values = line.strip().split('|')
                values = [int(i) for i in values]
                edges.append(values)
    return edges, queries


def buildTopoSort(edges : [[int,int]]) -> [int]:
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Create graph representation
    for v, u in edges: ## see here its v,u and not u,v
        graph[u].append(v)
        in_degree[v] += 1
        if u not in in_degree:
            in_degree[u] = 0  # Ensure all nodes are in in_degree

    # Queue for nodes with no incoming edges
    queue = deque([node for node in in_degree if in_degree[node] == 0])

    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check for cycles
    if len(topo_order) != len(in_degree):
        raise ValueError("Graph is not a DAG; topological sorting is not possible.")

    return topo_order

@timeit
def solve1(edges : [[int]], queries : [[int]]):
    setRules = set()
    ans = 0
    inCorrectQueries = []
    for e in edges:
        setRules.add((e[0],e[1]))
    for q in  queries:
        okay = True
        ln = len(q)
        for i in range(1,ln):
            if (q[i-1],q[i]) not in setRules:
                okay = False
                break
        if okay:
            ans += q[int(ln/2)]
        else :
            inCorrectQueries.append(q)
    return ans,inCorrectQueries

@timeit
def solve2(edges : [[int]],queries : [[int]]):
    setRules = set()
    for e in edges:
        setRules.add((e[0], e[1]))
    ans = 0
    for q in queries:
        ln = len(q)
        rulePairs = []
        for i in range(ln):
            for j in range(i+1,ln):
                if (q[i],q[j]) in setRules:
                    rulePairs.append([q[i],q[j]])
                elif (q[j],q[i]) in setRules:
                    rulePairs.append([q[j],q[i]])
        # now the rules for the elements are collected
        topoOrder = buildTopoSort(rulePairs)
        ans += topoOrder[int(len(topoOrder)/2)]
    return  ans

edges,queries = read()
ans1,inCorrectQueries = solve1(edges,queries)
print(ans1)
print(solve2(edges,inCorrectQueries))




