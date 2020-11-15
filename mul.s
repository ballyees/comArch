 lw 0 2 mcand
 lw 0 3 mpiler
 lw 0 4 pos
 lw 0 5 and
 nand 3 5 5
 nand 5 5 5
 beq 0 5 2
 nand 3 3 3
 add 3 4 3
mul add 1 2 1
 add 6 4 6
 beq 6 3 1
 beq 0 0 -4
 beq 0 5 2
 nand 1 1 1
 add 1 4 1
 noop
 halt
addrM .fill mul
mcand .fill 10
mpiler .fill -5
and .fill -32768
pos .fill 1