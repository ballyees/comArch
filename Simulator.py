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
    reg = [[0].copy() for i in range(8)]
    stack = []
    lines = []
    with open(abspath(f), 'r') as file:
        while True:
            l = file.readline()
            if not l:
                break
            lines.append(sf.splitOpcode(l.strip('\n')))
    sizeOfProgram = len(lines)
    index = 0
    while True:
        if index == sizeOfProgram:
            print('end of program')
            break
        index += 1
    print('+===+===+==='*8, end='\n\n')