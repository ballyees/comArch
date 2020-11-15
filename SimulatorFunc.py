from Config import Config

#------------------------------------------------------------------------------------------------------#
#                                                  CONVERT                                             #
#------------------------------------------------------------------------------------------------------#

def cvtTwosComplement(value: str) -> int:
    if value[0] == "1":
        val = -((int(value, base=2) ^ (Config.xor32Bit if len(value) == 32 else Config.xor16Bit)) + 1)
    else: 
        val = int(value[1:], base=2)
    return val

def isFillFormat(splitAddress: list, address: str) -> bool:
    twosCompVal = cvtTwosComplement(address)
    if (splitAddress[0] != Config.MSB7) or (Config.maxNegativeValue <= twosCompVal <= Config.maxPositiveValue):
        return True

def fillFormat(address: str, addr: list) -> None:
    addr.append('.fill')
    addr.append(cvtTwosComplement(address))

def rTypeFormatter(splitAddress: list, addr: list) -> None:
    # opcode
    addr.append(Config.opcodeRTypeBin[splitAddress[1]])
    # reg A
    addr.append(int(splitAddress[2][:3], base=2))
    # reg B
    addr.append(int(splitAddress[2][3:6], base=2))
    # dest reg
    addr.append(int(splitAddress[2][len(splitAddress[2]) - 3:], base=2))

def iTypeFormatter(splitAddress: list, addr: list) -> None:
    # opcode
    addr.append(Config.opcodeITypeBin[splitAddress[1]])
    # reg A
    addr.append(int(splitAddress[2][:3], base=2))
    # reg B
    addr.append(int(splitAddress[2][3:6], base=2))
    # offsetField
    addr.append(cvtTwosComplement(splitAddress[2][6:]))

def jTypeFormatter(splitAddress: list, addr: list) -> None:
    # opcode
    addr.append(Config.opcodeJTypeBin[splitAddress[1]])
    # reg A
    addr.append(int(splitAddress[2][:3], base=2))
    # reg B
    addr.append(int(splitAddress[2][3:6], base=2))

def oTypeFormatter(splitAddress: list, addr: list) -> None:
    # opcode
    addr.append(Config.opcodeOTypeBin[splitAddress[1]])

def splitOpcode(address: str) -> list:
    addr = []
    splitAddr = [address[:7], address[7:10], address[10:]]
    if isFillFormat(splitAddr, address):
        fillFormat(address, addr)
    elif (Config.opcodeOTypeBin.get(splitAddr[1], None)):
        # O Type
        oTypeFormatter(splitAddr, addr)
    elif Config.opcodeRTypeBin.get(splitAddr[1], None):
        # R Type
        rTypeFormatter(splitAddr, addr)
    elif Config.opcodeITypeBin.get(splitAddr[1], None):
        # I Type
        iTypeFormatter(splitAddr, addr)
    elif Config.opcodeJTypeBin.get(splitAddr[1], None):
        # J Type
        jTypeFormatter(splitAddr, addr)
    else:
        fillFormat(address, addr)
    # print(address, addr)
    return addr, cvtTwosComplement(address)

#------------------------------------------------------------------------------------------------------#
#                                                  SIMULATOR                                           #
#------------------------------------------------------------------------------------------------------#

def printMemory(memory: list):
    print('memory:')
    for i, addr in enumerate(memory):
        print(f'\tmem[ {i} ] {addr[1]}')
def printItemInMemory(memory: list):
    print('memory:')
    for i, addr in enumerate(memory):
        print(f'\tmem[ {i} ] {addr[0]}')

def printState(pc: int, memory: list, register: list):
    print('@@@')
    print('state:')
    print(f'\tpc {pc}')
    print('\tmemory:')
    for i, addr in enumerate(memory):
        print(f'\t\tmem[ {i} ] {addr[1]}')
    print('\tregisters:')
    for i, val in enumerate(register):
        print(f'\t\treg[ {i} ] {val}')
    print('end state\n',)

def nand1bit(p: chr, q: chr) -> str:
    return '0' if p == '1' and q == '1' else '1'

def nand16bit(a: str, b: str) -> str:
    return ''.join((nand1bit(p, q) for p, q in zip(a, b)))

def twosComplement16Bit(val: int):
        if val < 0:
            val = (val ^ Config.xor16Bit) + 1
        val = f'{val:016b}'.replace('-', '')
        return val

def nandInstruction(reg: list, dest: int, regA: int, regB: int) -> None:
    if not isAssignRegister0(dest):
        # regA16 = f'{reg[regA]:016b}'
        # regB16 = f'{reg[regB]:016b}'
        regA16 = twosComplement16Bit(reg[regA])
        regB16 = twosComplement16Bit(reg[regB])
        result = cvtTwosComplement(nand16bit(regA16, regB16))
        reg[dest] = result

def addInstruction(reg: list, dest: int, regA: int, regB: int) -> None:
    if not isAssignRegister0(dest):
        reg[dest] = reg[regA] + reg[regB]

def lwInstruction(reg: list, memory: list, stack: list, offsetField: int, regA: int, regB: int) -> int:
    if offsetField:
        # reg[regB] = reg[regA] + offsetField
        print(reg[regA])
        print(memory[reg[regA] + offsetField])
        reg[regB] = memory[reg[regA] + offsetField][1]
    else:
        # stack
        if len(stack) > 0:
            stack = stack.pop()
            reg[regA] = len(stack) #fixed register / regA = 7 and can do it by using addInstruction (Teacher do that)
        # stack[i] = reg[regA]
        # stack[i+1] = reg[regB]  
        # reg[regB] = reg[regA] + stack.pop()
    return 1

def swInstruction(reg: list, memory: list, stack: list, offsetField: int, regA: int, regB: int) -> int:
    if offsetField:
        pass
    else:
        stack = stack.append(reg[regB])
        reg[regA] = len(stack) #can do it by using addInstaruction (Teacher do that) 
    return 1

def beqInstruction(reg: list, memory: list, stack: list, offsetField: int, regA: int, regB: int) -> int:
    return offsetField+1 if reg[regA] == reg[regB] else 1

def jalrInstruction(reg: list, regA: int, regB: int, pc: int) -> int:
    if (reg[regA] == reg[regB]):
        reg[regB] = pc + 1
        return pc - reg[regA]
    else:
        reg[regB] = pc + 1
        return reg[regA] - pc

def haltInstruction(instructionsExecuted: int, pc: int, memory: list, register: list) -> None:
    print('machine halted')
    print(f'total of {instructionsExecuted} instructions executed')    
    print('final state of machine:\n')
    printState(pc, memory, register)

def isAssignRegister0(destReg: int):
    return not destReg

#------------------------------------------------------------------------------------------------------#
#                                                  SIMULATOR                                           #
#------------------------------------------------------------------------------------------------------#

FuncRType = {
    "add": addInstruction,
    'nand': nandInstruction
}
FuncIType = {
    'lw': lwInstruction,
    'sw': swInstruction,
    'beq': beqInstruction
}
FuncJType = {
    'jalr': jalrInstruction
}