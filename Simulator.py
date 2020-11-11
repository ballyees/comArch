from re import findall
from sys import argv
from os.path import abspath
from os import listdir
from Config import Config
import SimulatorFunc as sf

complieFile = [] if '-f' in argv[1:] else argv[1:]
if not complieFile:
    complieFile = list(filter(lambda file: (".compile" in file), listdir()))

for f in complieFile:
    # initialize register
    reg = [0 for i in range(Config.maxRegs)]
    stack = []
    memory = []
    with open(abspath(f), 'r') as file:
        while True:
            l = file.readline()
            if not l:
                break
            memory.append(sf.splitOpcode(l.strip('\n')))
    sizeOfProgram = len(memory)
    pc = 0
    ie = 0
    sf.printMemory(memory)
    # Simulator
    while True:
        
        if (pc == sizeOfProgram) or (memory[pc][0][0] == '.fill'):
            print('end of program')
            break
        instruction = memory[pc][0][0]
        if instruction == 'noop':
            pc += 1
            continue
        ie += 1
        sf.printState(pc, memory, reg)
        if instruction in sf.FuncRType:
            sf.FuncRType[instruction](reg, memory[pc][0][3], memory[pc][0][1], memory[pc][0][2])
            pc += 1
        elif instruction in sf.FuncIType:
            updatePC = sf.FuncIType[instruction](reg, stack, memory[pc][0][3], memory[pc][0][1], memory[pc][0][2])
            pc += updatePC
        elif instruction == 'halt':
            sf.haltInstruction(ie, pc+1, memory, reg)
            break
        
        # breakpoint()
    print('+===+===+==='*8, end='\n\n')