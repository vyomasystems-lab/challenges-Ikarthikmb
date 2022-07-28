# Generating Hex bits of the instructions from binary instructions

import random 

file1 = open('instr.txt', 'r')
lines = file1.readlines()

fp = open('inst_hex.txt', 'w')

for line in lines:
	line = hex(int("0b" + line, 2))
	print(line[2:], type(line))
	fp.writelines(line + "\n")

