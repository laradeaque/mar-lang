from errors import UnknownChar, Syntax_Error, ParseError, Panic,ExecutionError
from pathlib import Path
import json
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
INCREMENT = 'INCREMENT'
DECREMENT = 'DECREMENT'
MODULUS = 'MODULUS'
COLON = 'COLON'
SEMI = 'SEMI'
DOT = 'DOT'
QUESTION = 'QUESTION'
PLUS = 'PLUS'
MINUS = 'MINUS'
ASTERISK = 'ASTERISK'
DIVISION='DIVISION'
CARET = 'CARET'
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
	'&',
	'|'
)
BASE_DIR = Path(__file__).resolve().parent
LIBRARY_PATH = os.path.join(BASE_DIR, 'lib/')
PATHSPLIT = '/'

INBUILT_FUNCTION = {}
INBUILT_FUNCTION['print'] =  lambda x: do_print(x)
INBUILT_FUNCTION['int'] =  lambda x: x2int(x)
INBUILT_FUNCTION['string'] =  lambda x: x2str(x)
INBUILT_FUNCTION['readline'] =  lambda x: prompt(x)
INBUILT_FUNCTION['sysprint'] = lambda x: systemprint(*x)
INBUILT_FUNCTION['length'] =  lambda x: length(x)
INBUILT_FUNCTION['set'] =   lambda x: assign(*x)

def do_print(x):
	print(''.join(converter(x)))
	return None, None

def x2int(x):
	try: 
		y = to_int(x)
	except (TypeError, ValueError):
		return None, ExecutionError(
			'ExecutionError: TypeError',
			f"Cannot convert '{x}' to int"
		)
	return y, None

def x2str(x):
	return ''.join(to_str(x)), None

def prompt(x):
	return input(*to_str(x)), None

def length(x):
	return len(*x), None

converter = lambda x: to_str(x)

def assign(l, key, value=None):
	if type(l) is not dict and type(l) is not list:
		return None, ExecutionError(
			'ExecutionError: SetError',
			f'Cannot use set() on {l}'
		)
	if key == '::type':
		obj = 'Vector' if type(l) is list else l['::type']
		return None, ExecutionError(
			'ExecutionError: TypeError',
			f'Cannot set type to a {obj}'
		)
	l[key] = value
	
	### Change Value to None if it is not to be returned
	return value, None

def systemprint(x):
	if type(x) is dict:
		print(json.dumps(x, indent=4, sort_keys=False))
	else:
		print(x)
	
	return None, None

def to_str(expression):
	expr_str = []
	for term in expression:
		if type(term) is float or type(term) is str or type(term) is int: 
			expr_str.append(str(term))
		elif type(term) is list:
			expr_str.append(str(handle_list(term)))
		elif type(term) is tuple:
			expr_str.append(str(handle_tuple(term)))
		elif type(term) is dict:
			if term['::type'] == 'dict':
				term = term.copy()
				del term['::type']
			expr_str.append(str(term))
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
	def __init__(self, type, value, pos_start, pos_end=0):
		self.type = type
		self.value = value
		self.pos_start = pos_start
		self.pos_end = pos_end

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
		comment = False
		for line in lines:
			self.line = line
			self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
			if comment:
				comment = self.multiline_comment()
			else:
				toks, comment, error = self.get_tokens()
				if error: return None, error
			self.pos = 0
			self.line_number += 1
			tokens.extend(toks)
			tokens.append(Token(EOL, '\\n', None))

		tokens.append(Token(EOF, None, None))
		return tokens, None

	def skip_whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()
			
	def multiline_comment(self):
		while self.current_char is not None:
			if self.current_char == '*' and self.peek() == '/':
				return False
			self.advance()
		return True

	def skip_comment(self):
		if self.current_char == '#':
			while self.current_char is not None and self.current_char != '\n':
				self.advance()

	def peek(self):
		peek_pos = self.pos + 1
		return self.line[peek_pos] if peek_pos < len(self.line) else None

	def get_identifier(self):
		result = ''
		pos_start = self.pos

		while self.current_char is not None and self.current_char.isalnum() or self.current_char == '_':
			result += self.current_char
			self.advance()
		
		if result in KEYWORDS:
			return Token(KEYWORD, result, pos_start)
		else:
			return Token(ID, result, pos_start)

	def get_number(self):
		'''
		12.343
		'''
		num_str = ''
		dot_count = 0
		pos_start = self.pos

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
			num_str += self.current_char
			self.advance()
		
		if dot_count == 0:
			return Token(NUM, int(num_str), pos_start)
		else:
			return Token(NUM, float(num_str), pos_start)

	def get_string(self):
		string = ''
		escape_character = False
		used = self.current_char
		pos_start = self.pos
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
		
		pos_end = self.pos
		self.advance()
		return Token(STR, string, pos_start, pos_end), None

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
				tokens.append(self.get_identifier())
			elif self.current_char.isdigit():
				tokens.append(self.get_number())
			elif self.current_char == '"' or self.current_char == "'":
				token, error = self.get_string()
				if error: return None, False, error
				tokens.append(token)
			elif self.current_char == '(':
				tokens.append(Token(LPAREN, '(', self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(RPAREN, ')', self.pos))
				self.advance()
			elif self.current_char == ',':
				tokens.append(Token(COMMA, ',', self.pos))
				self.advance()
			elif self.current_char == ':':
				tokens.append(Token(COLON, ':', self.pos))
				self.advance()
			elif self.current_char == ';':
				tokens.append(Token(SEMI, ';', self.pos))
				self.advance()
			elif self.current_char == '>':
				if self.peek() == '=':
					tokens.append(Token(GTE, '>=', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(GT, '>', self.pos))
					self.advance()
			elif self.current_char == '<':
				if self.peek() == '=':
					tokens.append(Token(LTE, '<=', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(LT, '<', self.pos))
					self.advance()
			elif self.current_char == '[':
				tokens.append(Token(LBRACKET, '[', self.pos))
				self.advance()
			elif self.current_char == ']':
				tokens.append(Token(RBRACKET, ']', self.pos))
				self.advance()
			elif self.current_char == '{':
				tokens.append(Token(LCURLY, '{', self.pos))
				self.advance()
			elif self.current_char == '}':
				tokens.append(Token(RCURLY, '}', self.pos))
				self.advance()
			elif self.current_char == '.':
				tokens.append(Token(DOT, '.', self.pos))
				self.advance()
			elif self.current_char == '+':
				if self.peek() == '+':
					tokens.append(Token(INCREMENT, '++', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(PLUS, '+', self.pos))
					self.advance()
			elif self.current_char == '-':
				if self.peek() == '-':
					tokens.append(Token(DECREMENT, '--', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(MINUS, '-', self.pos))
					self.advance()
			elif self.current_char == '*':
				tokens.append(Token(ASTERISK, '*', self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(CARET, '^', self.pos))
				self.advance()
			elif self.current_char == '/' :
				if self.peek() == '*':
					self.multiline_comment()
					self.advance()
					self.advance()
					return tokens, True, None
				else:
					tokens.append(Token(DIVISION, '/', self.pos))
					self.advance()
			elif self.current_char == '%':
				tokens.append(Token(MODULUS, '%', self.pos))
				self.advance()
			elif self.current_char == '=':
				if self.peek() == '=':
					tokens.append(Token(EQ, '==', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(ASSIGN, '=', self.pos))
					self.advance()
			elif self.current_char == '!':
				if self.peek() == '=':
					tokens.append(Token(NE, '!=', self.pos))
					self.advance()
					self.advance()
				else:
					tokens.append(Token(NEGATE, '!', self.pos))
					self.advance()
			elif self.current_char == '&':
				tokens.append(Token(AND, '&', self.pos))
				self.advance()
			elif self.current_char == '|':
				tokens.append(Token(OR, '|', self.pos))
				self.advance()
			else:
				return tokens, False, Syntax_Error(
                    "SyntaxError: Unknown Character", 
                    self.current_char, 
                    self.pos, 
                    self.line_number, 
                    self.text
                )
		return tokens, False, None

class CmdLexer(Lexer):
	def __init__(self):
		super().__init__('')
		
	def lex_line(self, line):
		tokens = []
		self.line = line
		self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
		tokens, __, error = self.get_tokens()
		if error: return None, error
		tokens.extend([Token(EOL, '\\n', None), Token(EOF, None, None)])
		return tokens, None
	
	def get_string(self):
		string = ''
		escape_character = False
		used = self.current_char
		pos_start = self.pos
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
		
		pos_end = self.pos
		if self.current_char != used:
			self.advance()
			return None, Syntax_Error(
				"SyntaxError: Unclosed String",	
				used, 	
				pos_start, 
				0,
				self.line
			)
		self.advance()
		return Token(STR, string, pos_start, pos_end), None 

class Parser:
	def __init__(self, tokens, text):
		self.tokens = tokens
		self.line_number = 0
		self.tok_idx = 0
		self.text = text
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
		print('call the parse error' )
		quit()
	
	def eat(self, token_type):
		if self.current_token.type == token_type:
			self.advance()
		else:
			return
		
	def parse(self):
		result, error = self.program()
		
		if error: return None, error
		if self.current_token.type != EOF:
			return None, Panic(self.line_number + 1)
		
		return result, None
	
	def program(self):
		'''
		program 	-> statement program 
		'''
		statements = []
		
		while self.current_token.type != EOF:
			value, error = self.statement()
			
			if error: return None, error
			statements.append(value)
		
		return statements, None
	
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
				value, error = self.function_declaration()
				if error: return None, error
				return value, None
			if self.current_token.value == 'parent':
				value, error = self.parent_initialisation()
				if error: return None, error
				return value, None
			if self.current_token.value == 'return':
				value, error = self.return_statement()
				if error: return None, error
				return value, None
			if self.current_token.value == 'while':
				value, error = self.while_loop()
				if error: return None, error
				return value, None
			if self.current_token.value == 'class':
				value, error = self.class_declaration()
				if error: return None, error
				return value, None
			if self.current_token.value == 'for':
				value, error = self.for_loop()
				if error: return None, error
				return value, None
			if self.current_token.value == 'let':
				value, error = self.var_assign()
				if error: return None, error
				return value, None
			if self.current_token.value == 'if':
				value, error = self.if_statement()
				if error: return None, error
				return value, None
			if self.current_token.value == 'from' or self.current_token.value == 'use':
				value, error = self.from_statement()
				if error: return None, error
				return value, None
			else:
				value, error = self.expression_statement()
				if error: return None, error
				return value, None
		else:
			value, error = self.expression_statement()
			if error: return None, error
			return value, None
	
	def function_declaration(self):
		'''
		function	-> "function" id_statement parameters block
		'''
		self.eat(KEYWORD)
		
		function_name, error = self.id_statement()
		if error: return None, error
		
		(input_parameters, output_parameters, default_args), error = self.parameters()
		if error: return None, error
		
		block, error = self.block()
		if error: return None, error
		
		return ('function', function_name, (input_parameters, output_parameters, default_args), block), None
	
	def parent_initialisation(self):
		'''
		parent_initialisation   -> "parent" id_statement function_call
		'''
		self.eat(KEYWORD)
		
		parent_name, error = self.id_statement()
		if error: return None, error
		
		parent_args, error = self.arguments()
		if error: return None, error
	
		return ('parent', parent_name, parent_args), None
	
	def class_declaration(self):
		'''
		class	-> "class" id_statement block
		'''
		self.eat(KEYWORD)
		
		class_name, error = self.id_statement()
		if error: return None, error
		
		parent_classes, error = self.inherit_class() if self.current_token.type == 'LPAREN' else ([], None)
		if error: return None, error
	
		block, error = self.block()
		if error: return None, error
		
		return ('class', class_name, block, parent_classes), None
	
	def from_statement(self):
		'''
		use_statement  -> "from" id_statement "use" module_names "as" id_statement
					   -> "use" module_names "as" id_statement
		'''
		if self.current_token.value == "from":
			self.eat(KEYWORD)
			parent_module, error = self.id_statement()
			if error: return None, error
			
			if self.current_token.value != 'use': 
				return None, ParseError(
					'ParseError:Import Error', 
					self.current_token.value,
					self.current_token.pos_start,
					self.line_number, 
					self.text, 
					f'Expected the keyword "use" but found {self.current_token.value}'
				)
			self.eat(KEYWORD)
			module_names, error = self.module_names()
			if error: return None, error
		else:
			self.eat(KEYWORD)
			parent_module =  None
			module_names, error = self.module_names()
			if error: return None, error
		
		alias = []
		if self.current_token.type == KEYWORD and self.current_token.value == 'as':
			self.eat(KEYWORD)
			
			al, error = self.module_names()
			if error: return None, error
			
			alias.append(al)
		
		return ('from', parent_module, module_names, alias), None
		
	def module_names(self):
		paren = False
		if self.current_token.type == LPAREN:
			self.eat(LPAREN)
			paren = True
		name, error = self.id_statement()
		if error: return None, error
		names = [name]
		
		while self.current_token.type == 'COMMA':
			self.eat(COMMA)
			name, error = self.id_statement()
			if error: return None, error
			
			names.append(name)
		
		if paren: self.eat(RPAREN)
		if error: return None, error
	
		return names, None
		
	def if_statement(self):
		'''
		if_statement  -> "if" "(" expression ")" block elif_clauses else_clause
		elif_clauses  -> "elif" "(" expression ")" block elif_clauses | ε
		else_clause   -> "else" block | ε
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		condition, error = self.expression()
		if error: return None, error
		self.eat(RPAREN)
		
		if_block, error = self.block()
		if error: return None, error
		elif_clauses = []
		else_clause = None

		while self.current_token.value == 'elif':
			self.eat(KEYWORD)
			
			self.eat(LPAREN)
			elif_condition, error = self.expression()
			if error: return None, error
			
			self.eat(RPAREN)
			
			elif_block, error = self.block()
			if error: return None, error
			elif_clauses.append((elif_condition, elif_block))

		if self.current_token.value == 'else':
			self.eat(KEYWORD)
			else_block, error = self.block()
			else_clause = else_block
			if error: return None, error

		return ('if', condition, if_block, elif_clauses, else_clause), None
	
	def return_statement(self):
		self.eat(KEYWORD)
		values = []

		while self.current_token.type != SEMI:
			value, error = self.expression()
			if error: return None, error
			
			values.append(value)
			if self.current_token.type == COMMA:
				self.eat(COMMA)

		self.eat(SEMI)
		return ('return', values), None
	
	def while_loop(self):
		'''
		while	-> "while" "(" expression ")" block
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		condition, error = self.expression()
		if error: return None, error
	
		self.eat(RPAREN)
		
		block, error = self.block()
		if error: return None, error

		return ('while', condition, block), None
	
	def for_loop(self):
		'''
		for   ->  "for" "(" expression ":" id_statement ")" block
		'''
		self.eat(KEYWORD)
		
		self.eat(LPAREN)
		
		iterator, error = self.expression()
		if error: return None, error
		loop_variables = []
		
		if self.current_token.type == COLON:
			self.eat(COLON)
			
			if self.current_token.type == ID:
				name, error = self.id_statement()
				if error: return None, error
				loop_variables.append(name)
				
				while self.current_token.type == COMMA:
					self.eat(COMMA)
					name, error = self.id_statement()
					if error: return None, error
					loop_variables.append(name)
					
		self.eat(RPAREN)
		
		block, error = self.block()
		if error: return None, error
		
		return ('for', (iterator, loop_variables), block), None
	
	def var_assign(self):
		'''
		var assignment	->   "let" id_statement "=" expression
		'''
		self.eat(KEYWORD)
		
		var_name, error = self.id_statement()
		if error: return None, error
		
		if self.current_token.type == SEMI:
			self.eat(SEMI)
			return ('let', var_name), None
			
		if self.current_token.type == COMMA:
			statement, error = self.multi_assignment(var_name)
			if error: return None, error
			return statement, None
			
		self.eat(ASSIGN)
		
		var_content, error = self.expression()
		if error: return None, error
		
		return ('let', var_name, var_content), None
		
	def variable_assign(self, var_name):
		'''
		var assignment	->   id_statement "=" expression
		'''
		self.eat(ASSIGN)
		
		if self.current_token.type == SEMI:
			self.eat(SEMI)
			return ('let', var_name), None
			
		var_content, error = self.expression()
		if error: return None, error
		
		return ('let', var_name, var_content), None
	
	def expression_statement(self):
		result, error = self.expression()
		if error: return None, error
		
		return result, None
	
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
			variable_name, error = self.property_access(variable_name, property_name)
			if error: return None, error

		return ('var', variable_name), None
	
	def property_access(self, object_name, property_name):
		properties =  ('.', object_name, property_name)

		while self.current_token.type == DOT:
			self.eat(DOT)
			property_name = self.current_token.value
			self.eat(ID)
			properties = ('.', properties, property_name)
			
		return properties, None
	
	def vector_elements(self):
		self.eat(LBRACKET)

		if self.current_token.type != RBRACKET:
			element, error = self.expression()
			if error: return None, error
			elements = [element]

			while self.current_token.type == COMMA:
				self.eat(COMMA)
				if self.current_token.type == RBRACKET: break
				element, error = self.expression()
				if error: return None, error
				elements.append(element)
		else:
			elements = []

		self.eat(RBRACKET)

		return elements, None
		
	def get_key(self):
		key = ''
		token = self.current_token
		
		if token.type == NUM:
			self.eat(NUM)
			return ('Number', token.value), None
		elif token.type == STR:
			self.eat(STR)
			return ('String', token.value), None
		else:
			return None, ParseError(
				'ParseError:Type Error', 
				self.current_token.value,
				self.current_token.pos_start,
				self.line_number, 
				self.text, 
				'Key must be either String or Number type'
			)
			
		return key, None
	
	def dict_elements(self):
		self.eat(LCURLY)
		
		if self.current_token.type != RCURLY:
			key, error = self.get_key()
			if error: return None, error
			
			self.eat(COLON)
			value, error = self.expression()
			if error: return None, error

			elements = {key: value}
			while self.current_token.type == COMMA:
				self.eat(COMMA)
				if self.current_token.type == RCURLY: break
				key, error = self.get_key()
				if error: return None, error
				
				self.eat(COLON)
				elements[key], error = self.expression()
				if error: return None, error
		else:
			elements = {}
		
		self.eat(RCURLY)

		return elements, None
	
	def inherit_class(self):
		self.eat(LPAREN)

		if self.current_token.type != RPAREN:
			parent_class, error = self.id_statement()
			if error: return None, error
		
			parent_classes = [parent_class]

			while self.current_token.type == COMMA:
				self.eat(COMMA)
				parent_class, error = self.id_statement()
				if error: return None, error
				parent_classes.append(parent_class)
		else:
			parent_classes = []

		self.eat(RPAREN)

		return parent_classes, None

	def parameters(self):
		'''
		parameters   -> "(" input_parameters ":" output_parameters ")"
		'''
		self.eat(LPAREN)
		input_parameters = []
		default_args = {}
		
		if self.current_token.type != RPAREN and self.current_token.type != COLON:
			param, error = self.id_statement()
			if error: return None, error
			input_parameters.append(param[1])
			
			if self.current_token.type == ASSIGN:
				self.eat(ASSIGN)
				
				arg_name = input_parameters[-1]
				default_args[arg_name], error = self.expression()
				if error: return None, error
			
			while self.current_token.type == COMMA:
				self.eat(COMMA)
				param, error = self.id_statement()
				if error: return None, error
				input_parameters.append(param[1])
				
				if self.current_token.type == ASSIGN:
					self.eat(ASSIGN)
					
					arg_name = input_parameters[-1]
					default_args[arg_name], error = self.expression()
					if error: return None, error
		
		if self.current_token.type == COLON:
			self.eat(COLON)

			output_parameters = []

			if self.current_token.type != RPAREN:
				param, error = self.expression()
				if error: return None, error
				output_parameters.append(param)

				while self.current_token.type == COMMA:
					self.eat(COMMA)
					param, error = self.expression()
					if error: return None, error
					output_parameters.append(param)
		else:
			output_parameters = []

		self.eat(RPAREN)

		return (input_parameters, output_parameters, default_args), None
	
	def block(self):
		self.eat(LCURLY)
		statements = []

		while self.current_token.type != RCURLY:
			statement, error = self.statement()
			if error: return None, error
			statements.append(statement)

		self.eat(RCURLY)

		return statements, None
	
	def expression(self):
		expr, error = self.comparison_expression()
		if error: return None, error
	
		return expr, None
	
	def comparison_expression(self):
		result, error = self.power_expression()
		if error: return None, error
	
		count = 0

		while self.current_token.type in (LT, GT, LTE, GTE, EQ, NE, AND, OR):
			token = self.current_token
			
			if token.type == LT:
				self.eat(LT)
				left, error =self.power_expression()
				if error: return None, error
				result = ('<', result, left)
			elif token.type == GT:
				self.eat(GT)
				left, error =self.power_expression()
				if error: return None, error
				result = ('>', result, left)
			elif token.type == LTE:
				self.eat(LTE)
				left, error =self.power_expression()
				if error: return None, error
				result = ('<=', result, left)
			elif token.type == GTE:
				self.eat(GTE)
				left, error =self.power_expression()
				if error: return None, error
				result = ('>=', result, left)
			elif token.type == EQ:
				self.eat(EQ)
				left, error =self.power_expression()
				if error: return None, error
				result = ('==', result, left)
			elif token.type == NE:
				self.eat(NE)
				left, error =self.power_expression()
				if error: return None, error
				result = ('!=', result, left)
			elif token.type == AND:
				self.eat(AND)
				left, error =self.power_expression()
				if error: return None, error
				result = ('&', result, left)
			elif token.type == OR:
				self.eat(OR)
				left, error =self.power_expression()
				if error: return None, error
				result = ('|', result, left)
			
			if count == 0:
				last_term = result[-1]
			if count > 0:
				op, condition1, new_last_term = result
				
				condition2 = (op, last_term, new_last_term)
				
				result = ('&', condition1, condition2)
				
				last_term = new_last_term
			count += 1
		return result, None
	
	def power_expression(self):
		result, error = self.arithmetic_expression()
		if error: return None, error
		
		if self.current_token.type == CARET:
			self.eat(CARET)
			left, error =self.arithmetic_expression()
			if error: return None, error
			result = ('^', result, left)

		return result, None
	
	def arithmetic_expression(self):
		result, error = self.term()
		if error: return None, error

		while self.current_token.type in (PLUS, MINUS):
			token = self.current_token
			if token.type == PLUS:
				self.eat(PLUS)
				left, error =self.term()
				if error: return None, error
				result = ('+', result, left)
			elif token.type == MINUS:
				self.eat(MINUS)
				left, error =self.term()
				if error: return None, error
				result = ('-', result, left)

		return result, None
	
	def term(self):
		result, error = self.primary()
		if error: return None, error

		while self.current_token.type in (ASTERISK, DIVISION, MODULUS):
			token = self.current_token
			if token.type == ASTERISK:
				self.eat(ASTERISK)
				left, error =self.primary()
				if error: return None, error
				result = ('*', result, left)
			if token.type == DIVISION:
				self.eat(DIVISION)
				left, error =self.primary()
				if error: return None, error
				result = ('/', result, left)
			elif token.type == MODULUS:
				self.eat(MODULUS)
				left, error =self.primary()
				if error: return None, error
				result = ('%', result, left)

		return result, None
	
	def primary(self):
		result, error = self.factor()
		if error: return None, error
	
		while self.current_token.type in (LPAREN, LBRACKET):
			if self.current_token.type == LPAREN:
				result, error = self.function_call(result)
				if error: return None, error
			elif self.current_token.type == LBRACKET:
				result, error = self.factor_suffix(result)
				if error: return None, error
		return result, None

	def factor(self):
		token = self.current_token
		
		if token.type == ID:
			var, error = self.id_statement()
			if error: return None, error
			
			if self.current_token.type in (ASSIGN, INCREMENT, DECREMENT):
				value, error = self.factor_suffix(var)
				if error: return None, error
				
				return value, None
				
			return var, None
		elif token.type == NUM:
			self.eat(NUM)
			return ('Number', token.value), None
		elif token.type == STR:
			self.eat(STR)
			return ('String', token.value), None
		elif token.type == KEYWORD:
			self.eat(KEYWORD)
			if token.value == 'True':
				return ('Bool', True), None
			elif token.value == 'False':
				return ('Bool', False), None
			elif token.value == 'break':
				return ('Flow', token.value), None
			elif token.value == 'continue':
				return ('Flow', token.value), None
			elif token.value == 'None':
				return ('None', None), None
			else:
				return None, None
		elif token.type == LPAREN:
			self.eat(LPAREN)
			
			result = None
			if self.current_token.type != RPAREN:
				result, error = self.expression()
				if error: return None, error
			
			expr_list = [result]
			while self.current_token.type == COMMA:
				self.eat(COMMA)
				expr, error = self.expression()
				if error: return None, error
				expr_list.append(expr)
				
			self.eat(RPAREN)
			return (result, None) if len(expr_list) == 1 else (expr_list, None)
		elif token.type == LBRACKET:
			vectors, error = self.vector_elements()
			if error: return None, error
			return vectors, None
		elif token.type == LCURLY:
			value, error = self.dict_elements()
			if error: return None, error
			return value, None
		elif token.type == LPAREN:
			value, error = self.multi_assignment()
			if error: return None, error
			return value, None
		elif token.type == MINUS:
			self.eat(MINUS)
			value, error = self.factor()
			if error: return None, error
			return ('-', value), None
		elif token.type == PLUS:
			self.eat(PLUS)
			value, error = self.factor()
			if error: return None, error
			return ('+', value), None
		elif token.type == NEGATE:
			self.eat(NEGATE)
			value, error = self.factor()
			if error: return None, error
			return ('!', value), None
		else:
			return None, ParseError(
				'ParseError',
				token.value,
				token.pos_start,
				self.line_number-1,
				self.text,
				'Unexpected token'
			)
			
	def multi_assignment(self, var_name):
		var_list = [var_name]
		
		while self.current_token.type == COMMA:
			self.eat(COMMA)
			value, error = self.id_statement()
			if error: return None, error 
			
			var_list.append(value)
		
		if self.current_token.type == SEMI:
			self.eat(SEMI)
			return ('multi', var_list, [None]*len(var_list)), None
		
		self.eat(ASSIGN)
		
		expr_list, error = self.expression()
		if error: return None, Error
		
		if type(expr_list) is not list: expr_list = [expr_list]
		
		self.eat(SEMI)
		
		return ('multi', var_list, expr_list), None

	def factor_suffix(self, expression):
		token = self.current_token
		
		if token.type == ASSIGN:
			value, error = self.variable_assign(expression)
			if error: return None, error
			return value, None
		if token.type == INCREMENT:
			self.eat(INCREMENT)
			return ('++', expression), None
		if token.type == DECREMENT:
			self.eat(DECREMENT)
			return ('--', expression), None
		if token.type == COMMA:
			self.eat(COMMA)
			value, error = self.multi_assignment(expression)
			if error: return None, error
			return value, None
		if token.type == LPAREN:
			self.eat(LPAREN)
			arguments, error = self.arguments()
			if error: return None, error
			self.eat(RPAREN)
			return ('call', expression, arguments), None
		elif token.type == LBRACKET:
			self.eat(LBRACKET)
			index, error = self.expression()
			if error: return None, error
			self.eat(RBRACKET)
			return ('index', expression, index), None

	def function_call(self, expression):
		arguments, error = self.arguments()
		if error: return None, error
		
		return ('call', expression, arguments), None

	def arguments(self):
		'''
		arguments	-> expression ("," expression)*
		'''
		self.eat(LPAREN)
		
		if self.current_token.type == RPAREN:
			arg_list = []
		else:
			arg, error = self.expression()
			if error: return None, error
			arg_list = [arg]
			while self.current_token.type == COMMA:
				self.eat(COMMA)
				arg, error = self.expression()
				if error: return None, error
				
				arg_list.append(arg)
		
		self.eat(RPAREN)
		
		return arg_list, None

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
	def __init__(self, text, cmd=False):
		self.text = text
		self.cmd = cmd
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
		if not self.cmd: quit()
		
	def interpret(self, ast):
		for statement in ast:
			__, error = self.execute_statement(statement)
			
			if error: return None, error
		return __, None

	def execute_statement(self, statement, scope={}):
		statement_type = statement[0]
		
		if statement_type == 'let':
			value, error  = self.execute_variable_declaration(statement, scope)
			if error: return None, error
			return value, None
		elif statement_type == 'if':
			value, error  = self.execute_if_statement(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'class':
			value, error  = self.execute_class_declaration(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'parent':
			value, error  = self.execute_parent_declaration(statement, scope)
			if error: return None, error
			return value, None
		elif statement_type == 'function':
			value, error  = self.execute_function_declaration(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'from':
			value, error  = self.execute_from_statement(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'while':
			value, error  = self.execute_while_loop(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'for':
			value, error  = self.execute_for_loop(statement)
			if error: return None, error
			return value, None
		elif statement_type == 'return':
			value, error  = self.execute_return_statement(statement)
			if error: return None, error
			return value, None
		else:
			value, error  = self.evaluate_expression(statement, scope)
			if error: return None, error
			return value, None
	
	def execute_return_statement(self, statement):
		if len(statement) > 1:
			self.return_value = []
			for expression in statement[1]:
				expr, error = self.evaluate_expression(expression)
				if error: return None, error
				
				self.return_value.append(expr	)
		else:
			self.return_value = None
			
		return None, None

	def execute_while_loop(self, statement):
		result, error = self.evaluate_expression(statement[1])
		if error: return None, error
		
		while result:
			for line in statement[2]:
				if self.continue_loop: 
					self.continue_loop = False
					continue
				__, error = self.execute_statement(line)
				if error: return None, error
				
				result, error = self.evaluate_expression(statement[1])
				if error: return None, error
			
				if self.break_loop or self.return_value is not None: break
			
			if self.break_loop or self.return_value is not None: break
		self.break_loop = False
		
		### Change results to None if while is not to return anything
		return None, None
	
	def execute_for_loop(self, statement):
		(iterable, loop_variables), loop_block = statement[1:]
		
		if iterable[0] == 'var': 
			iterable, error = self.get_variable_value(iterable[1])
			if error: return None, error
		
		iterator = IterableIterator(iterable)
		
		loop_variable = loop_variables[0][1]
		self.create_loop_variable(loop_variable)
		
		while True:
			try:
				value = next(iterator)
				self.create_new_scope()
				if loop_variable is not None:
					self.set_variable_value(loop_variable, value)
				
				results, error = self.execute_block(loop_block, self.current_scope)
				if error: return None, error
				
				self.destroy_current_scope()
			except StopIteration:
				break
		#self.clean_up([loop_variable])
		
		### Change results to None if while is not to return anything
		return results, None
	
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
						return None,  ExecutionError(
							'ExecutionError : UndefinedObject', 
							f"Tried to create '{object_name}.{property_name}' while '{object_name}' does not exist"
						)
				
			while type(property_name) is tuple and parent is not None:
				
				expression = property_name
				object_name = expression[1]
				parent = parent.get(object_name)
				property_name = expression[-1]
			
			if parent is None:
				expr = (".", object_name, property_name)
				return None,  ExecutionError(
					'ExecutionError : UndefinedObject', 
					f"Tried to create '{self.show_varname(expr)}' while '{object_name}' does not exist"
				)
			
			if len(statement) > 2:
				value, error = self.evaluate_expression(statement[2]) 
			else:
				value, error = None, None
			
			if error: return None, error
		
			parent[property_name] = value
			
			### Change the value to None if we should not return anything on assignment
			return value, error
		
		if len(statement) > 2:
			initial_value, error = self.execute_variable_assignment(variable_name, statement[2])
			if error: return None, error
		else:
			initial_value = None
			self.current_scope[variable_name] = initial_value
			self.local_vars.append(variable_name)
			
		#return initial_value, None
		return None, None
	
	def execute_variable_assignment(self, variable_name, expression):
		value, error = self.evaluate_expression(expression)
		if error: return None, error
		
		self.current_scope[variable_name] = value
		self.local_vars.append(variable_name)
		
		#return value, None
		return None, None
	
	def evaluate_expression(self, expression, scope={}):
		if isinstance(expression, int) or isinstance(expression, str) or isinstance(expression, bool):
			return expression, None
		elif isinstance(expression, list):
			vector = []
			
			for item in expression:
				value, error = self.evaluate_expression(item)
				
				if error: return None, error
				vector.append(value)
				
			return  vector, None
		elif isinstance(expression, dict):
			mar_dict = {}
			for key, item in expression.items():
				key, error = self.evaluate_expression(key)
				if error: return None, error
			
				value, error = self.evaluate_expression(item)
				if error: return None, error
				
				mar_dict[key] = value
			mar_dict['::type'] = 'dict'
			return mar_dict, None
		elif expression is None:
			return 'None', None
		elif isinstance(expression, tuple):
			expression_type = expression[0]
			if expression_type == 'Number':
				return expression[1], None
			elif expression_type == 'String':
				return expression[1], None
			elif expression_type == 'Bool':
				return expression[1], None
			elif expression_type == 'None':
				return expression[1], None
			elif expression_type == 'Flow':
				return self.break_and_continue(expression[1]), None
			elif expression_type == 'var':
				return self.get_variable_value(expression[1], scope)
			elif expression_type in ['!', '-', '++', '--'] and len(expression) <= 2:
				return self.evaluate_unary_operation(expression)
			elif expression_type in BIN_OPS:
				return self.evaluate_binary_operation(expression)
			elif expression_type == '.':
				return self.evaluate_property_access(expression, scope)
			elif expression_type == 'multi':
				return self.evaluate_multi_assign(expression, scope)
			elif expression_type == 'call':
				self.stack_trace.append(self.show_varname(expression[1][1]))
				value, error = self.evaluate_function_call(expression, scope)
				if error: return None, error
				self.stack_trace.pop()
				return value, None
			elif expression_type == 'index':
				return self.evaluate_index_value(expression)
			else:
				return None, ExecutionError(
					'ExecutionError: InvalidExpression',
					f"Invalid expression: '{expression_type}'"
				)
		else:
			return None, ExecutionError(
				'ExecutionError: InvalidExpression',
				f"Invalid expression: '{expression_type}'"
			)
			
	def get_variable_value(self, variable_name, scope={}):
		if type(variable_name) is tuple:
			return self.evaluate_property_access(variable_name, scope)
		if variable_name in self.current_scope:
			return self.current_scope[variable_name], None 
		for scope in reversed(self.scopes):
			if variable_name in scope:
				return scope[variable_name], None
		if variable_name in self.internal_variables:
			return self.internal_variables[variable_name], None
		
		return None, ExecutionError(
			'ExecutionError: UndefinedVariable',
			f"Variable '{self.show_varname(variable_name)}' is not defined"
		)
	
	def execute_from_statement(self, statement):
		parent_module = statement[1]
		import_modules = statement[2]
		aliases = statement[-1]
		
		if aliases and len(aliases) != len(import_modules):
			return None, ExecutionError(
				'ExecutionError: ImportError',
				f'Aliases given did not match the modules imported'
			)
			
		if not aliases:
			aliases = [None] * len(import_modules)
		
		#if not parent_module:
			#self.execute_use_statement(import_modules, aliases)
		#else:
		__, error =  self.execute_import(parent_module[1], import_modules, aliases)
		if error: return None, error
		
		return None, None
		
	def execute_import(self, parent_module, import_modules, aliases):
		parent_module = self.show_varname(parent_module)
		
		filename, content, error = self.get_content(parent_module)
		if error: return None, error
		
		tokens = Lexer(content).lex()
		
		ast, error = Parser(tokens, content).parse()
		if error: return error
	
		internal = Interpreter(content)
		res, error = internal.interpret(ast)
		
		for import_module, alias in zip(import_modules, aliases):
			#checking in global_scope
			if import_module[1] in internal.global_scope:
				value = internal.global_scope[import_module[1]]
				if type(value) is dict:
					type_ = value.get('::type', None)
					if type_ and type(type_) is list:
						for class_name in value['::type']:
							self.classes[class_name] = internal.classes[class_name]
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
				alias = alias[0]
				self.import_all(import_module[1], alias[1], internal)
				continue
			return None, ExecutionError(
					'ExecutionError: ImportError',
					f"Module '{import_module[1]}' was not found in '{parent_module}' ({filename})"
				)
		return None, None
	
	def get_content(self, module_name):
		filename = self.make_filename(module_name)
		if not filename: 
			return None, None, ExecutionError(
				'ExecutionError: ImportError',
				'Failed to get the module location'
			)
		
		try:
			with open(filename, 'r') as fo:
				content = fo.read()
		except FileNotFoundError:
			# Threading can cause this error
			return filename, None, ExecutionError(
				'ExecutionError: ImportError', 
				f"Module was not found!\nNo module named '{module_name.replace('.', '/')}'"
			)
		
		return filename, content, None
	
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
		obj, error = self.evaluate_expression(expression[1])
		if error: return None, error
		index, error = self.evaluate_expression(expression[-1])
		if error: return None, error
		
		if type(index) is not int and type(obj) is not dict:
			return None, ExecutionError(
				'ExecutionError: TypeError',
				f"index must be an int but found {index}"
			)
			
		return obj[index], None
		
	def evaluate_multi_assign(self, statement, scope={}):
		variables = statement[1]
		expressions = []
		
		for __ in statement[-1]:
			expression, error = self.evaluate_expression(__)
			
			if error: return None, error
			expressions.append(expression)
		
		if len(expressions) == 1 and type(expressions) is list:
			expressions = expressions[0]
			
		if len(variables) != len(expressions):
			return None, ExecutionError(
				'ExecutionError: MultiAssignmentError',
				f"expected {len(variables)} values but found {len(expressions)}"
			)
		
		for var_name, value in zip(variables, expressions):
			self.set_variable_value(var_name[1], value)
		
		### Change expressions to None if not supposed to give responses
		#return expressions, None
		return None, None
				
	def break_and_continue(self, statement):
		if statement == 'break':self.break_loop = True
		elif statement == 'continue' :self.continue_loop = True
		return None
		
	def execute_if_statement(self, if_statement):
		condition, if_block, elif_clauses, else_clause = if_statement[1:]
		
		res, error = self.evaluate_expression(condition)
		if error: return None, error
		
		if res:
			__, error = self.execute_block(if_block)
			if error: return None, error
		else:
			for elif_condition, elif_block in elif_clauses:
				res, error = self.evaluate_expression(elif_condition)
				if error: return None, error
				if res:
					for statement in elif_block:
						__, error = self.execute_statement(statement)
						if error: return None, error
					return None, None
			if else_clause:
				for statement in else_clause:
					__, error = self.execute_statement(statement)
					if error: return None, error
		return None, None

	def evaluate_binary_operation(self, expression):
		operator = expression[0]
		
		left_operand, error = self.evaluate_expression(expression[1])
		if error: return None, error
	
		right_operand, error = self.evaluate_expression(expression[2])
		if error: return None, error
		
		if operator == '+':
			return (left_operand + right_operand), None
		elif operator == '-':
			return (left_operand - right_operand), None
		elif operator == '*':
			return (left_operand * right_operand), None
		elif operator == '^':
			return (left_operand ** right_operand), None
		elif operator == '/':
			return (left_operand / right_operand), None
		elif operator == '%':
			return (left_operand % right_operand), None
		elif operator == '>':
			return (left_operand > right_operand), None
		elif operator == '<':
			return (left_operand < right_operand), None
		elif operator == '<=':
			return (left_operand <= right_operand), None
		elif operator == '>=':
			return (left_operand >= right_operand), None
		elif operator == '!=':
			return (left_operand != right_operand), None
		elif operator == '&':
			return (left_operand and right_operand), None
		elif operator == '|':
			return (left_operand or right_operand), None
		elif operator == '==':
			return (left_operand == right_operand), None
		else:
			return None, ExecutionError(
				'ExecutionError: InvalidBinaryOperator',
				f"Invalid binary operator: '{operator}'"
			)
	
	def evaluate_unary_operation(self, expression):
		operator = expression[0]
		operand, error = self.evaluate_expression(expression[1])
		if error: return None, error
	
		if operator == '!':
			return not operand, None
		elif operator == '-':
			return -operand, None
		elif operator == '++':
			value = operand + 1
			self.set_variable_value(expression[1][1], value)
			return value, None
		elif operator == '--':
			value =  operand - 1
			self.set_variable_value(expression[1][1], value)
			return value, None
		else:
			return None, ExecutionError(
				'ExecutionError: InvalidUnaryOperator',
				f"Invalid unary operator: '{operator}'"
			)
	
	def evaluate_property_access(self, expression, scope={}):
		object_name = expression[1]
		property_name = expression[2]
		object_value, error = self.get_variable_value(object_name)
		if error: return None, error
	
		if object_name != 'me' and 'me' in object_value.keys():
			object_value = object_value['me']
		
		while type(property_name) is tuple:
			expression = property_name
			object_value = object_value[property_name]
			property_name = expression[2]
		
		if isinstance(object_value, dict) and property_name in list(object_value.keys()):
			return object_value[property_name], None
		else:
			return None, ExecutionError(
				'ExecutionError: UndefinedProperty',
				f"Property '{property_name}' not found on object '{object_name}'"
			)
		
	def execute_block(self, block, scope={}):
		for statement in block:
			__, error = self.execute_statement(statement, scope)
			if error: return None, error
			if self.return_value is not None:
				break
		return self.return_value, None
	
	def execute_function_declaration(self, statement):
		function_name = statement[1][1]
		parameters = statement[2]
		body = statement[3]
		
		self.functions[function_name] = (parameters, body)
		return None, None

	def evaluate_function_call(self, statement, scope):
		identifier = statement[1][1]
		args = statement[2]
		func_scope = {}

		cls_method = False
		if identifier in list(INBUILT_FUNCTION.keys()):
			expressions = []

			for arg in args:
				value, error = self.evaluate_expression(arg, self.current_scope) 

				if error: return None, error
				expressions.append(value)
				
			return INBUILT_FUNCTION[identifier](expressions)
		elif type(identifier) is tuple:
			object_name = identifier[1]

			object_value, error = self.get_variable_value(object_name)
			if error: return None, error

			if type(object_value) is list or type(object_value) is str or type(object_value) is int:
				return self.evaluate_list_method(object_value, identifier, args)
			
			if not object_value.get('::alias', None):
				# check if current scope is in an object
				if object_value.get('::type', None):
					class_name = object_value['::type'][0]
				else:
					class_name =   self.current_scope['::type'][0] 
			else:
				class_name = object_value[object_name]['::alias']
			
			method_name = identifier[2]
			while type(method_name) is tuple:
				object_name = method_name[1]
				object_value, error = self.get_variable_value(object_name)
				if error: return None, error
			
				if type(object_value) is list or type(object_value) is str or type(object_value) is int:
					return self.evaluate_list_method(object_value, identifier)
				
				if not object_value.get('::alias', None):
					# sheck if current scope is in an object
					if object_value.get('::type', None):
						class_name = object_value['::type'][0]
					else:
						class_name =   self.current_scope['::type'][0] 
				else:
					class_name = object_value['::alias']
				
				method_name = method_name[-1]
			
			method = self.classes.get(class_name).get(method_name)
			
			if not method:
				classes, error = self.get_variable_value(object_name)
				if error: return None, error
				
				classes = classes['::type']
				for class_name in classes[1:]:
					while type(class_name) is tuple:
						class_name = class_name[-1]
						
					method = self.classes.get(class_name).get(method_name)
					if method: break
				
			if not method: 
				print(method_name)
				return None, ExecutionError(
					'ExecutionError: UndefinedMethod',
					f"Method '{method_name}()' not found on object '{self.show_varname(object_name)}'"
				)
			parameters, body = method
			
			if 'me' == parameters[0][0]:
				func_scope, error = self.get_variable_value(object_name)
			cls_method = True
		elif identifier in list(self.classes.keys()):
			return self.execute_class_constructor(identifier, args)
		elif identifier not in self.functions:
			return None, ExecutionError(
				'ExecutionError: UndefinedVariable',
				f"Identifier '{self.show_varname(identifier)}' is not defined"
			)
		else:
			parameters, body = self.functions[identifier]
		
		input_params, output_params, default_args = parameters
		
		new_scope = {}
		if func_scope:
			new_scope = func_scope
			input_params = input_params[1:]
		
		if len(input_params) != (len(args)+len(default_args)) and len(input_params) != len(args):
			return None, ExecutionError(
				'ExecutionError: FunctionError',
				f"Function '{self.show_varname(identifier)}()' expects {len(input_params) - len(default_args)} arguments, but {len(args)} {'was' if len(input_params) == 1 else 'were' } provided"
			)
			
		for key, value in default_args.items():
			new_scope[key], error = self.evaluate_expression(value)
			if error: return None, error
		
		if args:
			size = len(input_params) if len(args) == len(input_params) else	len(input_params)-len(default_args)
			for i in range(size):
				parameter = input_params[i]
				argument, error = self.evaluate_expression(args[i])
				if error: return None, error
				new_scope[parameter] = argument
		
		self.scopes.append(new_scope)
		self.current_scope = new_scope
		
		initial_return, error = self.execute_block(body, self.current_scope)
		if error: return None, error
		
		if initial_return:
			self.return_value = None
			self.clean_up(input_params)
			self.scopes.pop()
			self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
			self.local_vars = []
			if len(initial_return) == 1: return initial_return[0], None
			else: return initial_return, None
		
		retr =  []
		for param in output_params:
			value, error = self.evaluate_expression(param, self.current_scope)
			if error: return None, error
			retr.append(value)
		
		self.clean_up(input_params)
		self.destroy_current_scope()
		self.clean_scope()
		
		self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
		self.local_vars = []
		
		if retr:
			if len(retr) == 1: return retr[0], None
			else: return retr, None
		else: return None, None
	
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
		return None, None
	
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
			class_var, error = self.execute_special(constructor, args, class_var)
			if error: return None, error
			
			return class_var, None
		else:
			return class_var, None
	
	def execute_parent_declaration(self, statement, scope):
		class_name = statement[1][1]
		args = statement[-1]
		
		constructor = self.classes.get(class_name).get(class_name)
		
		cls_name = scope['::type'][0] if not scope['::alias'] else scope['::alias']
		parent_classes = self.classes[cls_name][1]
		
		if statement[1] in parent_classes:
			scope['::type'].append(class_name)
		else:
			return None, ExecutionError(
				'ExecutionError; ClassError',
				f"class '{cls_name}' has not defined parent class '{class_name}' in Parent class list"
			)
			
		
		if not constructor: return None, None
		return self.execute_special(constructor, args, scope)
		
	def execute_special(self, constructor, args, class_dict):
		parameters, body = constructor
		
		input_params, output_params, default_args = parameters
		
		if input_params[0] != 'me': 
			return None, ExecutionError(
				'ExecutionError: ClassError',
				f"Expected 'me' as first class '{class_dict['::type']}' constructor parameter but found '{input_params[0]}'"
			)
		
		input_params = input_params[1:]
		if len(input_params) != (len(args)+len(default_args)) and len(input_params) != len(args):
			return None, ExecutionError(
				'ExecutionError: ClassError',
				f"class '{class_dict['::type']}' constructor expects {(len(input_params) - len(default_args)) if len(input_params) else 'no'} arguments, but {len(args)} {'was' if len(args) == 1 else 'were' } provided \n\n{self.evaluate_expression(args)}\n"
			)
			
		new_scope = {}
		
		for key, value in default_args.items():
			new_scope[key], error = self.evaluate_expression(value)
			if error: return None, error
		
		if args:
			size = len(input_params) if len(args) == len(input_params) else	len(input_params)-len(default_args)
			for i in range(size):
				parameter = input_params[i]
				argument, error = self.evaluate_expression(args[i])
				if error: return None, error
				new_scope[parameter] = argument
		
		
		self.scopes.append(new_scope)
		self.current_scope = new_scope
		self.local_vars = []
		
		for statement in body:
			__, error = self.execute_statement(statement, class_dict)
			if error: return None, error
		
		
		self.clean_up(input_params)
		self.destroy_current_scope()
		self.clean_scope()
		
		self.current_scope = self.scopes[-1] if self.scopes else self.global_scope
		self.local_vars = []
		
		return class_dict, None
	
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
			arguments = []
			for arg in args:
				res, error = self.evaluate_expression(arg, self.current_scope)
				if error: return None, error
				arguments.append(res)
			return method(*arguments), None
		except :
			obj_type = type(obj)
			if obj_type is str:
				obj_type = 'String'
			elif obj_type is int:
				obj_type = "Number"
			else:
				obj_type = "Vector"
			return None, ExecutionError(
				'ExecutionError: TypeError',
				f"'{obj_type}' object has no method '{function}'"
			)

class InlineParser(Parser):
	pass

class InlineInterpreter(Interpreter):
	def set_text(self, text):
		self.text = text
		
	def interpret(self, ast):
		results = []
		for statement in ast:
			result, error = self.execute_statement(statement)
			if error: return None, error
			
			if result is not None: results.append(result)
		
		return results, None
