from re import findall
from sys import argv
from os.path import abspath
from os import listdir
from Config import Config
import SimulatorFunc as sf
from printArt import startSimulalor, endSimulalor

compileFile = [] if '-f' in argv[1:] else argv[1:]
if not compileFile:
    compileFile = list(filter(lambda file: (".compile" in file), listdir()))

for f in compileFile:
    print(f'run in file: {f}')
    startSimulalor()
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
    sf.printItemInMemory(memory)
    sf.printMemory(memory)
    # breakpoint()
    # Simulator
    while True:
        # print(memory[pc])
        instruction = memory[pc][0][0]
        if (pc == sizeOfProgram) or (instruction == '.fill'):
            print('end of program')
            break
        
        if instruction == 'noop':
            pc += 1
            continue
        ie += 1
        sf.printState(pc, memory, reg)
        if instruction in sf.FuncRType:
            sf.FuncRType[instruction](reg, memory[pc][0][3], memory[pc][0][1], memory[pc][0][2])
            pc += 1
        elif instruction in sf.FuncIType:
            updatePC = sf.FuncIType[instruction](reg, memory, stack, memory[pc][0][3], memory[pc][0][1], memory[pc][0][2])
            pc += updatePC
        elif instruction in sf.FuncJType:
            updatePC = sf.FuncJType[instruction](reg, memory[pc][0][1], memory[pc][0][2], pc)
            pc += updatePC
        elif instruction == 'halt':
            pc += 1
            sf.haltInstruction(ie, pc, memory, reg)
            break
        
        # breakpoint()

    # print('+===+===+==='*8, end='\n\n')
    endSimulalor()