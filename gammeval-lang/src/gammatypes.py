from typing import final


class Integer:
	def __init__(self, value):
		self.value = min(max(int(value), -255), 255)
	

	def __repr__(self):
		return f"{self.value}"
	

	def __str__(self):
		return str(self.value)
	

	def op_add(self, right):
		return Integer(self.value + right.value)
	

	def op_sub(self, right):
		return Integer(self.value - right.value)
	

	def op_mul(self, right):
		return Integer(self.value * right.value)
	

	def op_div(self, right):
		return Integer(int(self.value / right.value))
	

	def comp_eql(self, right):
		return True if self.value == right.value else False
	

	def comp_nql(self, right):
		return True if self.value != right.value else False
	

	def comp_gtr(self, right):
		return True if self.value > right.value else False
	
	
	def comp_lsr(self, right):
		return True if self.value < right.value else False



class String:
	def __init__(self, value):
		self.value = value
	
	
	def __repr__(self):
		return f"{self.value}"
	

	def __str__(self):
		return self.value


class RegisterReference:
	def __init__(self, number):
		self.number = number
	
	
	def __repr__(self):
		return f"#{self.number}"


class LabelReference:
	def __init__(self, name):
		self.name = name
	

	def __repr__(self):
		return f"?{self.name}"


class Opcode:
	def __init__(self, operation, args):
		self.operation = operation
		self.args = args
	
	
	def __repr__(self):
		return f"!{self.operation}{self.args}"


class ExternalCode:
	def __init__(self, language, code):
		self.language = language
		self.code = code
	

	def __repr__(self):
		return f"{self.language} code: {self.code}"
	

	def __str__(self):
		return self.code