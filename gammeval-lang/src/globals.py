from gammatypes import *


class Registers:
	def __init__(self):
		self.registers = {}

		for a in range(10):
			for b in range(10):
				for c in range(10):
					for d in range(10):
						self.registers[f"{d}{c}{b}{a}"] = Integer(0)


	def set(self, register, value):
		self.registers[str(register.number)] = value
	

	def get(self, register):
		return self.registers[str(register.number)]


class Labels:
	def __init__(self, source):
		self.labels = {}

		index = 0
		for line in source.split("\n"):
			if line.strip() in " \n\t": continue 
			if len(line.split(" ")) == 1:
				if line[-1] == ":":
					self.labels[line[:-1]] = Integer(index)
			index += 1
	

	def set(self, label, line):
		self.labels[label.name] = line
	

	def get(self, label):
		return self.labels[label.name]


class JumpHistory:
	def __init__(self):
		self.jumps = []
	

	def push(self, file, line):
		self.jumps.append((file, line))
	

	def pull(self):
		res = self.jumps[-1]
		self.jumps.pop()
		return res
