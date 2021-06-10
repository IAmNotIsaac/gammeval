from gammatypes import *


class Opcode:
	def __init__(self, args, interpreter):
		pass
	

	def expect(self, argument, gammatypes):
		passed = False
		for i in gammatypes:
			if isinstance(argument, gammatypes):
				passed = True
		
		if passed:
			return argument
		else:
			return argument
			# Error handling here later!


class Set(Opcode):
	def __init__(self, args, interpreter):
		self.value_a = self.expect(args[0], ())