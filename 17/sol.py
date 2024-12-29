from utils import timeit
import re

FILE = "inp.txt"

def read():
    with open(FILE, 'r') as file:
        input_text = file.read()

    # Extract register values
    reg_pattern = r"Register ([A-C]): (\d+)"
    registers = {match.group(1): int(match.group(2)) for match in re.finditer(reg_pattern, input_text)}

    # Extract program values
    program_pattern = r"Program: ([\d,]+)"
    program_match = re.search(program_pattern, input_text)
    program = list(map(int, program_match.group(1).split(','))) if program_match else []

    # Map the values to desired output variables
    regA = registers.get('A', 0)
    regB = registers.get('B', 0)
    regC = registers.get('C', 0)

    return regA, regB, regC, program

@timeit
def solve1(regA,regB,regC,vals):
    n = len(vals)
    output = []

    ins = 0
    def getComboVal(x):
        if 0<=x<=3:
            return x
        if x==4:
            return regA
        if x==5:
            return regB
        if x==6:
            return regC
        assert x<7

    def process(opcode,operand):
        nonlocal ins,regA,regB,regC,output
        if opcode==0:
            temp = regA
            temp2 = int(pow(2,getComboVal(operand)))
            regA = temp//temp2
            ins+=2
        elif opcode == 1 :
            regB = regB ^ operand
            ins+=2
        elif opcode == 2:
            regB = getComboVal(operand)%8
            ins+=2
        elif opcode == 3:
            if regA == 0 :
                ins+=2
            else:
                ins = operand
        elif opcode==4:
            regB = regB ^ regC
            ins += 2
        elif opcode==5:
            output.append(getComboVal(operand)%8)
            ins+=2
        elif opcode==6:
            temp = regA
            temp2 = int(pow(2, getComboVal(operand)))
            regB = temp // temp2
            ins += 2
        elif opcode==7:
            temp = regA
            temp2 = int(pow(2, getComboVal(operand)))
            regC = temp // temp2
            ins += 2

    while 0<=ins<n-1:
        process(vals[ins],vals[ins+1])


    return output


regA,regB,regC,vals = read()

@timeit
def solve2(regB,regC,vals):
    """
    Todo : add the math solving logic from notes to here
    """

    times = len(vals)
    inf = 999999999999999999999999999999999
    ans = inf


    def rec(timesl,ansHold):
        nonlocal ans
        if timesl == 0:
            ans = min(ans,int(str(ansHold), 8))
            return
        for i in range(0,8):
            lans = solve1(int(ansHold+str(i), 8),regB,regC,vals)
            if vals[-len(lans):] == lans:
                rec(timesl-1,ansHold+str(i))


    rec(times,"")
    assert ans!=inf
    return ans


print(','.join(map(str,solve1(regA,regB,regC,vals))))
print(solve2(regB,regC,vals))

"""
Function 'solve1' executed in 0.0000 seconds
5,1,4,0,5,1,0,2,6
Function 'solve2' executed in 0.0585 seconds
202322936867370
"""