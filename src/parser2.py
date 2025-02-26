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

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else ('EOF', '')

    def advance(self):
        """Advance to the next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
            return self.current_token
        else:
            # Ensure we don't go beyond the end of the token list
            self.current_token = ('EOF', '')
            return self.current_token

    def peek(self):
        """Look at the next token without advancing"""
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return ('EOF', '')

    def consume(self, expected_type):
        """Consume a token of the expected type"""
        if self.current_token[0] == expected_type:
            token = self.current_token
            self.advance()
            return token
        else:
            token_type = self.current_token[0]
            token_value = self.current_token[1]
            raise SyntaxError(f"Expected {expected_type}, got {token_type} ('{token_value}') at position {self.pos}")

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
        """Parse basic expressions: numbers, strings, variables, parenthesized expressions"""
        token_type, token_value = self.current_token

        if token_type == 'NUMBER':
            self.advance()
            return Number(int(token_value))
        elif token_type == 'STRING':
            self.advance()
            return String(token_value)
        elif token_type == 'IDENT':
            self.advance()
            return Variable(token_value)
        elif token_type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token in factor: {token_type} ('{token_value}') at position {self.pos}")

    def parse_block(self):
        """Parse a block enclosed in `{}`"""
        self.consume('LBRACE')
        statements = []
        
        # Prevent infinite loop - use a max iteration guard
        max_iterations = 1000
        iteration_count = 0
        
        while (self.current_token[0] != 'RBRACE' and 
               self.current_token[0] != 'EOF' and 
               iteration_count < max_iterations):
            
            # Skip any newlines inside blocks
            while self.current_token[0] == 'NEWLINE':
                self.advance()
                # Guard against infinite loop here too
                iteration_count += 1
                if iteration_count >= max_iterations:
                    raise RuntimeError("Maximum loop iterations exceeded while skipping newlines")
            
            # Break if we reached the end of block
            if self.current_token[0] == 'RBRACE':
                break
                
            # Parse the statement and add it to our block
            if self.current_token[0] != 'EOF':
                statements.append(self.parse_statement())
            
            iteration_count += 1
        
        if iteration_count >= max_iterations:
            raise RuntimeError("Maximum loop iterations exceeded while parsing block")
            
        if self.current_token[0] == 'EOF':
            raise SyntaxError("Unexpected end of file while parsing block - missing '}'")
            
        self.consume('RBRACE')
        return statements

    def parse_statement(self):
        """Parse a single statement"""
        if self.current_token[0] == 'EOF':
            raise SyntaxError("Unexpected end of file while parsing statement")
            
        token_type = self.current_token[0]
        
        if token_type == 'IDENT':
            var_name = self.current_token[1]
            self.advance()
            self.consume('ASSIGN')
            expr = self.parse_expression()
            return Assignment(var_name, expr)

        elif token_type == 'PRINT':
            self.advance()
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return Print(expr)

        elif token_type == 'IF':
            self.advance()
            condition = self.parse_expression()
            body = self.parse_block()
            
            # Handle else-if and else
            if self.current_token[0] == 'ELF':
                # Create a chain of if-else statements for else-if branches
                return self.parse_if_else_chain(condition, body)
            
            # Simple if with optional else
            else_body = None
            if self.current_token[0] == 'ELSE':
                self.advance()
                else_body = self.parse_block()
                
            return IfStatement(condition, body, else_body)
        else:
            raise SyntaxError(f"Unexpected token in statement: {token_type} ('{self.current_token[1]}') at position {self.pos}")

    def parse_if_else_chain(self, condition, body):
        """Parse a chain of if-else-if-else statements"""
        current_if = IfStatement(condition, body)
        last_if = current_if
        
        # Maximum iterations to prevent infinite loops
        max_iterations = 100
        iteration_count = 0
        
        # Handle chains of else-if statements
        while self.current_token[0] == 'ELF' and iteration_count < max_iterations:
            self.advance()
            elf_condition = self.parse_expression()
            elf_body = self.parse_block()
            
            # Create a new if statement for this else-if and link it to the previous one
            new_if = IfStatement(elf_condition, elf_body)
            last_if.else_body = [new_if]  # Wrap in list to maintain statement block structure
            last_if = new_if
            
            iteration_count += 1
        
        if iteration_count >= max_iterations:
            raise RuntimeError("Maximum loop iterations exceeded while parsing else-if chain")
        
        # Handle final else if present
        if self.current_token[0] == 'ELSE':
            self.advance()
            else_body = self.parse_block()
            last_if.else_body = else_body
            
        return current_if

    def parse(self):
        """Parse the entire program"""
        statements = []
        
        # Maximum iterations to prevent infinite loops
        max_iterations = 1000
        iteration_count = 0
        
        # Parse until we reach the end of file
        while self.current_token[0] != 'EOF' and iteration_count < max_iterations:
            # Skip any standalone newlines
            while self.current_token[0] == 'NEWLINE':
                self.advance()
                iteration_count += 1
                if iteration_count >= max_iterations:
                    raise RuntimeError("Maximum loop iterations exceeded while skipping newlines")
                    
            # Break if we reached the end of file
            if self.current_token[0] == 'EOF':
                break
            
            # Parse the statement and add it to our AST
            statement = self.parse_statement()
            statements.append(statement)
            
            iteration_count += 1
        
        if iteration_count >= max_iterations:
            raise RuntimeError("Maximum loop iterations exceeded while parsing program")
            
        return statements