 lw 0 2 input //asdss
 lw 0 3 and
 lw 0 4 pos1
 nand 3 2 3
 nand 3 3 3
 beq 0 3 end
cvt nand 2 2 2
 add 2 4 2
end noop
 halt
input .fill -1231
and .fill -32768
pos1 .fill 1
