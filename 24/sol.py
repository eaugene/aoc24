from functools import cache
from utils import timeit

FILE = 'inp.txt'

def read():
    initDone = False
    equation = {}
    reverseEquation = {}
    zs = []
    maxBitIndex=-1
    with open(FILE, 'r') as file:
        for line in file:
            if line == '\n':
                initDone = True
                continue
            if not initDone:
                val = line.strip().split(': ')
                reverseEquation[val[0]] = val[1] # x01 -> 0
                maxBitIndex = max(maxBitIndex,int(val[0][1:]))
            else:
                val = line.strip().split(' -> ')
                equation[val[0]] = val[1] # ntg XOR fgs -> mjb
                reverseEquation[val[1]] = val[0] # mjb -> ntg XOR fgs
                if 'z' in val[1][0]:
                    zs.append(val[1])

    return equation,reverseEquation,sorted(zs,reverse=True),maxBitIndex


@cache
def solve1Util(val):
    assert val in revEq
    if len(revEq[val]) == 1:
        return int(revEq[val])

    sp = revEq[val].split(' ')
    assert len(sp) == 3
    op1 = sp[0]
    op2 = sp[2]

    if sp[1] == 'AND':
        return solve1Util(op1) & solve1Util(op2)
    if sp[1] == 'OR':
        return solve1Util(op1) | solve1Util(op2)
    if sp[1] == 'XOR':
        return solve1Util(op1) ^ solve1Util(op2)
    assert False

@timeit
def solve1(zs):
    ans = 0
    for z in zs:
        ans = ( ans<<1 ) + (solve1Util(z))
    return ans

@timeit
def solve2(maxBitIndex):
    """
    ## Circuit Diagram
    For a 6bit Full Adder - https://github.com/eaugene/aoc24/blob/main/24/6BitAdderCircuit.jpg  . ( however , note that this problem is 45 bit adder )

    ## A brief of the solving idea
    (1) Based on the constraints given in the problem , we are sure that changes of wire are in pairs
    (2) Also , the only possible gates are AND , XOR , OR . So we need to make a full added with them ( refer the circuit image attached above )

    Case 1 ( handleMalform() ) :
    In this case , we know whats the expected wire , but unfortunately , we get some other thing as output from X operation Y , so we swap that other wire with the expected wire .

    Case 2 ( handleMalform2() ) :
    So when we find a out wires ( say X , Y and operation like "X operation Y" (or) "Y operation X" ) which does not match with any of the given operation list ( variable eq in our case ) , then we can suspect that some problem is there .
    In this case , we try to search in operations with half of the eq ( i.e X & operation (or) Y & Operation ) and try to find the other wire from the remaning section ( findRemFromHalf() ) .
    Buy this we would know the which wire is wrong and whats the correct one , so we swap it


    PS : This is solvable by hand ( I did solve this in notebook first ) , but making to code is the tricky part ( I later wrote the code - what's the fun of Advent if we cannot code it out ? :D )
    """

    ans = []

    def handleMalform(op1,op2,operation,expected):
        actual = eq[getExistingEquation(op1,op2,operation)]
        swapWires(actual,expected)

    def swapWires(wire1,wire2):
        nonlocal ans
        global eq,revEq

        ans.append(wire1)
        ans.append(wire2)
        r1 = revEq[wire1]
        r2 = revEq[wire2]
        revEq[wire1] = r2
        revEq[wire2] = r1
        eq[r1] = wire2
        eq[r2] = wire1

    def findRemFromHalf(op,operation):
        checkStr = [op+" "+operation,operation+" "+op]
        for c in checkStr:
            for k,v in eq.items():
                if c in k:
                    return k.replace(c,'').strip()
        return None

    def handleMalform2(wire1,wire2,op):

        #suspect wire 1 is wrong
        otherWrongWire = findRemFromHalf(wire2,op)
        if otherWrongWire is not None:
            swapWires(wire1,otherWrongWire)
            return otherWrongWire,wire2

        #suspect wire 2 is wrong
        otherWrongWire = findRemFromHalf(wire1,op)
        if otherWrongWire is not None:
            swapWires(wire2,otherWrongWire)
            return wire1,otherWrongWire

        assert False


    def getExistingEquation(op1,op2,operation):
        if op1+" "+operation+" "+op2 in eq:
            return op1+" "+operation+" "+op2
        if op2+" "+operation+" "+op1 in eq:
            return op2+" "+operation+" "+op1
        return None


    # 0th bit
    x = 'x00'
    y = 'y00'
    z = 'z00'

    actual_out_wire = eq[getExistingEquation(x,y,'XOR')]
    actual_carry_wire = eq[getExistingEquation(x,y,'AND')]
    if actual_out_wire != z:
        handleMalform(x,y,'XOR',z)

    if not maxBitIndex >= 1:
        if actual_carry_wire != 'z01':
            handleMalform('x00','y00','AND','z01')
        return ans

    # 1st bit
    x = 'x01'
    y = 'y01'
    z = 'z01'

    currBitAdder = eq[getExistingEquation(x,y,'XOR')]
    if getExistingEquation(currBitAdder,actual_carry_wire,'XOR') is None:
        currBitAdder,actual_carry_wire = handleMalform2(currBitAdder,actual_carry_wire,'XOR')
    actual_out_wire = eq[getExistingEquation(currBitAdder,actual_carry_wire,'XOR')]
    if actual_out_wire != z:
        handleMalform(x,y,'XOR',z)
    actual_carry_wire = eq[getExistingEquation(currBitAdder, actual_carry_wire, 'AND')]

    # 2nd to n th bit
    for i in range(2, maxBitIndex + 1):
        prevx = 'x'+('0' if 0<=i-1<=9 else '')+str(i-1)
        prevy = 'y'+('0' if 0<=i-1<=9 else '')+str(i-1)
        x = 'x'+('0' if 0<=i<=9 else '')+str(i)
        y = 'y'+('0' if 0<=i<=9 else '')+str(i)
        z = 'z'+('0' if 0<=i<=9 else '')+str(i)

        actual_prev_carry = eq[getExistingEquation(prevx,prevy,'AND')]
        if getExistingEquation(actual_prev_carry,actual_carry_wire,'OR') is None:
            actual_prev_carry,actual_carry_wire = handleMalform2(actual_prev_carry,actual_carry_wire,'OR')


        actual_carry_represntation = eq[getExistingEquation(actual_prev_carry,actual_carry_wire,'OR')]
        currBitAdder = eq[getExistingEquation(x,y,'XOR')]

        if getExistingEquation(currBitAdder,actual_carry_represntation,'XOR') is None:
            currBitAdder,actual_carry_represntation = handleMalform2(currBitAdder,actual_carry_represntation,'XOR')

        actual_out_wire = eq[getExistingEquation(currBitAdder,actual_carry_represntation,'XOR')]

        if actual_out_wire != z:
            handleMalform(currBitAdder,actual_carry_represntation,'XOR',z)

        actual_carry_wire = eq[getExistingEquation(currBitAdder, actual_carry_represntation, 'AND')]

    # n+1 th bit
    prevx = 'x' + ('0' if 0 <= (maxBitIndex) <= 9 else '') + str(maxBitIndex)
    prevy = 'y' + ('0' if 0 <= (maxBitIndex) <= 9 else '') + str(maxBitIndex)
    z='z' + ('0' if 0 <= (maxBitIndex + 1) <= 9 else '') + str(maxBitIndex + 1)
    actual_prev_carry = eq[getExistingEquation(prevx, prevy, 'AND')]
    if getExistingEquation(actual_prev_carry, actual_carry_wire, 'OR') is None:
        actual_prev_carry, actual_carry_wire = handleMalform2(actual_prev_carry, actual_carry_wire, 'OR')

    actual_out_wire = eq[getExistingEquation(actual_prev_carry, actual_carry_wire, 'OR')]
    if actual_out_wire != z:
        handleMalform(actual_prev_carry,actual_carry_wire,'OR',z)

    return ','.join(sorted(ans))


@timeit
def assertionOfAdderCircuitAfterSolve2(maxBitIndex):
    xval = ['x'+('0' if 0<=i<=9 else '')+str(i) for i in range(maxBitIndex,-1,-1)]
    yval = ['y'+('0' if 0<=i<=9 else '')+str(i) for i in range(maxBitIndex,-1,-1)]

    solve1Util.cache_clear() # imp , else the caches from solve1(zs) will come , note at solve 2 we are changing the circuit
    lhs = solve1(xval)+solve1(yval)
    rhs = solve1(zs)
    assert lhs == rhs

eq,revEq,zs,maxBitIndex = read()
print(solve1(zs))
print(solve2(maxBitIndex))

assertionOfAdderCircuitAfterSolve2(maxBitIndex)

"""
Function 'solve1' executed in 0.0002 seconds
64755511006320
Function 'solve2' executed in 0.0002 seconds
djg,dsd,hjm,mcq,sbg,z12,z19,z37

Function 'assertionOfAdderCircuitAfterSolve2' executed in 0.0002 seconds
"""