from utils import timeit

def read():
  # Initialize empty lists
    list1 = []
    list2 = []

    # Open the file and process its lines
    with open('inp.txt', 'r') as file:
        for line in file:
            # Strip whitespace and split the line into two values
            values = line.strip().split()
            if len(values) == 2:  # Ensure there are exactly two elements
                list1.append(int(values[0]))  # Add the first value to list1
                list2.append(int(values[1]))  # Add the second value to list2
    return list1,list2

@timeit
def solve1(list1,list2):
    list1.sort()
    list2.sort()
    ln = len(list1)
    ans = 0
    for i in range(ln):
        ans += (abs(list1[i]-list2[i]))
    print(ans)

@timeit
def solve2(list1,list2):
    dct = {}
    for i in list2:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1
    ans=0
    for i in list1:
        if i in dct:
            ans += (i*dct[i])

    print(ans)

l1,l2 = read()
solve1(l1,l2)
solve2(l1,l2)