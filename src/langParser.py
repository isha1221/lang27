from lexer import tokenize

class Node:
    pass

class Number(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Print(Node):
    def __init__(self, expr):
        self.expr = expr

class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.tokens[self.pos][0]}")

    def parse_expression(self):
        left = self.parse_term()

        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'):
            op = self.tokens[self.pos][1]
            self.consume(self.tokens[self.pos][0])
            right = self.parse_term()
            left = BinOp(left, op, right)

        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('MUL', 'DIV'):
            op = self.tokens[self.pos][1]
            self.consume(self.tokens[self.pos][0])
            right = self.parse_factor()
            left = BinOp(left, op, right)
        return left

    def parse_factor(self):
        token_type, token_value = self.tokens[self.pos]
        if token_type == 'NUMBER':
            self.consume('NUMBER')
            return Number(int(token_value))
        elif token_type == 'STRING':
            self.consume('STRING')
            return String(token_value)
        elif token_type == 'IDENT':
            self.consume('IDENT')
            return Variable(token_value)
        elif token_type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token_value}")

    def parse_block(self):
        """ Parses a block enclosed in `{}` """
        self.consume('LBRACE')
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return statements

    def parse_statement(self):
        print(f"Parsing statement at position: {self.pos}") # Debugging
        if self.pos >= len(self.tokens):
            return None # End of tokens.
        token_type, token_value = self.tokens[self.pos]
        print(f"Current token: {token_type}, {token_value}") # Debugging

        if token_type == 'IDENT':
            var_name = token_value
            self.consume('IDENT')
            self.consume('ASSIGN')
            expr = self.parse_expression()
            return Assignment(var_name, expr)

        elif token_type == 'PRINT':
            self.consume('PRINT')
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return Print(expr)

        elif token_type == 'IF':
            self.consume('IF')
            condition = self.parse_expression()
            body = self.parse_block()

            else_body = None
            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ELF':
                self.consume('ELF')
                elf_condition = self.parse_expression()
                elf_body = self.parse_block()
                else_body = [IfStatement(elf_condition, elf_body)]

            if self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'ELSE':
                self.consume('ELSE')
                else_body = self.parse_block()

            return IfStatement(condition, body, else_body)

        else:
            raise SyntaxError(f"Unexpected token: {token_value}")

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos][0] == 'NEWLINE':
                self.pos += 1
                continue
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
        return statements
