import re

pattern = r"mul\(\d{1,3},\d{1,3}\)"
FILE = 'inp.txt'
def read():
    val = []
    with open(FILE, 'r') as file:
        for line in file:
            matches = re.findall(pattern, line)
            for m in matches:
                i,j = m[4:-1].split(',')
                val.append((int(i),int(j)))
    return val


def solve1(mulList):
    ans = 0
    for i,j in mulList:
        ans += ( i*j)
    return ans

pattern2 = r"mul\(\d{1,3},\d{1,3}\)|don'?t\(\)|do\(\)"


def read2():
    val = []
    with open(FILE, 'r') as file:
        for line in file:
            matches = re.findall(pattern2, line)
            val.extend(matches)
    return val

def solve2(list2):
    ans = 0
    enable = True
    for i in list2:
        if( i == 'do()'):
            enable = True
        elif( i == 'don\'t()'):
            enable = False
        elif( enable ):
            x,y = i[4:-1].split(',')
            ans += (int(x)*int(y))
    return ans

mulList = read()
print(solve1(mulList))

list2 = read2()
print(list2)
print(solve2(list2))