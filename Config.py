class Config:
    #-------------------------------------------------------------------------------------------------------#
    #                                                  ASSEMBLER                                            #
    #-------------------------------------------------------------------------------------------------------#
    maxRegs = 8
    maxOffsetField = 15
    maxPositiveValue = (1<<maxOffsetField) - 1
    maxNegativeValue = -(1<<maxOffsetField)
    numericAddress = { chr(ord('0') + i): chr(ord('0') + i) for i in range(maxRegs) }
    opcodeIType = {
        'lw': '010',
        'sw': '011',
        'beq': '100',
    }
    opcodeRType = {
        'add': '000',
        'nand': '001',
        }
    opcodeJType = {
        'jalr': '101'
        }
    opcodeOType = {
        'halt': '110',
        'noop': '111',
    }
    opcodes = {**opcodeIType, **opcodeRType, **opcodeJType, **opcodeOType}
    xor32Bit = 0b11111111111111111111111111111111
    xor16Bit = 0b1111111111111111
    MSB7 = '0'*7
    rType15to3 = '0'*13
    LSB22 = '0'*22
    LSB16 = '0'*16
    #------------------------------------------------------------------------------------------------------#
    #                                                  SIMULATOR                                           #
    #------------------------------------------------------------------------------------------------------#
    opcodeITypeBin = dict([(b, i) for i, b in opcodeIType.items()])
    opcodeRTypeBin = dict([(b, i) for i, b in opcodeRType.items()])
    opcodeJTypeBin = dict([(b, i) for i, b in opcodeJType.items()])
    opcodeOTypeBin = dict([(b, i) for i, b in opcodeOType.items()])
    opcodesBin = dict([(b, i) for i, b in opcodes.items()])

    