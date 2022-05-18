#!/usr/bin/env python3

import os
import sys
import re
from optparse import OptionParser

def get_arguments():
	parser = OptionParser()

	parser.add_option('-a', "--arch", dest = "arch", default = "elf64", 
			help = "specify architecture (default = elf64)")

	parser.add_option('-n', "--no-interactive", dest = "interactive", default = True, action = "store_false",
			help = "do not print the instructions interactively")

	return parser.parse_args()

def get_obj_output(inp, arch):
	in_file = "/tmp/pybin.s"
	obj_file = "/tmp/pybin.o"

	with open(in_file, "w") as f:
		f.write(inp)

	os.system("nasm -f" + arch + ' ' + in_file)

	if os.path.exists(obj_file):
		pipe = os.popen("objdump -M intel -D " + obj_file)
		return pipe.read()

def extract_instruction(inp):
	begin_heading = "<.text>:\n"
	start_pos = inp.find(begin_heading)

	if start_pos == -1:
		return

	start_pos += len(begin_heading)
	inp = inp[start_pos:]
	ret = str()

	for m in re.finditer("([a-fA-F0-9]{2}( {1,2}))+(?!\n)", inp):
		ret += m.group(0)

	return ret

def print_instructions_helper(instructions, prefix, seperator):

	for i in range(0, len(instructions) - 1, 3):
		print(prefix, instructions[i], instructions[i + 1], sep = "", end = seperator) 
	
	print()
	print('-' * 50)

def print_c_style(instructions):
	print("{ ", end = "")

	for i in range(0, len(instructions) - 1, 3):
		c = '' if i == len(instructions) - 3 else ','
		print("'\\x", instructions[i], instructions[i + 1], '\'' + c + ' ' , sep = '', end = '')

	print('}')

def print_instructions(instructions):
	instructions = instructions.replace("  ", ' ')

	print("-" * 50)
	print(instructions)
	print("-" * 50)

	print_instructions_helper(instructions, "0x", '')
	print_instructions_helper(instructions, "\\x", '')
	print_c_style(instructions)

######

(options, args) = get_arguments()
combined_res = str()

for line in sys.stdin:
	obj_out = get_obj_output(line, options.arch)

	if obj_out == None:
		continue

	ins = extract_instruction(obj_out)

	if ins != None:
		combined_res += ins

		if options.interactive:
			print_instructions(ins)
			print()

print_instructions(combined_res)

try:
	os.remove("/tmp/pybin.o")
	os.remove("/tmp/pybin.s")
except:
	pass
