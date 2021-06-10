from gammatypes import *


class Lexer:
	def __init__(self, source, labels):
		self.source = source
		self.labels = labels
		

	def make_opcodes(self):
		operations = self.source.split("\n")
		program = []
		line = 0

		for raw_operation in operations:
			raw_operation = raw_operation.strip()
			if raw_operation in " \t\n" or raw_operation[0] == "/": continue
			arguments = raw_operation.split(" ")
			opcode = arguments[0]
			arguments.pop(0)
			
			arguments = self.make_types(arguments)

			if opcode[-1] == ":":
				#self.labels.set(LabelReference(opcode[:-1]), Integer(line))
				opcode = Opcode("NOP", None)
			else:
				opcode = Opcode(opcode, arguments)
			program.append(opcode)
			
			line += 1
		
		return program


	def make_types(self, arguments):
		res = []
		
		for argument in arguments:
			if argument[0] == "/": break
			elif argument[0] == "#": res.append(self.make_registerref(argument))
			elif argument[0] == "?": res.append(self.make_labelref(argument))
			elif argument[0] in "-1234567890": res.append(self.make_number(argument))
			elif argument[0].lower() in "abcdefghijklmnopqrstuvwxyz": res.append(self.make_string(argument))
			elif argument[0] == "$": res.append(self.make_external_code(argument))
			else: res.append(self.make_string(argument)) # Error handle here later
		
		return res


	def make_registerref(self, argument):
		return RegisterReference(argument[1:])
	

	def make_labelref(self, argument):
		return LabelReference(argument[1:])


	def make_number(self, argument):
		return Integer(argument)


	def make_string(self, argument):
		return String(argument)
	

	def make_external_code(self, argument):
		return ExternalCode("python", argument[1:])