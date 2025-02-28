class Node:
    pass


class Number(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class Decimal(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Decimal({self.value})"


class String(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String('{self.value}')"


class Character(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Character('{self.value}')"


class Boolean(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"


class Variable(Node):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Variable({self.name})"


class TypedVariable(Node):
    def __init__(self, name, type_name):
        self.name = name
        self.type_name = type_name
        
    def __repr__(self):
        return f"TypedVariable({self.name}, {self.type_name})"


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


class TypedAssignment(Node):
    def __init__(self, name, type_name, expr):
        self.name = name
        self.type_name = type_name
        self.expr = expr
        
    def __repr__(self):
        return f"TypedAssignment({self.name}, {self.type_name}, {self.expr})"


class Print(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"Print({self.expr})"
    

class Input(Node):
    def __init__(self, prompt=None, input_type=None):
        self.prompt = prompt
        self.input_type = input_type
    
    def __repr__(self):
        return f"Input(prompt={self.prompt}, input_type={self.input_type})"


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
    

class FunctionDefinition(Node):
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters  # List of parameter names (strings)
        self.body = body  # List of statements
        
    def __repr__(self):
        return f"FunctionDefinition({self.name}, {self.parameters}, {self.body})"


class ReturnStatement(Node):
    def __init__(self, expr):
        self.expr = expr
        
    def __repr__(self):
        return f"ReturnStatement({self.expr})"    


class LengthFunction(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"LengthFunction({self.expr})"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        if tokens:
            self.current_token = self.tokens[0]
        else:
            self.current_token = ('EOF', '')

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
            return Number(token_value)
            
        elif token_type == 'DECIMAL':
            self.advance()
            return Decimal(token_value)
            
        elif token_type == 'BOOL_TRUE' or token_type == 'BOOL_FALSE':
            value = True if token_type == 'BOOL_TRUE' else False
            self.advance()
            return Boolean(value)

        elif token_type == 'STRING':
            value = token_value
            self.advance()
            # Check if it's a single character
            if len(value) == 1:
                return Character(value)
            return String(value)
        
        elif token_type == 'INPUT':
            self.advance()
            self.consume('LPAREN')
            
            # Parse prompt if present
            prompt = None
            if self.current_token[0] == 'STRING':
                prompt = self.current_token[1]
                self.advance()
                
                # Check if there's a comma followed by a type
                input_type = None
                if self.current_token[0] == 'COMMA':
                    self.advance()
                    if self.current_token[0] in ('TYPE_NUM', 'TYPE_STR', 'TYPE_DEC', 'TYPE_CHR', 'TYPE_BOOL'):
                        input_type = self.current_token[1]
                        self.advance()
                    else:
                        raise SyntaxError(
                            f"Expected type after comma in eingabe, got {self.current_token[0]}")
                
                self.consume('RPAREN')
                return Input(prompt, input_type)
            
            # No prompt, just closing parenthesis
            self.consume('RPAREN')
            return Input()

        elif token_type == 'IDENT':
            self.advance()

            # Handle function calls like len(str1)
            if self.current_token[0] == 'LPAREN':
                self.advance()  # Consume '('
                args = []
                if self.current_token[0] != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.current_token[0] == 'COMMA':
                        self.advance()  # Consume ','
                        args.append(self.parse_expression())
                self.consume('RPAREN')
                return FunctionCall(token_value, args)

            return Variable(token_value)

        elif token_type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
            
        # Add handling for type keywords when they appear in expressions
        elif token_type in ('TYPE_NUM', 'TYPE_STR', 'TYPE_DEC', 'TYPE_CHR', 'TYPE_BOOL'):
            # In a factor context, this is an error - types aren't valid expressions
            raise SyntaxError(
                f"Type keyword '{token_value}' cannot be used as an expression at position {self.pos}")

        raise SyntaxError(
            f"Unexpected token in factor: {token_type} ('{token_value}') at position {self.pos}")

    def parse_block(self):
        """Parse a block enclosed in {}"""
        self.consume('LBRACE')
        statements = []
        
        while self.current_token[0] == 'NEWLINE':
            self.advance()
        
        while self.current_token[0] != 'RBRACE' and self.current_token[0] != 'EOF':
            statements.append(self.parse_statement())
            while self.current_token[0] == 'NEWLINE':
                self.advance()
        self.consume('RBRACE')
        while self.current_token[0] == 'NEWLINE':
            self.advance()
        return statements

    def parse_statement(self):
        """Parse a single statement"""
        while self.current_token[0] == 'NEWLINE':
            self.advance()
            
        if self.current_token[0] == 'FUNCTION':
            self.advance()
            # Get function name
            if self.current_token[0] != 'IDENT':
                raise SyntaxError(f"Expected function name, got {self.current_token[0]}")
            func_name = self.current_token[1]
            self.advance()
            
            # Parse parameters
            self.consume('LPAREN')
            parameters = []    
            if self.current_token[0] == 'IDENT':
                parameters.append(self.current_token[1])
                self.advance()
                while self.current_token[0] == 'COMMA':
                    self.advance()
                    if self.current_token[0] != 'IDENT':
                        raise SyntaxError(f"Expected parameter name, got {self.current_token[0]}")
                    parameters.append(self.current_token[1])
                    self.advance()
            self.consume('RPAREN')
            body = self.parse_block()
            return FunctionDefinition(func_name, parameters, body)
        
        elif self.current_token[0] == 'RETURN':
            self.advance()
            expr = self.parse_expression()
            return ReturnStatement(expr)
        
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
            else_body = None
            if self.current_token[0] == 'ELSE':
                self.advance()
                else_body = self.parse_block()
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
            
        elif self.current_token[0] in ('TYPE_NUM', 'TYPE_STR', 'TYPE_DEC', 'TYPE_CHR', 'TYPE_BOOL'):
            # This is a typed variable declaration
            type_name = self.current_token[1]  # Get the type name
            self.advance()
            
            if self.current_token[0] != 'IDENT':
                raise SyntaxError(f"Expected variable name after type, got {self.current_token[0]}")
                
            variable_name = self.current_token[1]
            self.advance()
            
            if self.current_token[0] == 'ASSIGN':
                # This is a declaration with initialization
                self.advance()
                expr = self.parse_expression()
                return TypedAssignment(variable_name, type_name, expr)
            else:
                # This is just a declaration without initialization
                return TypedVariable(variable_name, type_name)

        elif self.current_token[0] == 'IDENT':
            variable_name = self.current_token[1]
            self.advance()
            
            if self.current_token[0] == 'ASSIGN':
                self.advance()
                expr = self.parse_expression()
                return Assignment(variable_name, expr)
            else:
                # If it's not an assignment, we need to backtrack
                self.pos -= 1
                self.current_token = self.tokens[self.pos]
                
        # Handle expressions (including function calls)
        expr = self.parse_expression()
        return expr

    def parse(self):
        """Parse the entire input and return a list of statements."""
        statements = []
        while self.pos < len(self.tokens) and self.current_token[0] == 'NEWLINE':
            self.advance()
        while self.pos < len(self.tokens) and self.current_token[0] != 'EOF':
            try:
                statement = self.parse_statement()
                statements.append(statement)
                
                # Skip any semicolons between statements
                while self.current_token[0] == 'SEMICOLON':
                    self.advance()
                    
                # Skip any newlines between statements
                while self.current_token[0] == 'NEWLINE':
                    self.advance()
                    
            except Exception as e:
                # For debugging, add more context to the error
                token_info = f"{self.current_token[0]} ('{self.current_token[1]}') at position {self.pos}"
                raise SyntaxError(f"Error parsing statement at {token_info}: {str(e)}")
            
        return statements
