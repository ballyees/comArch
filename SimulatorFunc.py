from Config import Config

#------------------------------------------------------------------------------------------------------#
#                                                  CONVERT                                             #
#------------------------------------------------------------------------------------------------------#

def cvtTwoCsomplement(value: str) -> int:
    if value[0] == "1":
        val = -((int(value, base=2) ^ (Config.xor32Bit if len(value) == 32 else Config.xor16Bit)) + 1)
    else: 
        val = int(value[1:], base=2)
    return val

def isFillFormat(splitAddress: list) -> bool:
    if splitAddress[0] != Config.MSB7:
        return True

def fillFormat(address: str, addr: list) -> None:
    addr.append('.fill')
    addr.append(cvtTwoCsomplement(address))

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
    addr.append(cvtTwoCsomplement(splitAddress[2][6:]))

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
    splitAddr = []
    # MSB 7 bit
    splitAddr.append(address[:7])
    # opcode
    splitAddr.append(address[7:10]) 
    splitAddr.append(address[10:])
    if isFillFormat(splitAddr):
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
    return addr

#------------------------------------------------------------------------------------------------------#
#                                                  SIMULATOR                                           #
#------------------------------------------------------------------------------------------------------#

def isAssignRegister0():
    return True