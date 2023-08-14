#!/usr/bin/env python
from mar import Interpreter, Lexer, CmdLexer, Parser, InlineInterpreter
from cmd import Cmd
import sys
import os


space = ' ' * 4
commands = []

class Shell(Cmd):
	intro = 'Martha Version 0.0.1 -- Laradespace Inc.\n'
	count = 1
	prompt = f'[{count}]~: '
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.interpreter = InlineInterpreter('')

	def do_EOF(self, line):
		'''Exit the shell'''
		print('\nGoodbye!')
		return True

	def run(self, line):
		tokens, error = CmdLexer().lex_line(line.replace('\t', space))
		if error: return
    
		ast, error = Parser(tokens, line.replace('\t', space)).parse()
		if error: return
	
		self.interpreter.set_text(line.replace('\t', space))
		try:
			result, error = self.interpreter.interpret(ast)
			if error:
				error.show_error()
				error.show_hint()
			else:
				if result:
					if len(result) == 1: print(result.pop())
					else: print(result)
		except Exception as e:
			print(e)
	
	def execute_history(self):
		for cmd in commands: 
			print(cmd)
		
	def execute_clear(self):
		os.system('cls' if os.name == 'nt' else 'clear') 
		
	def default(self, line):
		if line.strip() != '':
			if line.startswith('..'):
				name = line.strip()[2:]
				
				if len(commands) == 0:
					commands.append(line)
				else:
					if line != commands[-1]: commands.append(line)
				method_name = f'execute_{name}'
				try:
					method = getattr(self, method_name)
					return method()
				except Exception as e:
					print(f"command '{name}' not implemented")
					return
			#try: 
			self.run(line)
			#except Exception as e: 
			#	print(e)
		self.count += 1
		self.prompt = f'[{self.count}]~: '
		if len(commands) == 0:
			commands.append(line)
		else:
			if line != commands[-1]: commands.append(line)
	
	def emptyline(self):
		pass

def interpret_file(filename):
	try:
		with open(filename, 'r') as file:
			code = file.read()
	except FileNotFoundError as e:
		print(e)
		print()
		quit()
	lexer = Lexer(code.replace('\t', space))
	tokens, error = lexer.lex()
	
	if error: return

	parser = Parser(tokens, code.replace('\t', space))
	
	ast, error = parser.parse()
	if error: return
	#try:
	interpreter = Interpreter(code.replace('\t', space))
	result, error = interpreter.interpret(ast)
	
	if error: 
		error.show_error()
		error.show_hint()
	#except Exception as e:
	#	print(e)

def main():
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		#try:
		interpret_file(filename)
		#except KeyboardInterrupt:
		#	print('\nGoodbye!')
	else:
		# Start an interactive shell
		try:
			Shell().cmdloop()
		except KeyboardInterrupt:
			print('\nGoodbye!')

if __name__ == '__main__':
	main()
