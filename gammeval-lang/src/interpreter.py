import os

from gammatypes import *


class Interpreter:
	def __init__(self, program, config, registers, jump_history):
		self.program = program
		self.config = config

		self.registers = registers
		self.jump_history = jump_history

		self.current_file = list(program.keys())[0]
		self.current_program = program[self.current_file]
		self.index = 0


	def expect_type(self, comp, gammatype):
		for t in gammatype:
			if isinstance(comp, t):
				return comp
		print(f"Expected {gammatype} got {type(comp)}")
		self.opcode_end(None)
	

	def as_integer(self, thing):
		if isinstance(thing, Integer):
			return thing
		elif isinstance(thing, RegisterReference):
			return self.registers.get(thing)
	

	def as_string(self, thing):
		if isinstance(thing, String):
			return thing
		elif isinstance(thing, Integer):
			return String(str(thing))
		elif isinstance(thing, RegisterReference):
			return String(str(self.registers.get(thing)))
		elif isinstance(thing, ExternalCode):
			return String(str(thing.code))
	

	def run(self):
		while self.index < len(self.current_program["source"]):
			operation = self.current_program["source"][self.index]
			op_func = getattr(self, f"opcode_{operation.operation.lower()}")

			op_func(operation.args)

			self.index += 1
	

	def opcode_nop(self, args):
		pass


	def opcode_out(self, args):
		final_out = ""

		for i in range(len(args)):
			out = self.expect_type(args[i], [RegisterReference, Integer, String, ExternalCode])

			out = self.as_string(out)
			final_out += f"{out} "
		
		print(final_out.strip())


	def opcode_set(self, args):
		regf = self.expect_type(args[0], [RegisterReference])
		value = self.expect_type(args[1], [RegisterReference, Integer])

		value = self.as_integer(value)

		self.registers.set(regf, value)


	def opcode_add(self, args):
		regf = self.expect_type(args[0], [RegisterReference])
		value = self.expect_type(args[1], [RegisterReference, Integer])

		value = self.as_integer(value)

		self.registers.set(regf, self.registers.get(regf).op_add(value))
		self.registers.set(regf, value)


	def opcode_sub(self, args):
		regf = self.expect_type(args[0], [RegisterReference])
		value = self.expect_type(args[1], [RegisterReference, Integer])

		value = self.as_integer(value)

		self.registers.set(regf, self.registers.get(regf).op_sub(value))
		self.registers.set(regf, value)


	def opcode_mul(self, args):
		regf = self.expect_type(args[0], [RegisterReference])
		value = self.expect_type(args[1], [RegisterReference, Integer])

		value = self.as_integer(value)

		self.registers.set(regf, self.registers.get(regf).op_mul(value))
		self.registers.set(regf, value)


	def opcode_div(self, args):
		regf = self.expect_type(args[0], [RegisterReference])
		value = self.expect_type(args[1], [RegisterReference, Integer])

		value = self.as_integer(value)

		self.registers.set(regf, self.registers.get(regf).op_div(value))
	

	def opcode_jump(self, args):
		labelf = self.expect_type(args[0], [LabelReference])

		self.jump_history.push(self.current_file, Integer(self.index))
		self.index = self.current_program["labels"].get(labelf).value
	

	def opcode_jumpo(self, args):
		offset = self.expect_type(args[0], [Integer])

		self.jump_history.push(self.current_file, Integer(self.index))
		self.index += offset.value - 1
	

	def opcode_jumpf(self, args):
		file = self.expect_type(args[0], [String])
		
		self.jump_history.push(self.current_file, Integer(self.index))
		
		self.current_file = str(file)
		self.current_program = self.program[str(file)]
		self.index = -1
	

	def opcode_jumpfl(self, args):
		file = self.expect_type(args[0], [String])
		labelf = self.expect_type(args[1], [LabelReference])
		
		self.jump_history.push(self.current_file, Integer(self.index))
		
		self.current_file = str(file)
		self.current_program = self.program[str(file)]

		self.index = self.current_program["labels"].get(labelf).value - 1
	

	def opcode_query(self, args):
		left = self.expect_type(args[0], [RegisterReference, Integer])
		right = self.expect_type(args[1], [RegisterReference, Integer])
		opcode = self.expect_type(args[2], [String])

		left = self.as_integer(left)
		right = self.as_integer(right)

		if left.comp_eql(right):
			op_func = getattr(self, f"opcode_{opcode.value.lower()}")
			op_func(args[3:])
	

	def opcode_queryn(self, args):
		pass
	

	def opcode_queryg(self, args):
		pass
	

	def opcode_queryl(self, args):
		pass
	

	def opcode_python(self, args):
		python_code = ""

		for arg in args:
			python_code += str(self.expect_type(arg, [String]))
		
		python_code = python_code.replace("\"", "'")

		exec = f"python -c {python_code}"
		os.system(exec)
	

	def opcode_pythonf(self, args):
		python_file = self.expect_type(args[0], [String])

		exec = f"python {self.config['program']['hierarchy'][str(python_file)]}"
		os.system(exec)


	def opcode_end(self, args):
		self.index = len(self.current_program["source"])
	

	def opcode_ret(self, args):
		if len(self.jump_history.jumps) > 0:
			jump = self.jump_history.pull()
			self.current_file = str(jump[0])
			self.current_program = self.program[self.current_file]
			self.index = jump[1].value