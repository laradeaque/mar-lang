#!/usr/bin/env python
from mar import Interpreter, Parser, Lexer
import sys

def interpret_file(filename):
	try:
		with open(filename, 'r') as file:
			code = file.read()
	except FileNotFoundError as e:
		print(e)
		print()
		quit()
	lexer = Lexer(code.replace('\t', space))
	tokens = lexer.lex()
	parser = Parser(tokens)
	ast = parser.parse()
	try:
		interpreter = Interpreter()
		interpreter.interpret(ast)
	except Exception as e:
		print(e)

def main():
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		try:
			interpret_file(filename)
		except KeyboardInterrupt:
			print('\nGoodbye!')
	else:
		print('Mar Version 0.0.1 -- Laradespace\n')
		print('\nI-Shell coming soon...')

if __name__ == '__main__':
	main()
