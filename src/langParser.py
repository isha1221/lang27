class Node:
    pass


class Number(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String('{self.value}')"


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"


class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"


class Assignment(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def __repr__(self):
        return f"Assignment({self.name}, {self.expr})"


class Print(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Print({self.expr})"


class IfStatement(Node):
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.body}, {self.else_body})"


class LoopStatement(Node):
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"LoopStatement({self.init}, {self.condition}, {self.update}, {self.body})"


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"


class LengthFunction(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"LengthFunction({self.expr})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else ('EOF', '')

    def advance(self):
        """Advance to the next token"""
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(
            self.tokens) else ('EOF', '')

    def peek(self):
        """Look at the next token without advancing"""
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else ('EOF', '')

    def consume(self, expected_type):
        """Consume a token of the expected type"""
        if self.current_token[0] == expected_type:
            token = self.current_token
            self.advance()
            return token
        raise SyntaxError(
            f"Expected {expected_type}, got {self.current_token[0]} ('{self.current_token[1]}') at position {self.pos}")

    def parse_expression(self):
        """Parse expressions including comparison operators"""
        left = self.parse_additive()
        while self.current_token[0] in ('EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'):
            op = self.current_token[1]
            self.advance()
            right = self.parse_additive()
            left = BinOp(left, op, right)
        return left

    def parse_additive(self):
        """Parse addition and subtraction"""
        left = self.parse_term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[1]
            self.advance()
            right = self.parse_term()
            left = BinOp(left, op, right)
        return left

    def parse_term(self):
        """Parse multiplication and division"""
        left = self.parse_factor()
        while self.current_token[0] in ('MUL', 'DIV'):
            op = self.current_token[1]
            self.advance()
            right = self.parse_factor()
            left = BinOp(left, op, right)
        return left

    def parse_factor(self):
        """Parse numbers, strings, variables, and function calls"""
        token_type, token_value = self.current_token

        if token_type == 'NUMBER':
            self.advance()
            return Number(int(token_value))

        elif token_type == 'STRING':
            self.advance()
            return String(token_value)

        elif token_type == 'IDENT':
            self.advance()

            # Handle function calls like len(str1)
            if self.current_token[0] == 'LPAREN':
                self.advance()  # Consume '('
                args = []
                while self.current_token[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    if self.current_token[0] == 'COMMA':
                        self.advance()  # Consume ','
                self.consume('RPAREN')
                return FunctionCall(token_value, args)

            return Variable(token_value)

        elif token_type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr

        raise SyntaxError(
            f"Unexpected token in factor: {token_type} ('{token_value}') at position {self.pos}")

    def parse_block(self):
        """Parse a block enclosed in `{}`"""
        self.consume('LBRACE')
        statements = []
        while self.current_token[0] != 'RBRACE' and self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return statements

    def parse_statement(self):
        """Parse a single statement"""
        while self.current_token[0] == 'NEWLINE':
            self.advance()
        if self.current_token[0] == 'IDENT':
            var_name = self.current_token[1]
            self.advance()
            self.consume('ASSIGN')
            expr = self.parse_expression()
            return Assignment(var_name, expr)
        elif self.current_token[0] == 'PRINT':
            self.advance()
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return Print(expr)
        elif self.current_token[0] == 'IF':
            self.advance()
            condition = self.parse_expression()
            body = self.parse_block()
            else_body = self.parse_block(
            ) if self.current_token[0] == 'ELSE' else None
            return IfStatement(condition, body, else_body)
        elif self.current_token[0] == 'FOR':
            self.advance()
            self.consume('LPAREN')
            init = self.parse_statement()  # Initialization (e.g., i = 0)
            self.consume('SEMICOLON')
            condition = self.parse_expression()  # Condition (e.g., i < 10)
            self.consume('SEMICOLON')
            update = self.parse_statement()  # Update (e.g., i = i + 1)
            self.consume('RPAREN')
            body = self.parse_block()  # Body of the loop
            return LoopStatement(init, condition, update, body)

        raise SyntaxError(
            f"Unexpected token: {self.current_token[0]} ('{self.current_token[1]}') at position {self.pos}")

    def parse(self):
        """Parse the entire input and return a list of statements."""
        statements = []
        while self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
        return statements
