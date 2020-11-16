from re import findall
from sys import argv
from os.path import abspath
from os import listdir
from Config import Config
import AssemblerFunc as af
from printArt import startAssembler, endAssembler

sFile = [] if '-f' in argv[1:] else argv[1:]
if not sFile:
    sFile = list(filter(lambda file: (".s" in file), listdir()))

for f in sFile:
    print(f'complie in file {f}')
    startAssembler()
    with open(abspath(f), 'r') as file:
        # init value
        symbolicAddress = {}
        symbolicAddressLabel = {}
        lines = [af.addFillVal(symbolicAddress, symbolicAddressLabel, fields, i) for i, fields in enumerate(file.readlines())]
        address = list(range(len(lines)))
        # convert to binary
        for i, l in enumerate(lines):
            fields = af.cvtSymbolicAddress2RegisterNumber(l.copy(), symbolicAddress, symbolicAddressLabel, i)
            lines[i] = fields.copy()
            if fields[1] in Config.opcodeIType:
                address[i] = af.iTypeFormatter(fields, i)
            elif fields[1] in Config.opcodeRType:
                address[i] = af.rTypeFormatter(fields)
            elif fields[1] in Config.opcodeJType:
                address[i] = af.jTypeFormatter(fields)
            elif fields[1] in Config.opcodeOType:
                address[i] = af.oTypeFormatter(fields)
            elif fields[1] == '.fill':
                address[i] = af.fillInstructionFormatter(fields, i)
            else:
                raise AttributeError(f'{fields[1]} not instruction')
        for i, a in enumerate(address):
            if lines[i][1] == '.fill':
                dec = af.twoComplement2Integer(a)
                addr = int(a, base=2)
                print(f'(address {i}): {dec} (hex {addr:#x})')
            else:
                dec = int(a, base=2)
                print(f'(address {i}): {dec} (hex {dec:#08x})')
        af.writeFile(f, address)
    endAssembler()
