def read():
  # Initialize empty lists
    list1 = []

    # Open the file and process its lines
    with open('inp1.txt', 'r') as file:
        for line in file:
            # Strip whitespace and split the line into values
            values = line.strip().split()
            values = [int(i) for i in values]
            list1.append(values)
    return list1

def solve1(list1):
    ans = 0
    for i in list1:
        if(validateUtil(i)):
            ans += 1
    return ans


def validateUtil(i):
    ln = len(i)
    sz = 0
    flag = True
    for j in range(1, ln):
        if (i[j] > i[j - 1]):
            sz += 1
        elif i[j] < i[j - 1]:
            sz -= 1
        else:
            flag = False
        if (not (abs(i[j] - i[j - 1]) >= 1 and abs(i[j] - i[j - 1]) <= 3)):
            flag = False
    if (flag and abs(sz) == ln - 1):
        return True
    return False


def solve2(list1):
    ans = 0
    for i in list1:
        if(validateUtil(i)):
            ans += 1
        else :
            for h in range(len(i)):
                listCopy = i.copy()
                # remove index h from listCopy
                listCopy.pop(h)
                if(validateUtil(listCopy)):
                    ans += 1
                    break
    return ans


l1 = read()
print("solving part 1 ")
print(solve1(l1))
print("solving part 2 ")
print(solve2(l1))




