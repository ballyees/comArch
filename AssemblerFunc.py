from Config import Config

def writeLine(filename: str, line: str) -> list:
    with open(filename, 'a+') as file:
        file.write(line+'\n')

def writeFile(fileDotS: str, address: list) -> None:
    filename = f'{fileDotS.split(".")[0]}.compile'
    with open(filename, 'w') as file:
        for addr in address:
            file.write(addr + '\n')

def writeFileNoFill(fileDotS: str, address: list, lines: list) -> None:
    filename = f'{fileDotS.split(".")[0]}.compile'
    with open(filename, 'w') as file:
        for addr, line in zip(address, lines):
            if '.fill' not in line:
                file.write(addr + '\n')

def addFillVal(SA: dict, fields: list, index: int) -> list:
    fields = fields.strip('\n').split(' ')
    if len(fields) == 3 and fields[1] == '.fill':
        SA[fields[0]] = SA.get(fields[2], fields[2])
    elif fields[0]:
        SA[fields[0]] = index
    return fields

def cvtSymbolicAddress2RegisterNumber(feilds: list, SA: dict, index: int) -> list:
    for i, f in enumerate(feilds[2:], start=2):
        if Config.opcodes.get(feilds[1], None):
            if len(feilds) - 1 == i and Config.opcodeIType.get(feilds[1], None):
                if SA.get(f, None):
                    if int(SA[f]) <= 0:
                        feilds[i] = SA[f]
                    else:
                        feilds[i] = f'{int(SA[f])-index}'
                        # feilds[i] = f'{int(SA[f])-index}' if index > int(SA[f]) and int(SA[f]) >= 0 else SA[f]
                else:
                    try:
                        feilds[i] = int(f)
                    except:
                        raise ValueError(f"Line {index}: can't convert symbolic address or numeric address")
            elif SA.get(f, None):
                feilds[i] = SA[f]
            elif not Config.numericAddress.get(f, None):
                raise ValueError(f"Line {index}: can't convert symbolic address or numeric address")
        elif feilds[1] == '.fill':
            if SA.get(f, None):
                feilds[i] = SA[f]
            else:
                try:
                    int(feilds[i])
                except ValueError:
                    raise ValueError(f"Line {index}: can't convert symbolic address")
    return feilds

def isNegativeValue(value: int) -> bool:
    return value < 0

def convert2TwoComplement(val: str, index: int, fill: bool=False) -> str:
    val = int(val)
    if fill:
        if isNegativeValue(val):
            val = (val ^ Config.xor32Bit) + 1
        val = f'{val:032b}'.replace('-', '')
        return val
    else:
        if Config.maxNegativeValue <= val <= Config.maxPositiveValue:
            if isNegativeValue(val):
                val = (val ^ Config.xor16Bit) + 1
            val = f'{val:016b}'.replace('-', '')
            
            return val
        else:
            raise ValueError(f'Line {index}:Value must in range [{Config.maxNegativeValue}, {Config.maxPositiveValue}]')
            

def rTypeFormatter(fields: list) -> str:
    # Bits 24-22 opcode
    # Bits 21-19 reg A (rs)
    # Bits 18-16 res B (rt)
    # Bits 15-3 ไม่ใช้ (ควรตั้งไว้ที่ 0)
    # Bits 2-0 destReg (rd)
    opcode = Config.opcodeRType[fields[1]]
    regA = f'{int(fields[2]):03b}'
    regB = f'{int(fields[3]):03b}'
    destReg = f'{int(fields[4]):03b}'
    return f'{Config.MSB7}{opcode}{regA}{regB}{Config.rType15to3}{destReg}'

def iTypeFormatter(fields: list, index: int) -> str:
    # Bits 24-22 opcode
    # Bits 21-19 reg A (rs)
    # Bits 18-16 reg B (rt)
    # Bits 15-0 offsetField (เลข16-bit และเป็น 2’s complement โดยอยู่ในช่วง –32768 ถึง 32767)
    opcode = Config.opcodeIType[fields[1]]
    regA = f'{int(fields[2]):03b}'
    regB = f'{int(fields[3]):03b}'
    offsetField = convert2TwoComplement(fields[4], index)
    return f'{Config.MSB7}{opcode}{regA}{regB}{offsetField}'

def jTypeFormatter(fields: list) -> str:
    # Bits 24-22 opcode
    # Bits 21-19 reg A (rs)
    # Bits 18-16 reg B (rd)
    # Bits 15-0 ไม่ใช้ (ควรตั้งไว้ที่ 0) 
    opcode = Config.opcodeJType[fields[1]]
    regA = f'{int(fields[2]):03b}'
    regB = f'{int(fields[3]):03b}'
    return f'{Config.MSB7}{opcode}{regA}{regB}{Config.LSB16}'

def oTypeFormatter(fields: list) -> str:
    # Bits 24-22 opcode
    # Bits 21-0 ไม่ใช้ (ควรตั้งไว้ที่ 0)
    opcode = Config.opcodeOType[fields[1]]
    return f'{Config.MSB7}{opcode}{Config.LSB22}'

def fillInstructionFormatter(fields: list, index: int) -> str:
    return convert2TwoComplement(fields[2], index, True)