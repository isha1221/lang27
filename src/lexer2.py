import re

TOKEN_SPEC = [
    ('PRINT',     r'drucken'),           # Print statement
    ('IF',        r'if'),                # If statement
    ('ELF',       r'elf'),               # Else if statement
    ('ELSE',      r'el'),                # Else statement
    ('EQ',        r'=='),                # Equals (must be before ASSIGN)
    ('NEQ',       r'!='),                # Not Equals
    ('LE',        r'<='),                # Less Than or Equal
    ('GE',        r'>='),                # Greater Than or Equal
    ('ASSIGN',    r'='),                 # Assignment
    ('LT',        r'<'),                 # Less Than
    ('GT',        r'>'),                 # Greater Than
    ('NUMBER',    r'\d+'),               # Integer
    ('STRING',    r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),  # Fixed string pattern
    ('IDENT',     r'[a-zA-Z_]\w*'),      # Variable names
    ('PLUS',      r'\+'),                # Addition
    ('MINUS',     r'-'),                 # Subtraction
    ('MUL',       r'\*'),                # Multiplication
    ('DIV',       r'/'),                 # Division
    ('LPAREN',    r'\('),                # Left Parenthesis
    ('RPAREN',    r'\)'),                # Right Parenthesis
    ('LBRACE',    r'\{'),                # Left Brace
    ('RBRACE',    r'\}'),                # Right Brace
    ('NEWLINE',   r'\n'),                # Newline
    ('SKIP',      r'[ \t]+'),            # Spaces and tabs (ignored)
]

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKEN_SPEC:
            pattern = re.compile(regex)
            match = pattern.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'STRING':
                    # Extract the string content without the quotes
                    if text.startswith('"'):
                        tokens.append((token_type, text[1:-1].replace('\\"', '"')))
                    else:  # starts with '
                        tokens.append((token_type, text[1:-1].replace("\\'", "'")))
                elif token_type != 'SKIP':  # Ignore spaces
                    tokens.append((token_type, text))
                pos += len(text)
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[pos]} at position {pos}")
    
    # Add an EOF token to simplify parsing
    tokens.append(('EOF', ''))
    return tokens