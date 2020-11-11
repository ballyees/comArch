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
    reg = [i for i in range(Config.maxRegs)]
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
    sf.printMemory(memory)
    # Simulator
    while True:
        if pc == sizeOfProgram:
            print('end of program')
            break
        pc += 1
    print('+===+===+==='*8, end='\n\n')