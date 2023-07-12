from pathlib import Path
import re
import os

DIGITS = '0123456789'
# Token types
ID = 'ID'
NUM = 'NUM'
STR = 'STR'
BOOL = 'BOOL'
NULL = 'NULL'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'
LCURLY = 'LCURLY'
RCURLY = 'RCURLY'
COMMA = 'COMMA'
NEGATE = 'NEGATE'
MODULUS = 'MODULUS'
COLON = 'COLON'
SEMI = 'SEMI'
DOT = 'DOT'
QUESTION = 'QUESTION'
PLUS = 'PLUS'
MINUS = 'MINUS'
ASTERISK = 'ASTERISK'
CARET = 'CARET'
SLASH = 'SLASH'
LT = 'LT'
GT = 'GT'
LTE = 'LTE'
GTE = 'GTE'
EQ = 'EQ'
NE = 'NE'
AND = 'AND'
OR = 'OR'
ASSIGN = 'ASSIGN'
EOL = 'EOL'
EOF = 'EOF'
KEYWORD = 'KEYWORD'
KEYWORDS = (
	'func',
	'use',
	'from',
	'as',
	'for',
	'while',
	'class',
	'parent',
	'if',
	'elif',
	'else',
	'True',
	'False',
	'None',
	'return',
	'break',
	'continue',
	'let',
	'and',
	'or',
)
BIN_OPS = (
	'+',
	'-', 
	'*', 
	'^',
	'/', 
	'%', 
	'>', 
	'<', 
	'==', 
	'>=', 
	'<=',
	'!=',
)
BASE_DIR = Path(__file__).resolve().parent
LIBRARY_PATH = os.path.join(BASE_DIR, 'lib/')
PATHSPLIT = '/'


INBUILT_FUNCTION = {
	'print': lambda x: print(''.join(converter(x))),
	'int': lambda x: to_int(x),
	'readline': lambda x: input(to_str(x)),
	'sysprint': lambda x: systemprint(x),
	'length': lambda x: len(*x),
	'set': lambda x: assign(*x)
}

converter = lambda x: to_str(x)
def assign(l, key, value):
	l[key] = value

def systemprint(x, index = 0):
	if x:
		prout = x[0]
		print(prout)
	else:
		print(x)
		return

def to_str(expression) -> list:
	expr_str = []
	for term in expression:
		if type(term) is float or type(term) is str or type(term) is int: 
			expr_str.append(str(term))
		elif type(term) is list:
			expr_str.append(str(handle_list(term)))
		elif type(term) is tuple:
			expr_str.append(str(handle_tuple(term)))
		else: expr_str.append(str(term))
	return expr_str

def to_int(x):
	if len(x) > 1:
		return [int(num) for num in x]
	else:
		return int(x[0])
	
def handle_list(expression):
	list_str = []
	
	for term in expression:
		if type(term) is float or type(term) is str or type(term) is int: 
			list_str.append(term)
		elif type(term) is list:
			list_str.append(handle_list(term))
		elif type(term) is tuple:
			list_str.append(handle_tuple(term))
	return list_str
	
def handle_tuple(term):
	if term[0] == 'String':
		return f"{term[1]}"
	else:
		return term[1]
	
class Token:
	def __init__(self, type, value):
		self.type = type
		self.value = value

	def __repr__(self):
		return f'Token({self.type}, {self.value})'
	
	def __str__(self):
		return f'Token({self.type}, {self.value})'

class Lexer:
	def __init__(self, text):
		self.text = text
		self.pos = 0
		self.line_number = 0

	def advance(self):
		self.pos += 1
		self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
	
	def error(self, message):
		print(f'Error at line {self.line_number + 1}')
		print(f'{message}')
		quit()

	def lex(self):
		lines = self.text.split("\n")
		tokens = []
		for line in lines:
			self.line = line
			self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
			toks = self.get_tokens()
			self.pos = 0
			self.line_number += 1
			tokens.extend(toks)
			tokens.append(Token(EOL, '\\n'))

		tokens.append(Token(EOF, None))
		return tokens

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def skip_comment(self):
		if self.current_char == '#':
			while self.current_char is not None and self.current_char != '\n':
				self.advance()

	def peek(self):
		peek_pos = self.pos + 1
		return self.line[peek_pos] if peek_pos < len(self.line) else None

	def get_identifier(self):
		result = ''
		while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
			result += self.current_char
			self.advance()
		
		return result

	def get_number(self):
		'''
		12.343
		'''
		num_str = ''
		dot_count = 0

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.advance()
		
		if dot_count == 0:
			return int(num_str)
		else:
			return float(num_str)

	def get_string(self):
		string = ''
		escape_character = False
		used = self.current_char
		self.advance()

		escape_characters = {
			'n': '\n',
			't': '\t'
		}

		while self.current_char != None and (self.current_char != used or escape_character):
			if escape_character:
				string += escape_characters.get(self.current_char, self.current_char)
			else:
				if self.current_char == '\\':
					escape_character = True
				else:
					string += self.current_char
			self.advance()
			escape_character = False
		
		self.advance()
		return string

	def get_tokens(self):
		tokens = []
		while self.current_char is not None:
			if self.current_char.isspace():
				self.skip_whitespace()
				continue
			elif self.current_char == '#':
				self.skip_comment()
				continue
			elif self.current_char.isalpha() or self.current_char == '_':
				value = self.get_identifier()
				if value in KEYWORDS:
					tokens.append(Token(KEYWORD, value))
				else:
					tokens.append(Token(ID, value))
			elif self.current_char.isdigit():
				tokens.append(Token(NUM, self.get_number()))
			elif self.current_char == '"' or self.current_char == "'":
				tokens.append(Token(STR, self.get_string()))
			elif self.current_char == '(':
				tokens.append(Token(LPAREN, '('))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(RPAREN, ')'))
				self.advance()
			elif self.current_char == ',':
				tokens.append(Token(COMMA, ','))
				self.advance()
			elif self.current_char == ':':
				tokens.append(Token(COLON, ':'))
				self.advance()
			elif self.current_char == ';':
				tokens.append(Token(SEMI, ';'))
				self.advance()
			elif self.current_char == '>':
				if self.peek() == '=':
					tokens.append(Token(GTE, '>='))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(GT, '>'))
					self.advance()
			elif self.current_char == '<':
				if self.peek() == '=':
					tokens.append(Token(LTE, '<='))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(LT, '<'))
					self.advance()
			elif self.current_char == '[':
				tokens.append(Token(LBRACKET, '['))
				self.advance()
			elif self.current_char == ']':
				tokens.append(Token(RBRACKET, ']'))
				self.advance()
			elif self.current_char == '{':
				tokens.append(Token(LCURLY, '{'))
				self.advance()
			elif self.current_char == '}':
				tokens.append(Token(RCURLY, '}'))
				self.advance()
			elif self.current_char == '.':
				tokens.append(Token(DOT, '.'))
				self.advance()
			elif self.current_char == '+':
				tokens.append(Token(PLUS, '+'))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(MINUS, '-'))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(ASTERISK, '*'))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(CARET, '^'))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(SLASH, '/'))
				self.advance()
			elif self.current_char == '%':
				tokens.append(Token(MODULUS, '%'))
				self.advance()
			elif self.current_char == '=':
				if self.peek() == '=':
					tokens.append(Token(EQ, '=='))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(ASSIGN, '='))
					self.advance()
			elif self.current_char == '!':
				if self.peek() == '=':
					tokens.append(Token(NE, '!='))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(NEGATE, '!'))
					self.advance()
			elif self.current_char == '&' and self.peek() == '&':
				tokens.append(Token(AND, '&&'))
				self.advance()
				self.advance()
			elif self.current_char == '|' and self.peek() == '|':
				tokens.append(Token(OR, '||'))
				self.advance()
				self.advance()
			else:
				UnknownChar("Unknown Character", self.current_char, self.pos, self.line_number, self.text)
				print(f"unknown char: {self.current_char}")
				self.advance()
		return tokens

class CmdLexer(Lexer):
	def __init__(self):
		super().__init__('')
		
	def lex_line(self, line):
		tokens = []
		self.line = line
		self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
		toks = self.get_tokens()
		tokens = [toks, Token(EOL, '\\n'), Token(EOF, None)]
		return tokens

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.line_number = 0
		self.tok_idx = 0
		self.current_token = None
		self.advance()
		
	def advance(self):
		self.current_token = self.tokens[self.tok_idx]
		self.tok_idx += 1
		if self.current_token.type == EOL:
			self.line_number += 1
			self.advance()
		
	def reverse(self, times):
		index = self.tok_idx  - times
		if index < 0: return None
		else: return self.tokens[index]
	
	def error(self, token_type):
		# Called for minor parsing errors
		print(f'Invalid Token Error at line {self.line_number + 1}')
		print(f'Expected Token Type: {token_type} but found Token Type: {self.current_token.type}')
		print(f'Token Value: {self.current_token.value}')
		quit()
		
	def import_error(self):
		print(f'Import Error!')
		print(f'Expected the keyword "use" but found {self.current_token.value}')
		quit()
		
	def stop(self):
		# Called on major parsing error
		print(f'Parse Error from line {self.line_number + 1}')
		print('Could not parse the remainder')
		quit()
	
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.advance()
		else:
			self.error(token_type)
		
	def parse(self):
		result = self.program()
		
		if self.current_token.type != EOF:
			self.stop()
		return result
	
	def program(self):
		'''
		program 	-> statement program 
		'''
		statements = []
		
		while self.current_token.type != EOF:
			statements.append(self.statement())
		
		return statements
	
	def statement(self):
		'''
		statement   ->  function_declaration
					|   class_declaration
					|   use_statement
					| 	if_statement
					| 	return_statement
					|	while_loop
					| 	for_loop
					| 	print_statement
					| 	expression_statement
		'''
		if self.current_token.type == KEYWORD:
			if self.current_token.value == 'func':
				return self.function_declaration()
			if self.current_token.value == 'parent':
				return self.parent_initialisation()
			if self.current_token.value == 'return':
				return self.return_statement()
			if self.current_token.value == 'while':
				return self.while_loop()
			if self.current_token.value == 'class':
				return self.class_declaration()
			if self.current_token.value == 'for':
				return self.for_loop()
			if self.current_token.value == 'let':
				return self.var_assign()
			if self.current_token.value == 'if':
				return self.if_statement()
			if self.current_token.value == 'from' or self.current_token.value == 'use':
				return self.from_statement()
			else:
				return self.expression_statement()
		else:
			return self.expression_statement()
	
	def function_declaration(self):
		'''
		function	-> "function" id_statement parameters block
		'''
		self.eat(KEYWORD)
		
		function_name = self.id_statement()
		
		input_parameters, output_parameters = self.parameters()
		
		block = self.block()
		
		return ('function', function_name, (input_parameters, output_parameters), block)
	
	def parent_initialisation(self):
		'''
		parent_initialisation   -> "parent" id_statement function_call
		'''
		self.eat(KEYWORD)
		
		parent_name = self.id_statement()
		
		parent_args = self.arguments()
		
		return ('parent', parent_name, parent_args)
	
	def class_declaration(self):
		'''
		class	-> "class" id_statement block
		'''
		self.eat(KEYWORD)
		
		class_name = self.id_statement()
		
		parent_classes = self.inherit_class() if self.current_token.type == 'LPAREN' else []
		
		block = self.block()
		
		return ('class', class_name, block, parent_classes)
	
	def from_statement(self):
		'''
		use_statement  -> "from" id_statement "use" module_names "as" id_statement
					   -> "use" module_names "as" id_statement
		'''
		if self.current_token.value == "from":
			self.eat(KEYWORD)
			parent_module = self.id_statement()
			if self.current_token.value != 'use': self.import_error()
			self.eat(KEYWORD)
			module_names = self.module_names()
		else:
			self.eat(KEYWORD)
			parent_module =  None
			module_names = self.module_names()
		
		alias = []
		if self.current_token.type == KEYWORD and self.current_token.value == 'as':
			self.eat(KEYWORD)
			alias.extend(self.module_names())
		
		return ('from', parent_module, module_names, alias)
		
	def module_names(self):
		paren = False
		if self.current_token.type == LPAREN:
			self.eat(LPAREN)
			paren = True
		names = [self.id_statement()]
		
		while self.current_token.type == 'COMMA':
			self.eat(COMMA)
			names.append(self.id_statement())
		
		if paren: self.eat(RPAREN)
		
		return names
		
	def if_statement(self):
		'''
		if_statement  -> "if" "(" expression ")" block elif_clauses else_clause
		elif_clauses  -> "elif" "(" expression ")" block elif_clauses | ε
		else_clause   -> "else" block | ε
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		condition = self.expression()
		self.eat(RPAREN)
		
		if_block = self.block()
		elif_clauses = []
		else_clause = None

		while self.current_token.value == 'elif':
			self.eat(KEYWORD)
			
			self.eat(LPAREN)
			elif_condition = self.expression()
			self.eat(RPAREN)
			
			elif_block = self.block()
			elif_clauses.append((elif_condition, elif_block))

		if self.current_token.value == 'else':
			self.eat(KEYWORD)
			else_block = self.block()
			else_clause = else_block

		return ('if', condition, if_block, elif_clauses, else_clause)
	
	def return_statement(self):
		self.eat(KEYWORD)
		values = []

		while self.current_token.type != SEMI:
			value = self.expression()
			values.append(value)
			if self.current_token.type == COMMA:
				self.eat(COMMA)

		self.eat(SEMI)
		return ('return', values)
	
	def while_loop(self):
		'''
		while	-> "while" "(" expression ")" block
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		condition = self.expression()
		self.eat(RPAREN)
		
		block = self.block()

		return ('while', condition, block)
	
	def for_loop(self):
		'''
		for   ->  "for" "(" expression ":" id_statement ")" block
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		
		iterator = self.expression()
		loop_variables = []
		
		if self.current_token.type == COLON:
			self.eat(COLON)
			
			if self.current_token.type == ID:
				loop_variables.append(self.id_statement())
				
				while self.current_token.type == COMMA:
					self.eat(COMMA)
					loop_variables.append(self.id_statement())
		
		self.eat(RPAREN)
		
		block = self.block()
		
		return ('for', (iterator, loop_variables), block)
	
	def var_assign(self):
		'''
		var assignment	->   "let" id_statement "=" expression
		'''
		self.eat(KEYWORD)
		
		var_name = self.id_statement()
		
		if self.current_token.type == SEMI:
			self.eat(SEMI)
			return ('let', var_name)
		self.eat(ASSIGN)
		
		var_content = self.expression()
		
		return ('let', var_name, var_content)
	
	def expression_statement(self):
		result = self.expression()
		return result
	
	def id_statement(self):
		'''
		Either "var1" or "obj.prop1.prop2.prop3 ..."
		'''
		variable_name = self.current_token.value
		self.eat(ID)
		
		if self.current_token.type == DOT:
			self.eat(DOT)
			property_name = self.current_token.value
			self.eat(ID)
			variable_name = self.property_access(variable_name, property_name)

		return ('var', variable_name)
	
	def property_access(self, object_name, property_name):
		properties =  ('.', object_name, property_name)

		while self.current_token.type == DOT:
			self.eat(DOT)
			property_name = self.current_token.value
			self.eat(ID)
			properties = ('.', properties, property_name)
			
		return properties
	
	def vector_elements(self):
		self.eat(LBRACKET)

		if self.current_token.type != RBRACKET:
			elements = [self.expression()]

			while self.current_token.type == COMMA:
				self.eat(COMMA)
				element = self.expression()
				elements.append(element)
		else:
			elements = []

		self.eat(RBRACKET)

		return elements
	
	def inherit_class(self):
		self.eat(LPAREN)

		if self.current_token.type != RPAREN:
			parent_classes = [self.id_statement()]

			while self.current_token.type == COMMA:
				self.eat(COMMA)
				parent_class = self.id_statement()
				parent_classes.append(parent_class)
		else:
			parent_classes = []

		self.eat(RPAREN)

		return parent_classes

	def parameters(self):
		'''
		parameters   -> "(" input_parameters ":" output_parameters ")"
		'''
		self.eat(LPAREN)
		input_parameters = []
		
		if self.current_token.type != RPAREN and self.current_token.type != COLON:
			input_parameters.append(self.id_statement()[1])

			while self.current_token.type == COMMA:
				self.eat(COMMA)
				input_parameters.append(self.id_statement()[1])
		

		if self.current_token.type == COLON:
			self.eat(COLON)

			output_parameters = []

			if self.current_token.type != RPAREN:
				output_parameters.append(self.expression())

				while self.current_token.type == COMMA:
					self.eat(COMMA)
					output_parameters.append(self.expression())
		else:
			output_parameters = []

		self.eat(RPAREN)

		return (input_parameters, output_parameters)
	
	def block(self):
		self.eat(LCURLY)
		statements = []

		while self.current_token.type != RCURLY:
			statements.append(self.statement())

		self.eat(RCURLY)

		return statements
	
	def expression(self):
		return self.comparison_expression()
	
	def comparison_expression(self):
		result = self.power_expression()
		count = 0

		while self.current_token.type in (LT, GT, LTE, GTE, EQ, NE):
			token = self.current_token
			
			if token.type == LT:
				self.eat(LT)
				result = ('<', result, self.power_expression())
			elif token.type == GT:
				self.eat(GT)
				result = ('>', result, self.power_expression())
			elif token.type == LTE:
				self.eat(LTE)
				result = ('<=', result, self.power_expression())
			elif token.type == GTE:
				self.eat(GTE)
				result = ('>=', result, self.power_expression())
			elif token.type == EQ:
				self.eat(EQ)
				result = ('==', result, self.power_expression())
			elif token.type == NE:
				self.eat(NE)
				result = ('!=', result, self.power_expression())
			
			if count == 0:
				last_term = result[-1]
			if count > 0:
				op, condition1, new_last_term = result
				
				condition2 = (op, last_term, new_last_term)
				
				result = ('and', condition1, condition2)
				
				last_term = new_last_term
			count += 1
		return result
	
	def power_expression(self):
		result = self.arithmetic_expression()
		
		if self.current_token.type == CARET:
			self.eat(CARET)
			result = ('^', result, self.arithmetic_expression())

		return result
	
	def arithmetic_expression(self):
		result = self.term()

		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				result = ('+', result, self.term())
			elif token.type == MINUS:
				self.eat(MINUS)
				result = ('-', result, self.term())

		return result
	
	def term(self):
		result = self.primary()

		while self.current_token.type in (ASTERISK, SLASH, MODULUS):
			token = self.current_token
			if token.type == ASTERISK:
				self.eat(ASTERISK)
				result = ('*', result, self.primary())
			elif token.type == SLASH:
				self.eat(SLASH)
				result = ('/', result, self.primary())
			elif token.type == MODULUS:
				self.eat(MODULUS)
				result = ('%', result, self.primary())

		return result
	
	def primary(self):
		result = self.factor()
		
		while self.current_token.type in (LPAREN, LBRACKET):
			if self.current_token.type == LPAREN:
				result = self.function_call(result)
			elif self.current_token.type == LBRACKET:
				result = self.factor_suffix(result)
		return result

	def factor(self):
		token = self.current_token
		
		if token.type == ID:
			return self.id_statement()
		elif token.type == NUM:
			self.eat(NUM)
			return ('Number', token.value)
		elif token.type == STR:
			self.eat(STR)
			return ('String', token.value)
		elif token.type == KEYWORD:
			self.eat(KEYWORD)
			if token.value == 'true':
				return ('Bool', True)
			elif token.value == 'false':
				return ('Bool', False)
			elif token.value == 'break':
				return ('Flow', token.value)
			elif token.value == 'continue':
				return ('Flow', token.value)
			elif token.value == 'None':
				return ('None', None)
			else:
				return None
		elif token.type == LPAREN:
			self.eat(LPAREN)
			
			result = None
			if self.current_token.type != RPAREN:
				result = self.expression()
				
			self.eat(RPAREN)
			return result
		elif token.type == LBRACKET:
			return self.vector_elements()
		elif token.type == MINUS:
			self.eat(MINUS)
			return ('-', self.factor())
		elif token.type == PLUS:
			self.eat(PLUS)
			return ('+', self.factor())
		elif token.type == NEGATE:
			self.eat(NEGATE)
			return ('!', self.factor())
		else:
			print(f'Unexpected token at line: {self.line_number + 1}\nToken: {token}')
			quit()

	def factor_suffix(self, expression):
		token = self.current_token
		if token.type == LPAREN:
			self.eat(LPAREN)
			arguments = self.arguments()
			self.eat(RPAREN)
			return ('call', expression, arguments)
		elif token.type == LBRACKET:
			self.eat(LBRACKET)
			index = self.expression()
			self.eat(RBRACKET)
			return ('index', expression, index)

	def function_call(self, expression):
		arguments = self.arguments()
		
		return ('call', expression, arguments)

	def arguments(self):
		'''
		arguments	-> expression ("," expression)*
		'''
		self.eat(LPAREN)
		
		if self.current_token.type == RPAREN:
			arg_list = []
		else:
			arg_list = [self.expression()]
			while self.current_token.type == COMMA:
				self.eat(COMMA)
				arg_list.append(self.expression())
		
		self.eat(RPAREN)
		
		return arg_list

class IterableIterator:
	def __init__(self, iterable):
		self.iterable = iterable
		self.current_pointer_value = len(iterable) - 1

	def __iter__(self):
		return self

	def __next__(self):
		if self.current_pointer_value < 0:
			raise StopIteration
		value = self.iterable[self.current_pointer_value]
		self.current_pointer_value -= 1
		return value

class Interpreter:
	def __init__(self):
		self.global_scope = {}
		self.scopes = [self.global_scope]
		self.current_scope = self.global_scope
		self.return_value = None
		self.functions = {}
		self.classes = {}
		self.aliases = {}
		self.stack_trace = []
		self.break_loop = False
		self.continue_loop = False
		self.internal_variables = {
			'__scope__': self.current_scope,
			'__heap__': self.classes,
			'__stack__': self.stack_trace,
		}
		self.local_vars = []
	
	def error(self, message):
		print(message)
		quit()
		
	def interpret(self, ast):
		for statement in ast:
			self.execute_statement(statement)

	def execute_statement(self, statement, scope={}):
		statement_type = statement[0]
		
		if statement_type == 'let':
			self.execute_variable_declaration(statement, scope)
		elif statement_type == 'if':
			self.execute_if_statement(statement)
		elif statement_type == 'class':
			self.execute_class_declaration(statement)
		elif statement_type == 'parent':
			self.execute_parent_declaration(statement, scope)
		elif statement_type == 'function':
			self.execute_function_declaration(statement)
		elif statement_type == 'from':
			self.execute_from_statement(statement)
		elif statement_type == 'while':
			self.execute_while_loop(statement)
		elif statement_type == 'for':
			self.execute_for_loop(statement)
		elif statement_type == 'return':
			self.execute_return_statement(statement)
		else:
			return self.evaluate_expression(statement, scope)
	
	def execute_return_statement(self, statement):
		if len(statement) > 1:
			self.return_value = []
			for expression in statement[1]:
				self.return_value.append(
					self.evaluate_expression(expression)
				)
		else:
			self.return_value = None
			
	def execute_while_loop(self, statement):
		while self.evaluate_expression(statement[1]):
			for line in statement[2]:
				if self.continue_loop: 
					self.continue_loop = False
					continue
				self.execute_statement(line)
				
				if self.break_loop or self.return_value is not None: break
			
			if self.break_loop or self.return_value is not None: break
		self.break_loop = False
	
	def execute_for_loop(self, statement):
		(iterable, loop_variables), loop_block = statement[1:]
		
		if iterable[0] == 'var': 
			iterable = self.get_variable_value(iterable[1])
		
		iterator = IterableIterator(iterable)
		
		loop_variable = loop_variables[0][1]
		self.create_loop_variable(loop_variable)
		
		while True:
			try:
				value = next(iterator)
				self.create_new_scope()
				if loop_variable is not None:
					self.set_variable_value(loop_variable, value)
				self.execute_block(loop_block)
				self.destroy_current_scope()
			except StopIteration:
				break
		#self.clean_up([loop_variable])
	
	def create_loop_variable(self, name):
		self.current_scope[name] = None
	
	def set_variable_value(self, variable_name, value):
		for scope in reversed(self.scopes):
			if variable_name in scope:
				scope[variable_name] = value
				return
		self.current_scope[variable_name] = value
	
	def execute_variable_declaration(self, statement, scope={}):
		variable_name = statement[1][1]
		
		if type(variable_name) is tuple:
			object_name = variable_name[1]
			property_name = variable_name[-1]
			parent = scope.get(object_name)
			
			if parent is None:
				parent = self.current_scope.get(object_name).get('me')
				if parent is None:
					parent = self.current_scope.get(object_name)
					if parent is None:
						self.error(f'Tried to create "{object_name}.{property_name}" while "{object_name}" does not exist')
				
			while type(property_name) is tuple and parent is not None:
				
				expression = property_name
				object_name = expression[1]
				parent = parent.get(object_name)
				property_name = expression[-1]
			
			if parent is None:
				expr = (".", object_name, property_name)
				self.error(f'Tried to create "{self.show_varname(expr)}" while "{object_name}" does not exist')
			
			value = self.evaluate_expression(statement[2]) if len(statement) > 2 else None
			
			parent[property_name] = value
			return
		if len(statement) > 2:
			initial_value = self.execute_variable_assignment(variable_name, statement[2])
		else:
			self.current_scope[variable_name] = None
			self.local_vars.append(variable_name)
	
	def execute_variable_assignment(self, variable_name, expression):
		value = self.evaluate_expression(expression)
		self.current_scope[variable_name] = value
		self.local_vars.append(variable_name)
	
	def evaluate_expression(self, expression, scope={}):
		if isinstance(expression, int) or isinstance(expression, str) or isinstance(expression, bool):
			return expression
		elif isinstance(expression, list):
			return [self.evaluate_expression(item) for item in expression]
		elif expression is None:
			return 'null'
		elif isinstance(expression, tuple):
			expression_type = expression[0]
			if expression_type == 'Number':
				return expression[1]
			elif expression_type == 'String':
				return expression[1]
			elif expression_type == 'Bool':
				return expression[1]
			elif expression_type == 'None':
				return expression[1]
			elif expression_type == 'Flow':
				self.break_and_continue(expression[1])
			elif expression_type == 'var':
				return self.get_variable_value(expression[1], scope)
			elif expression_type in ['!', '-'] and len(expression) <= 2:
				return self.evaluate_unary_operation(expression)
			elif expression_type in BIN_OPS:
				return self.evaluate_binary_operation(expression)
			elif expression_type == '.':
				return self.evaluate_property_access(expression, scope)
			elif expression_type == 'call':
				self.stack_trace.append(self.show_varname(expression[1][1]))
				value = self.evaluate_function_call(expression, scope)
				self.stack_trace.pop()
				return value
			elif expression_type == 'index':
				return self.evaluate_index_value(expression)
			else:
				print(expression)
				self.error(f"Invalid expression: '{expression_type}'")
		else:
			self.error(f"Invalid expression: '{expression}'")
			
	def get_variable_value(self, variable_name, scope={}):
		if type(variable_name) is tuple:
			return self.evaluate_property_access(variable_name, scope)
		if variable_name in self.current_scope:
			return self.current_scope[variable_name]
		for scope in reversed(self.scopes):
			if variable_name in scope:
				return scope[variable_name]
		if variable_name in self.internal_variables:
			return self.internal_variables[variable_name]
		self.error(f"Variable '{self.show_varname(variable_name)}' is not defined")
	
	def make_filename(self, module_name):
		if '.' not in module_name:
			if os.path.exists(module_name):
				if os.path.isdir(module_name):return os.path.exists(module_name)
				else: return os.path.abspath(module_name + '.mar')
		
		dir_name = './'
		lib_dir_name = LIBRARY_PATH
		for filename in module_name.split('.'):
			
			if os.path.isfile(dir_name + filename + '.mar'):
				return os.path.abspath(dir_name + filename + '.mar')
			if os.path.isdir(dir_name + filename):
				dir_name +=  f'{filename}' + PATHSPLIT
				continue
			if os.path.isfile(lib_dir_name + filename + '.mar'):
				return os.path.abspath(lib_dir_name + filename + '.mar')
			if os.path.isdir(lib_dir_name + filename):
				lib_dir_name +=  f'{filename}' + PATHSPLIT
				continue
			
		return None
	
	def get_content(self, module_name):
		content = ''
		filename = self.make_filename(module_name)
		if not filename: return None, content
		print(content)
		try:
			with open(filename, 'r') as fo:
				content = fo.read()
		except FileNotFoundError:
			print(f'File is Missing {filename}\nFailling safe to use language library')
			
		return filename, content
		
	
	def execute_from_statement(self, statement):
		parent_module = statement[1]
		import_modules = statement[2]
		aliases = statement[-1]
		
		if aliases and len(aliases) != len(import_modules):
			self.error(f'Number of import modules aliases did not match the import modules.\nNumber of Import Modules: {len(import_modules)}\nNumber of Aliases: {len(aliases)}')
			
		if not aliases:
			aliases = [None] * len(import_modules)
		
		#if not parent_module:
			#self.execute_use_statement(import_modules, aliases)
		#else:
		self.execute_import(parent_module[1], import_modules, aliases)
		
	def execute_import(self, parent_module, import_modules, aliases):
		parent_module = self.show_varname(parent_module)
		
		failed = False
		filename, content = self.get_content(parent_module)
		
		if not filename:
			failed = True
		
		if failed:
			self.error(f"[Import Error] Module was not found!\n\nNo module named '{parent_module.replace('.', '/')}'")
		
		tokens = Lexer(content).lex()
		ast = CustomizedParser(tokens).parse()
		
		internal = Interpreter()
		internal.interpret(ast)
		
		for import_module, alias in zip(import_modules, aliases):
			#checking in global_scope
			if import_module[1] in internal.global_scope:
				value = internal.global_scope[import_module[1]]
				if alias: 
					self.current_scope[alias[1]] = value
					self.aliases[alias[1]] = import_module[1]
				else: self.current_scope[import_module[1]] = value
				continue
				
			#checking in functions
			if import_module[1] in internal.functions:
				value = internal.functions[import_module[1]]
				if alias: 
					self.functions[alias[1]] = value
					self.aliases[alias[1]] = import_module[1]
				else: self.functions[import_module[1]] = value
				continue
			
			#checking in classes
			if import_module[1] in internal.classes:
				value = internal.classes[import_module[1]]
				for class_name in value[1]:
					self.classes[class_name[1]] = internal.classes[class_name[1]]
				if alias:
					self.classes[alias[1]] = value
					self.aliases[alias[1]] = import_module[1]
				else: self.classes[import_module[1]] = value
				continue
			
			if import_module[1] == parent_module:
				self.import_all(import_module[1], alias[1], internal)
				continue
			self.error(f"\n[Import Error] Module '{import_module[1]}' was not found in '{parent_module}' ({filename})")
	
	def import_all(self, module_name, alias, interpreter):
		# Import global
		value = interpreter.global_scope
		if alias:
			self.current_scope[alias] = value
			self.aliases[alias] = module_name
		else: self.current_scope[module_name] = value
		
		# Import functions
		value = interpreter.functions
		if alias:
			self.functions[alias] = value
			self.aliases[alias] = module_name
		else: self.functions[module_name] = value
		
		# Import classes
		value = interpreter.classes
		if alias:
			self.classes[alias] = value
			self.aliases[alias] = module_name
		else: self.classes[module_name] = value
		
	def evaluate_index_value(self, expression):
		vector = self.evaluate_expression(expression[1])
		index = self.evaluate_expression(expression[-1])
		
		if type(index) is not int:
			self.error(f"index must be an int but found {index}")
			
		return vector[index]
		
	def break_and_continue(self, statement):
		if statement == 'break':self.break_loop = True
		elif statement == 'continue' :self.continue_loop = True
		
	def execute_if_statement(self, if_statement):
		condition, if_block, elif_clauses, else_clause = if_statement[1:]
		
		if self.evaluate_expression(condition):
			self.execute_block(if_block)
		else:
			for elif_condition, elif_block in elif_clauses:
				if self.evaluate_expression(elif_condition):
					for statement in elif_block:
						self.execute_statement(statement)
					return
			if else_clause:
				for statement in else_clause:
					self.execute_statement(statement)

	def evaluate_binary_operation(self, expression):
		operator = expression[0]
		left_operand = self.evaluate_expression(expression[1])
		right_operand = self.evaluate_expression(expression[2])
		
		if operator == '+':
			return left_operand + right_operand
		elif operator == '-':
			return left_operand - right_operand
		elif operator == '*':
			return left_operand * right_operand
		elif operator == '^':
			return left_operand ** right_operand
		elif operator == '/':
			return left_operand / right_operand
		elif operator == '%':
			return left_operand % right_operand
		elif operator == '>':
			return left_operand > right_operand
		elif operator == '<':
			return left_operand < right_operand
		elif operator == '<=':
			return left_operand <= right_operand
		elif operator == '>=':
			return left_operand >= right_operand
		elif operator == '!=':
			return left_operand != right_operand
		elif operator == 'and':
			return left_operand and right_operand
		elif operator == 'or':
			return left_operand or right_operand
		elif operator == '==':
			return left_operand == right_operand
		else:
			self.error(f"Invalid binary operator: '{operator}'")		
	
	def evaluate_unary_operation(self, expression):
		operator = expression[0]
		operand = self.evaluate_expression(expression[1])
		if operator == '!':
			return not operand
		elif operator == '-':
			return -operand
		else:
			self.error(f"Invalid unary operator: '{operator}'")
	
	def evaluate_property_access(self, expression, scope={}):
		object_name = expression[1]
		property_name = expression[2]
		object_value = self.get_variable_value(object_name)
		
		if object_name != 'me' and 'me' in object_value.keys():
			object_value = object_value['me']
		
		while type(property_name) is tuple:
			expression = property_name
			object_value = object_value[property_name]
			property_name = expression[2]
		
		if isinstance(object_value, dict) and property_name in list(object_value.keys()):
			return object_value[property_name]
		else:
			self.error(f"Property '{property_name}' not found on object '{object_name}'")
		
	def execute_block(self, block, scope={}):
		for statement in block:
			self.execute_statement(statement, scope)
			if self.return_value is not None:
				break
		return self.return_value
	
	def execute_function_declaration(self, statement):
		function_name = statement[1][1]
		parameters = statement[2]
		body = statement[3]
		
		self.functions[function_name] = (parameters, body)

	def evaluate_function_call(self, statement, scope):
		identifier = statement[1][1]
		args = statement[2]
		func_scope = {}
		
		cls_method = False
		if identifier in list(INBUILT_FUNCTION.keys()):
			return INBUILT_FUNCTION[identifier](
				[self.evaluate_expression(arg, self.current_scope) for arg in args]
			)
		elif type(identifier) is tuple:
			object_name = identifier[1]
			object_value = self.get_variable_value(object_name)
			if type(object_value) is list or type(object_value) is str or type(object_value) is int:
				return self.evaluate_list_method(object_value, identifier, args)
			class_name = self.current_scope[object_name]['::type'][0] if not self.current_scope[object_name]['::alias'] else self.current_scope[object_name]['::alias']
			method_name = identifier[2]
			
			while type(method_name) is tuple:
				object_name = method_name[1]
				object_value = self.get_variable_value(object_name)
				if type(object_value) is list or type(object_value) is str or type(object_value) is int:
					return self.evaluate_list_method(object_value, identifier)
				class_name = self.current_scope[object_name]['::type'][0] if not self.current_scope[object_name]['::alias'] else self.current_scope[object_name]['::alias']
				method_name = method_name[-1]
			
			method = self.classes.get(class_name).get(method_name)
			if not method:
				classes = self.get_variable_value(object_name)['::type']
				for class_name in classes[1:]:
					while type(class_name) is tuple:
						class_name = class_name[-1]
						
					method = self.classes.get(class_name).get(method_name)
					if method: break
				
			if not method: self.error(f"Method '{method_name}()' not found on object '{self.show_varname(object_name)}'")
			parameters, body = method
			
			if 'me' == parameters[0][0]:
				func_scope = self.get_variable_value(object_name)
			cls_method = True
		elif identifier in list(self.classes.keys()):
			return self.execute_class_constructor(identifier, args)
		elif identifier not in self.functions:
			self.error(f"Identifier '{self.show_varname(identifier)}' is not defined")
		else:
			parameters, body = self.functions[identifier]
		
		input_params, output_params = parameters
		
		new_scope = {}
		if func_scope:
			new_scope = func_scope
			input_params = input_params[1:]
			
		
		if len(input_params) != len(args):
			self.error(f"Function '{self.show_varname(identifier)}()' expects {len(input_params)} arguments, but {len(args)} {'was' if len(input_params) == 1 else 'were' } provided")
			
		for i in range(len(input_params)):
			parameter = input_params[i]
			argument = self.evaluate_expression(args[i])
			new_scope[parameter] = argument
		
		self.scopes.append(new_scope)
		self.current_scope = new_scope
		
		initial_return = self.execute_block(body, self.current_scope)
		
		if initial_return:
			self.return_value = None
			self.clean_up(input_params)
			self.scopes.pop()
			self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
			self.local_vars = []
			if len(initial_return) == 1: return initial_return[0]
			else: return initial_return
		
		retr = [self.evaluate_expression(param, self.current_scope) for param in output_params]
		
		self.clean_up(input_params)
		self.destroy_current_scope()
		self.clean_scope()
		
		self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
		self.local_vars = []
		
		if retr:
			if len(retr) == 1: return retr[0]
			else: return retr
		else: return
	
	def execute_class_declaration(self, statement):
		class_name = statement[1][1]
		methods = statement[2]
		
		parent_classes = statement[3]
		self.classes[class_name] = {}
		
		for method in methods:
			method_name = method[1][1]
			parameters = method[2]
			body = method[3]
			
			self.classes[class_name][method_name] = (parameters, body)
			
		# 1 used to avoid conflict with method names
		self.classes[class_name][1] = parent_classes if parent_classes else []
	
	def execute_class_constructor(self, class_name, args):
		me = {}
		class_var = {'me': me, '::alias': None}
		
		if class_name in self.aliases: 
			class_var['::alias'], class_name = class_name, self.aliases[class_name]
		
		if not class_var['::alias']:
			if class_name in self.classes[class_name]:
				constructor = self.classes[class_name][class_name]
			else: constructor = None
		else:
			if class_name in self.classes[class_var['::alias']]:
				constructor = self.classes[class_var['::alias']][class_name]
			else: constructor = None
		class_var['::type'] = [class_name]
		
		if constructor:
			class_var = self.execute_special(constructor, args, class_var)
			return class_var
		else:
			return class_var
	
	def execute_parent_declaration(self, statement, scope):
		class_name = statement[1][1]
		args = statement[-1]
		
		constructor = self.classes.get(class_name).get(class_name)
		if not constructor: return
		
		cls_name = scope['::type'][0] if not scope['::alias'] else scope['::alias']
		parent_classes = self.classes[cls_name][1]
		
		if statement[1] in parent_classes:
			scope['::type'].append(class_name)
		else:
			self.error(f"class '{class_name}' not defined in Parent class list")
			
		self.execute_special(constructor, args, scope)
		
	def execute_special(self, constructor, args, class_dict):
		parameters, body = constructor
			
		input_params, output_params = parameters
		if input_params[0] != 'me': 
			self.error(f"Expected 'me' as first class '{class_dict['::type']}' constructor parameter but found '{input_params[0]}'")
			
		if len(input_params[1:]) != len(args):
			self.error(f"class '{class_dict['::type']}' constructor expects {len(input_params[1:]) if len(input_params[1:]) else 'no'} arguments, but {len(args)} {'was' if len(input_params) == 1 else 'were' } provided \n\n{self.evaluate_expression(args)}\n")
			
		new_scope = {}
		for i in range(len(input_params[1:])):
			parameter = input_params[1:][i]
			argument = self.evaluate_expression(args[i])
			new_scope[parameter] = argument
		input_params = input_params[1:]
		
		self.scopes.append(new_scope)
		self.current_scope = new_scope
		self.local_vars = []
		
		for statement in body:
			self.execute_statement(statement, class_dict)
		
		self.clean_up(input_params)
		self.destroy_current_scope()
		self.clean_scope()
		
		self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
		self.local_vars = []
		return class_dict
	
	def clean_up(self, params):
		for param in params:
			del self.current_scope[param]
		
	def clean_scope(self):
		for local_var in self.local_vars:
			if local_var in self.current_scope.keys():
				del self.current_scope[local_var]
			
	def create_new_scope(self):
		new_scope = {}
		self.scopes.append(new_scope)
	
	def destroy_current_scope(self):
		self.scopes.pop()
		
	def show_varname(self, identifier):
		if type(identifier) is not tuple:
			return identifier
		
		name = []
		while type(identifier) is tuple:
			name.append(identifier[-1])
			identifier = identifier[1]
		name.append(identifier)
		
		return '.'.join(name[::-1])
	
	def evaluate_list_method(self, obj, identifier, args):
		function = identifier[-1]
		
		try:
			method = getattr(obj, function)
			return method(*[self.evaluate_expression(arg, self.current_scope) for arg in args])
		except :
			obj_type = type(obj)
			if obj_type is str:
				obj_type = 'String'
			elif obj_type is int:
				obj_type = "Number"
			else:
				obj_type = "Vector"
			self.error(f"[TypeError] '{obj_type}' object has no method '{function}'")
