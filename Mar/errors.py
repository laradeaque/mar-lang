from colorama import Fore
class Error:
	def __init__(self, name, char, position, line_number, text):
		self.name = name
		self.char = char
		self.position = position
		self.text = text
		self.line_number = line_number
		
		self.show_error()
		
	def show_error(self):
		print(self.text.split('\n')[self.line_number])
		space = ' ' * self.position + '^'
		print(space)
		print(self)
			
	def __str__(self):
		return f'\33[1;31m{self.name} at line: {self.line_number + 1}\33[1;0m'

class UnknownChar(Error):
	def __init__(self, name, char, position, line_number, text):
		super().__init__(name, char, position, line_number, text)

class InvalidSyntax(Error):
	def __init__(self, name, char, position, line_number, text):
		super().__init__(name, char, position, line_number, text)

class Syntax_Error(Error):
	def __init__(self, name, char, position, line_number, text):
		super().__init__(name, char, position, line_number, text)
	
class StructuralError:
	def __init__(self):
		pass
	
		
class ParseError(Error):
	def __init__(self, name, token, pos_start, line_number, text, hint):
		super().__init__(name, token, pos_start, line_number, text)
		self.show_hint(hint)
	
	def show_hint(self, hint):
		print(hint)

	def show_error(self):
		print(self.text.split('\n')[self.line_number])
		#space = ' ' * self.position + '^'# + '~' * (len(self.char) - 2) + ('^' if len(self.char) > 1 else '')
		#print(space)
		print(self)
	
class Panic:
	def __init__(self, line_number):
		self.show_error(line_number)
		
	def show_error(self, line_number):
		print(f'Parse Error from line {line_number + 1}')
		print('\33[1;31mCould not parse the remainder\33[1;0m')
		quit()
		
class ExecutionError:
	def __init__(self, name, hint, line_number=0, text='',):
		self.name = name
		self.line_number = line_number
		self.text = text
		self.hint = hint
		#self.show_error()
		#self.show_hint(hint)
	
	def show_hint(self):
		print(self.hint)
	
	def show_error(self):
		#line = self.text.split('\n')[self.line_number]
		#print(f"---->   {line}")
		#print(space)
		print(self)
		
	def __str__(self):
		return f'\33[1;31m{self.name}\33[1;0m'
