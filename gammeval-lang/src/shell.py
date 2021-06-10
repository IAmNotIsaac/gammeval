import json

from lexer import *
from interpreter import *
from globals import *



config = json.load(open("config.json"))
hierarchy = config["program"]["hierarchy"]

source = hierarchy[list(hierarchy.keys())[0]]


registers = Registers()
jump_history = JumpHistory()


program = {}


for file in hierarchy:
	path = hierarchy[file]

	raw_source = open(path).read()
	
	labels = Labels(raw_source)
	lexer = Lexer(raw_source, labels)

	source = lexer.make_opcodes()

	program[file] = {
		"source": source,
		"labels": labels
	}


interpretera = Interpreter(program, config, registers, jump_history)
interpretera.run()